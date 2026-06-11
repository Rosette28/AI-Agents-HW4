# PRD — Instrumentation & Token Comparison Mechanism

Parent document: `docs/PRD.md`. Architecture: `docs/PLAN.md` Sections 1.3,
1.4, 5.3, 6.2, 6.4, 6.5, ADR-004, ADR-006. Consumed by both
`docs/PRD_graph_guided_agent.md` and `docs/PRD_naive_baseline_agent.md`.

## 1. Description & Theoretical Background

This is the **measurement mechanism** that makes Task E (token-efficiency
comparison) and Task F (multi-bug generalization) meaningful: a
cross-cutting logger (`instrumentation.py`) shared by both agent workflows,
plus a report generator (`compare.py`) that turns raw logs into the
comparison artifacts required by the assignment.

The theoretical basis is straightforward **A/B instrumentation**: for the
comparison between graph-guided and naive modes to be valid, both arms must
record metrics through the *same code path* with the *same definitions*
(ADR-004) — otherwise differences in counting methodology could masquerade
as differences in approach. The four metrics tracked
(`tokens_used`, `llm_calls`, `files_read`, `iterations`) are the standard
proxies used in agentic-AI cost analysis: token count approximates $ cost
and context-window pressure; `llm_calls` and `iterations` approximate
latency/round-trip overhead; `files_read` approximates how much of the
codebase had to be "loaded" to reach an answer.

## 2. Requirements, Input/Output, Performance Metrics

### Functional Requirements

- **IC-FR1**: `instrumentation.py` exposes:
  - `log_llm_call(run_id: str, tokens_in: int, tokens_out: int) -> None`
  - `log_file_read(run_id: str, file_path: str) -> None`
  - `log_iteration(run_id: str) -> None`
  - `finalize(run_id: str, mode: str, root_cause_found: bool) ->
    InstrumentationLog`
- **IC-FR2**: `finalize()` aggregates all logged events for `run_id` into a
  single `InstrumentationLog` (`docs/PLAN.md` 6.2:
  `run_id`, `mode`, `tokens_used`, `llm_calls`, `files_read`, `iterations`,
  `root_cause_found`, `root_cause`) and writes it to
  `reports/<run_id>.json`.
- **IC-FR3**: `compare.py` reads `reports/graph_guided_run.json` and
  `reports/naive_run.json`, and writes `reports/token_comparison.md`
  containing:
  - a Markdown table with columns `mode | tokens_used | llm_calls |
    files_read | iterations | root_cause_found` (FR6/Section 6.4),
  - a bar chart image `reports/token_comparison.png` comparing the two
    modes across the numeric metrics,
  - 1-2 paragraphs of interpretation (Task 3.4) — written even if the
    graph-guided mode does *not* show savings.
- **IC-FR4 (Task F / ADR-006)**: a second `compare`-family function
  aggregates `InstrumentationLog`s from 5 graph-guided runs (one per
  BugsInPy HTTPie bug) into `reports/multi_bug_summary.md`
  (`docs/PLAN.md` 6.5): one row per bug
  (`bug_id | bug_summary | root_cause_found | tokens_used | llm_calls |
  files_read | iterations`) plus a short generalization paragraph.
- **IC-FR5**: Token counts (`tokens_in`/`tokens_out`) must come from the LLM
  provider's reported usage (or a tokenizer matching the model in
  `config/agent.json`), not estimated by character count.

### Input / Output Contract

- **Input**: in-process calls from both agent workflows during a run;
  `reports/graph_guided_run.json` + `reports/naive_run.json` (and, for Task
  F, `reports/<run_id>.json` per bug) as input to `compare.py`.
- **Output**: `reports/<run_id>.json` (per run), `reports/token_comparison.md`
  + `reports/token_comparison.png` (Task E), `reports/multi_bug_summary.md`
  (Task F).

### Performance Metrics / Targets

- Logging overhead must be negligible (in-memory counters, single JSON
  write at `finalize()`); must not itself add measurable LLM calls.
