# PRD — Graph-Guided Agent (LangGraph Workflow)

Parent document: `docs/PRD.md`. Architecture: `docs/PLAN.md` Sections 1.3,
1.4, 2.1, ADR-002, ADR-003, ADR-006. Depends on
`docs/PRD_graph_tools.md` and feeds `docs/PRD_instrumentation_and_comparison.md`.

## 1. Description & Theoretical Background

The graph-guided agent is the core deliverable of Tasks C/D: a multi-step
**LangGraph state machine** that locates and explains a real bug
(`httpie/sessions.py::Session.update_headers`, Bug #3) by first consulting a
**persistent knowledge layer** (the codebase graph + Obsidian vault) and only
then reading source code — directly addressing the "Lost in the Middle" /
context-window-cost problem described in `docs/PRD.md` Section 2.

The workflow implements a **role-specialized pipeline** (a common
agentic-AI pattern: decompose a broad task into narrow roles, each with a
constrained tool set and prompt):

1. **Navigator** — orients itself using `obsidian/index.md` and
   `obsidian/hot.md` (pre-written human knowledge) plus
   `graph_tools.get_neighbors()` around the area flagged in `hot.md`.
   Produces a list of **candidate `SuspectNode`s**.
2. **SuspectRanker** — scores candidates using a simple **centrality +
   proximity heuristic**: nodes with higher `in_degree`/`out_degree` (per
   `graph.json` `metrics`) and graph-distance closeness to the failing
   test's call path are ranked higher. This is a lightweight analog of
   PageRank-style centrality, chosen for explainability over ML complexity.
3. **CodeReader** — a tool that is *only registered after* Navigator +
   SuspectRanker have produced `suspect_nodes` (ADR-003: "graph-first rule
   enforced via tool ordering"). Reads only the specific
   file/function range identified (e.g., `sessions.py` lines 95-112).
4. **Explainer** — synthesizes the snippet + graph context into a
   `final_report`: root cause, file/line, and a fix proposal.

The state object threaded through all nodes is `AgentState` (see
`docs/PLAN.md` 1.4: `bug_id`, `graph`, `visited_nodes`, `suspect_nodes`,
`snippets_read`, `iteration`, `max_iterations`, `final_report`).

## 2. Requirements, Input/Output, Performance Metrics

### Functional Requirements

- **GA-FR1**: Implement the four nodes (Navigator, SuspectRanker,
  CodeReader, Explainer) as LangGraph nodes operating on `AgentState`.
- **GA-FR2**: Wire edges so that `code_reader` cannot execute before
  `navigator` and `suspect_ranker` have run at least once and populated
  `suspect_nodes` (ADR-003) — enforced structurally, not just via prompt.
- **GA-FR3**: Enforce `max_iterations` from `config/agent.json`
  (`config.max_iterations`, default 6, FR7) — the graph must terminate
  (with or without `final_report`) once `iteration >= max_iterations`.
- **GA-FR4**: Every node call must invoke `instrumentation.log_iteration()`
  and, for LLM-backed nodes, `instrumentation.log_llm_call()`; CodeReader
  must call `instrumentation.log_file_read()` for each snippet fetched.
- **GA-FR5**: On success, write `reports/graph_guided_run.json`
  (`InstrumentationLog`, `docs/PLAN.md` 6.2) with
  `root_cause_found: true` and `root_cause` naming
  `httpie/sessions.py::Session.update_headers` (line ~104).
- **GA-FR6 (Task F / ADR-006)**: The same workflow must be parameterizable
  by `--bug <1-5>` so it can be re-run against each of the 5 BugsInPy
  HTTPie bugs for `reports/multi_bug_summary.md`, without requiring
  per-bug vault pages.

### Input / Output Contract

- **Input**: `config/agent.json` (model, `max_iterations`, `graph_path`,
  `vault_path`), `artifacts/graph.json`, `obsidian/index.md`,
  `obsidian/hot.md` (or per-bug equivalent for Task F), read access to
  `data/httpie` source files via `graph_tools`/`vault_io`/`code_reader`.
- **Output**: `reports/graph_guided_run.json` (Task C/D, Bug #3) and, for
  Task F, one `InstrumentationLog`-shaped row per bug feeding
  `reports/multi_bug_summary.md`.

### Performance Metrics / Targets

- **Primary correctness metric**: `root_cause_found: true` and
  `root_cause` references `sessions.py` / `update_headers` for Bug #3.
- **Efficiency metrics** (compared against the naive baseline in
  `docs/PRD_instrumentation_and_comparison.md`): `tokens_used`,
  `llm_calls`, `files_read`, `iterations` — target is fewer files read and
  lower (or comparable) tokens than the naive mode, since the agent reads
  at most 1-2 targeted snippets vs. whole files.
- **Bound**: must always terminate within `max_iterations` (default 6) —
  no unbounded loops (FR7, NFR4).

## 3. Constraints, Limitations, Alternatives Considered

### Constraints

- LangGraph only (ADR-002) — chosen over CrewAI for explicit step control
  under a limited free-tier LLM account.
- `code_reader` may only read files from `data/httpie` (never the main
  project source) and only the specific ranges identified by
  `suspect_nodes` — not whole files (keeps the comparison meaningful).
- Must not mutate `data/httpie` source during Tasks C/D (the fix is a
  separate, later step — Task 3.5).
- For Task F (ADR-006), no new vault pages/diagrams are required per bug;
  the agent must still work with at least `obsidian/index.md` (general
  system map) even if a bug-specific `hot.md` doesn't exist for bugs 1-5.

### Alternatives Considered

- **CrewAI multi-agent framework**: rejected per ADR-002 — less precise
  control over iteration limits and instrumentation hooks.
- **Single monolithic "find the bug" prompt** (no role decomposition):
  rejected — would not demonstrate the graph-first methodology required by
  Task D, and would be harder to instrument per-step.
- **SuspectRanker using a learned/ML ranking model**: rejected — a simple
  centrality + proximity heuristic is explainable, requires no training
  data, and is sufficient at HTTPie's scale; documented as a possible
  future extension (4.2) rather than core scope.

## 4. Success Criteria & Test Scenarios

### Success Criteria

- Running `graphify_agent agent --mode graph_guided --bug 3` produces
  `reports/graph_guided_run.json` with `root_cause_found: true` and
  `root_cause` containing `"sessions.py"` and `"update_headers"`.
- The run uses `iterations <= max_iterations` and `files_read <= 2`.
- `code_reader` is never invoked before `suspect_nodes` is non-empty
  (verifiable from `visited_nodes`/log ordering).
- Unit tests cover each node's transition logic with >=85% coverage
  (NFR3); integration test runs the full graph against a stubbed/mocked
  LLM.
- (Task F) `graphify_agent agent --mode graph_guided --bug <1..5>` runs to
  completion (success or `max_iterations` reached) for all 5 bugs, each
  producing a row in `reports/multi_bug_summary.md`.

### Test Scenarios

1. **Happy path (Bug #3)**: Navigator finds `sessions.py` suspects from
   `hot.md`/graph neighbors -> SuspectRanker ranks `update_headers` highest
   -> CodeReader reads lines 95-112 -> Explainer reports the `None`-check
   bug. Assert `root_cause_found is True`.
2. **Tool-ordering enforcement**: directly invoke the graph with an empty
   `suspect_nodes` and assert `code_reader` is unreachable / raises.
3. **Max-iterations stop**: configure `max_iterations=1` and a Navigator
   that never produces usable suspects; assert the graph terminates after 1
   iteration with `final_report is None` and `root_cause_found: false`,
   without raising.
4. **Instrumentation completeness**: after a run, assert
   `reports/graph_guided_run.json` contains all `InstrumentationLog` fields
   (`tokens_used`, `llm_calls`, `files_read`, `iterations`,
   `root_cause_found`).
5. **Multi-bug smoke test (Task F)**: run with `--bug 1` through `--bug 5`
   against stubbed graphs/vault content; assert each run produces a valid
   `InstrumentationLog`-shaped result (success or graceful
   max-iterations stop), feeding `reports/multi_bug_summary.md`.
