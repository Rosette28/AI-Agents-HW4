# PRD — Naive Baseline Agent

Parent document: `docs/PRD.md`. Architecture: `docs/PLAN.md` Sections 1.3,
2.2. Counterpart to `docs/PRD_graph_guided_agent.md`; feeds
`docs/PRD_instrumentation_and_comparison.md`.

## 1. Description & Theoretical Background

The naive baseline agent (`naive_baseline.py`) implements the **control
condition** for the token-efficiency experiment (Task E / FR5). It performs
the same task as the graph-guided agent — locate and explain the root cause
of HTTPie Bug #3 in `data/httpie/httpie/sessions.py` — but **without** any
graph or vault guidance.

Theoretically, this models the most common real-world fallback when no
codebase map exists: an LLM is handed raw file contents (or large chunks)
from the target package and asked to find the bug, iterating by requesting
more files if it can't yet answer. This is the "paste large chunks of the
codebase into an LLM" failure mode described in `docs/PRD.md` Section 2,
and is the baseline against which the graph-guided approach's token/iteration
savings are measured.

## 2. Requirements, Input/Output, Performance Metrics

### Functional Requirements

- **NB-FR1**: Implement `naive_baseline.py` as a LangGraph (or simple loop)
  workflow operating on the same `AgentState` shape as the graph-guided
  agent (for instrumentation parity), but **without** access to
  `graph_tools` or `vault_io`.
- **NB-FR2**: On each iteration, select the "next raw file/chunk" from
  `httpie/` (e.g., in a fixed order: `sessions.py`, `client.py`,
  `downloads.py`, ... — or by simple heuristics like file size), pass its
  full content plus the bug-report-style question to the LLM, and ask for
  either a hypothesis or "need more files".
- **NB-FR3**: Enforce the same `max_iterations` from `config/agent.json` as
  the graph-guided agent (FR7) — identical stop condition for a fair
  comparison.
- **NB-FR4**: Call the same `instrumentation` hooks
  (`log_llm_call`, `log_file_read`, `log_iteration`) as the graph-guided
  agent (ADR-004) — same metrics, same schema.
- **NB-FR5**: On completion (success or `max_iterations` reached), write
  `reports/naive_run.json` (`InstrumentationLog`, `docs/PLAN.md` 6.2) with
  `mode: "naive"`.

### Input / Output Contract

- **Input**: `config/agent.json` (`max_iterations`, model), raw file
  contents from `data/httpie/httpie/*.py` (whole files, not snippets), the
  same bug description/question used for the graph-guided agent.
- **Output**: `reports/naive_run.json` with the same `InstrumentationLog`
  shape as `reports/graph_guided_run.json`, enabling direct comparison.

### Performance Metrics / Targets

- No correctness target is imposed beyond honest reporting — per
  `docs/PRD.md` Goals table, "numbers reported even if the result is
  negative" (i.e., even if naive mode happens to use fewer tokens, that
  result must be reported as-is, not adjusted).
- Expected (not required) outcome: higher `tokens_used` and `files_read`
  than the graph-guided agent, since it reads whole files rather than
  targeted snippets.

## 3. Constraints, Limitations, Alternatives Considered

### Constraints

- Must not import or call `graph_tools` / `vault_io` — any such access
  would invalidate the comparison.
- Must use the **same** `instrumentation` module and `InstrumentationLog`
  schema as the graph-guided agent (ADR-004) so `compare.py` can read both
  reports uniformly.
- Must use the **same** `max_iterations` value and the **same** underlying
  LLM/model as the graph-guided run for a like-for-like comparison.
- File selection order must be deterministic (documented in code/comments)
  so the run is reproducible.

### Alternatives Considered

- **Dump the entire `httpie/` package in a single prompt**: rejected as the
  sole mode — for very large codebases this would exceed context limits;
  the iterative "one file per step, ask if more needed" loop is more
  representative of how a developer/agent without a map would actually
  behave, and still produces comparable per-iteration metrics.
- **Random file order**: rejected in favor of a deterministic order, to
  keep the experiment reproducible across runs (NFR1).
- **Different stop condition than the graph-guided agent** (e.g., token
  budget instead of iteration count): rejected — using the same
  `max_iterations` keeps the comparison's "iterations" column meaningful.

## 4. Success Criteria & Test Scenarios

### Success Criteria

- Running `graphify_agent agent --mode naive --bug 3` produces
  `reports/naive_run.json` with a complete `InstrumentationLog`
  (`mode: "naive"`, `tokens_used`, `llm_calls`, `files_read`, `iterations`,
  `root_cause_found`).
- The run terminates within `max_iterations`, regardless of whether the
  root cause is found.
- `reports/naive_run.json` and `reports/graph_guided_run.json` are
  structurally identical (same keys/types), enabling `compare.py` to merge
  them into `reports/token_comparison.md`.
- Unit tests cover the file-selection and stop-condition logic with >=85%
  coverage (NFR3).

### Test Scenarios

1. **Happy path**: with a stubbed LLM that correctly identifies the bug
   after reading `sessions.py` (iteration 1), assert
   `root_cause_found: true`, `files_read == 1`, `iterations == 1`.
2. **Max-iterations exhaustion**: with a stubbed LLM that always returns
   "need more files", assert the run stops at exactly `max_iterations`,
   `root_cause_found: false`, and `files_read == max_iterations` (one new
   file per iteration).
3. **Deterministic file order**: assert two runs with the same stubbed LLM
   request files in the same order.
4. **Schema parity**: assert `reports/naive_run.json` and
   `reports/graph_guided_run.json` (from a stubbed run) have identical key
   sets, differing only in `mode` and values.
5. **No graph/vault access**: a static-analysis/unit test asserts
   `naive_baseline.py` does not import `graph_tools` or `vault_io`.