- `compare.py` must run in well under a few seconds for 2 (Task E) or up to
  6 (Task E + Task F) report files.
- The comparison's *interpretive* success criterion (per `docs/PRD.md`
  Goals table) is that numbers are reported **honestly**, whichever
  direction they point.

## 3. Constraints, Limitations, Alternatives Considered

### Constraints

- Both agents (`docs/PRD_graph_guided_agent.md`,
  `docs/PRD_naive_baseline_agent.md`) must call the *same*
  `instrumentation` functions — no separate ad-hoc counters per agent
  (ADR-004).
- `InstrumentationLog` schema (`docs/PLAN.md` 6.2) is fixed and shared by
  Task E and Task F outputs; `multi_bug_summary.md` rows are a thin
  projection of the same fields plus `bug_id`/`bug_summary`.
- `reports/` is the only output location for these artifacts (NFR-aligned
  with the project's directory layout); no writes to `data/httpie`.
- Chart generation (`token_comparison.png`) must not require any
  GUI/display — must run headless (e.g., a non-interactive matplotlib
  backend).

### Alternatives Considered

- **Per-agent ad-hoc counters** (each agent tracks its own metrics
  independently): rejected per ADR-004 — risk of inconsistent definitions
  (e.g., one agent counting a "re-read" of the same file twice, the other
  not) would invalidate the comparison.
- **Estimating tokens via `len(text) / 4`**: rejected as the primary
  method — inaccurate across models; real provider usage figures (or a
  matching tokenizer) are required for a credible Task E result. A
  character-based estimate may be used only as a documented fallback if
  usage data is unavailable.
- **Single combined report for Task E and Task F**: rejected — keeping
  `token_comparison.md` (2-row, Bug #3 only) separate from
  `multi_bug_summary.md` (5-row, all bugs) keeps the primary
  graph-vs-naive comparison uncluttered, per ADR-006.

## 4. Success Criteria & Test Scenarios

### Success Criteria

- After running both agents on Bug #3, `reports/graph_guided_run.json` and
  `reports/naive_run.json` both validate against the `InstrumentationLog`
  schema.
- `graphify_agent compare` produces `reports/token_comparison.md` with the
  required table columns, an embedded/linked chart image, and at least one
  paragraph of interpretation.
- (Task F) after 5 graph-guided runs (bugs 1-5),
  `reports/multi_bug_summary.md` contains exactly 5 data rows plus a
  generalization paragraph.
- Unit tests for `instrumentation.py` and `compare.py` reach >=85% coverage
  (NFR3).

### Test Scenarios

1. **Counter accuracy**: call `log_llm_call` twice (10/20 and 5/15 tokens),
   `log_file_read` once, `log_iteration` three times, then `finalize(...,
   root_cause_found=True)`; assert `tokens_used == 50`, `llm_calls == 2`,
   `files_read == 1`, `iterations == 3`.
2. **Report file written**: after `finalize("run_x", "graph_guided", True)`,
   assert `reports/run_x.json` exists and matches the `InstrumentationLog`
   schema.
3. **Compare table generation**: given two fixture `InstrumentationLog`
   JSON files (graph-guided cheaper than naive), assert
   `token_comparison.md` contains a table row for each mode with the
   correct values, in the documented column order.
4. **Honest negative result**: given fixtures where naive mode happens to
   use *fewer* tokens than graph-guided, assert `compare.py` still produces
   a valid table (no special-casing/hiding of the result) and that the
   interpretation paragraph is non-empty.
5. **Multi-bug summary (Task F)**: given 5 fixture `InstrumentationLog`
   files (one per bug, 2 with `root_cause_found: false`), assert
   `multi_bug_summary.md` has exactly 5 rows and the generalization
   paragraph mentions the number of bugs successfully diagnosed (e.g.,
   "3 of 5").
6. **Headless chart generation**: `compare.py` runs successfully in an
   environment without a display (e.g., `MPLBACKEND=Agg`) and produces
   `reports/token_comparison.png`.
