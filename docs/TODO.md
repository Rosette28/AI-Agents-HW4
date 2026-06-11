# TODO — Task Tracking

Status legend: `Not Started` / `In Progress` / `Done`
Owners: **A** = Partner A (Rosette), **B** = Partner B — reassign as needed.
Priorities: **P0** (blocking/critical), **P1** (required for grading), **P2** (nice-to-have / extension).

---

## Phase 1 — Setup & Decisions, Graph & Knowledge Base

| ID | Task | Priority | Status | Owner | Definition of Done |
|---|---|---|---|---|---|
| 1.1 | Create GitHub repo with recommended structure | P0 | Done | A | `AI-Agents-HW4` repo exists locally with `src/`, `tests/`, `docs/`, `obsidian/`, `artifacts/`, `reports/`, `data/`, `config/`, `results/`, `assets/`, `notebooks/` |
| 1.2 | `uv init` + `pyproject.toml` + `uv.lock` | P0 | Done | A | `uv run python -c "print('hello')"` succeeds; `uv.lock` committed |
| 1.3 | `.gitignore`, `.env-example` | P0 | Done | A | Secrets/`.venv` ignored; `.env-example` lists required keys |
| 1.4 | Choose base repo + bug, write justification | P0 | Done | A | README "Chosen Repository & Bug Justification" section written (HTTPie / BugsInPy Bug #3) |
| 1.5 | Clone target code into `data/httpie` at buggy commit | P0 | Done | A | `data/httpie` checked out at `8c33e5e3...`; bug present in `sessions.py` |
| 1.6 | Set up isolated environment for `data/httpie` | P0 | Done | A | `data/httpie/.venv` (Py 3.8) created, bug-3 deps + `setuptools` installed |
| 1.7 | Resolve BugsInPy test mismatch for Bug #3 | P0 | Not Started | B | Correct test for `Session.update_headers` identified and confirmed to fail pre-fix |
| 1.8 | Investigate unrelated failing test (`test_session_ignored_header_prefixes`) | P2 | Not Started | B | Root cause documented in `docs/TODO.md` or fixed/explained in README as "known unrelated issue" |
| 1.9 | Write `docs/PRD.md` | P1 | Done | A | PRD covers overview, problem, audience, goals/KPIs, FR/NFR, user stories, assumptions, timeline |
| 1.10 | Write `docs/PLAN.md` | P1 | Done | A | PLAN covers C4 diagrams, UML, deployment diagram, ADRs, API docs, data schemas |
| 1.11 | Write `docs/TODO.md` (this file) | P1 | In Progress | A | All phases/tasks listed with priority, status, owner, DoD |
| 1.12 | Write empty `README.md` outline with all required headers | P1 | Done | A | All sections from "README Requirements" present as headers |
| 1.13 | Run Grphify on `data/httpie` | P0 | Not Started | B | `artifacts/graph.json` and `artifacts/GRAPH_REPORT.md` generated and openable |
| 1.14 | Open Grphify output in Obsidian; create vault skeleton | P0 | Not Started | B | `obsidian/` folder opens as an Obsidian vault |
| 1.15 | Write `obsidian/index.md` | P0 | Not Started | A | Describes HTTPie's system structure, main modules, and primary navigation paths, with links to component pages |
| 1.16 | Write `obsidian/hot.md` | P0 | Not Started | A | Documents Bug #3 suspects (`sessions.py::update_headers`), relevant test, knowns/unknowns |
| 1.17 | Add component pages for key modules (cli, client, sessions, downloads, models, output) | P1 | Not Started | B | One short Markdown page per key module, cross-linked to `index.md`/`hot.md` |
| 1.18 | Take "before" screenshots of Obsidian graph view | P1 | Not Started | B | Screenshots saved to `assets/` for later before/after comparison |

**Milestone M1:** Knowledge base ready — `graph.json`, `GRAPH_REPORT.md`, full Obsidian vault skeleton (`index.md`, `hot.md`, component pages), "before" screenshots, PRD/PLAN/TODO complete.

---

## Phase 2 — Reverse Engineering + AI Agent

| ID | Task | Priority | Status | Owner | Definition of Done |
|---|---|---|---|---|---|
| 2.1 | Macro pass: identify clusters/hubs/bridges in graph | P1 | Not Started | A | Findings noted in `obsidian/` (e.g., `architecture-notes.md`) |
| 2.2 | Drill into the community containing `sessions.py` | P1 | Not Started | A | Sub-graph/notes describing session/config/client interactions |
| 2.3 | Draw architectural block diagram (Mermaid) | P0 | Not Started | A | Diagram shows main blocks (CLI, client, sessions, downloads, output, plugins) + data flow; embedded in README |
| 2.4 | Draw OOP schema (Mermaid class diagram) | P0 | Not Started | A | Classes, inheritance, composition, usage relations for HTTPie core; embedded in README |
| 2.5 | Identify anomalies: God Nodes, mixed responsibilities, orphans | P1 | Not Started | A | Documented in `obsidian/` with at least 1-2 concrete examples |
| 2.6 | Write reverse-engineering draft section | P1 | Not Started | A | Draft answers "what wasn't obvious" + "most central components" research questions |
| 2.7 | Confirm framework choice (LangGraph) | P0 | Done (per ADR-002) | B | `docs/PLAN.md` ADR-002 documents decision and rationale |
| 2.8 | Implement `graph_tools.py` (load/query graph) | P0 | Not Started | B | `load_graph`, `get_node`, `get_neighbors`, `search_nodes` implemented + unit tests |
| 2.9 | Implement `vault_io.py` (read/write Obsidian pages) | P0 | Not Started | B | `read_page`, `write_page`, `list_pages` implemented + unit tests |
| 2.10 | Implement `instrumentation.py` | P0 | Not Started | B | `log_llm_call`, `log_file_read`, `log_iteration`, `finalize` implemented + unit tests |
| 2.11 | Implement Navigator agent node | P0 | Not Started | B | Reads `index.md`/`hot.md`/graph neighbors; produces candidate suspect nodes |
| 2.12 | Implement SuspectRanker agent node | P1 | Not Started | B | Scores candidates (centrality/proximity to failing test) |
| 2.13 | Implement CodeReader tool/node | P0 | Not Started | B | Fetches only specific file/function snippets from `data/httpie`, gated per ADR-003 |
| 2.14 | Implement Explainer agent node | P0 | Not Started | B | Produces root-cause hypothesis + fix proposal as `final_report` |
| 2.15 | Wire LangGraph workflow + max-iteration stop condition | P0 | Not Started | B | Graph runs end-to-end with `config/agent.json` `max_iterations` enforced |
| 2.16 | Run graph-guided agent on Bug #3; capture trace | P0 | Not Started | A+B | `reports/graph_guided_run.json` produced; agent names `sessions.py::update_headers` as root cause |

**Milestone M2:** Architecture diagrams complete; graph-guided agent implemented and successfully identifies Bug #3's root cause with logged instrumentation.

---

## Phase 3 — Baseline & Token Comparison + Fix & Before/After

| ID | Task | Priority | Status | Owner | Definition of Done |
|---|---|---|---|---|---|
| 3.1 | Implement naive baseline agent (`naive_baseline.py`) | P0 | Not Started | A | Reads raw `httpie/` files/chunks, same instrumentation hooks, same stop condition |
| 3.2 | Run naive baseline on Bug #3; capture trace | P0 | Not Started | A | `reports/naive_run.json` produced |
| 3.3 | Implement `compare.py` -> `reports/token_comparison.md` | P0 | Not Started | A | Table (mode, tokens, llm_calls, files_read, iterations, root_cause_found) + bar chart image |
| 3.4 | Write interpretation paragraphs for comparison | P1 | Not Started | A | 1-2 paragraphs explaining results (or why savings failed, if applicable) |
| 3.5 | Apply 1-line fix to `data/httpie/httpie/sessions.py` | P0 | Not Started | B | `if value is None: continue` guard added in `update_headers` |
| 3.6 | Verify fix via failing test | P0 | Not Started | B | Identified Bug #3 test fails before fix, passes after (Task 1.7 dependency) |
| 3.7 | Document problem/root cause/change/verification | P0 | Not Started | B | README "Bug Description, Root Cause & Fix" section complete |
| 3.8 | Re-run Grphify on fixed `data/httpie` | P1 | Not Started | B | Updated `artifacts/graph.json`/`GRAPH_REPORT.md` (post-fix) saved separately or diffed |
| 3.9 | Update Obsidian pages (`hot.md`, component pages) post-fix | P1 | Not Started | B | Vault reflects resolved bug, links/insights updated |
| 3.10 | Capture "after" screenshots | P1 | Not Started | B | Screenshots saved to `assets/`, paired with "before" for README |
| 3.11 | Write before/after comparison section | P1 | Not Started | A | README section shows knowledge-layer diffs (pages/nodes/links/insights) |

**Milestone M3:** Token comparison report complete; bug fixed and verified; before/after documentation (code + knowledge layer) complete.

---

## Phase 4 — Extensions + Documentation & Submission Polish

| ID | Task | Priority | Status | Owner | Definition of Done |
|---|---|---|---|---|---|
| 4.1 | Extension A — dynamic `hot.md` from `git diff` + `graph.json` | P2 | Not Started | A | Script regenerates `hot.md` suspects section from a git diff + graph query |
| 4.2 | Extension B — centrality ranking of suspect nodes | P2 | Not Started | A | `SuspectRanker` scores/ranks nodes by graph centrality, documented in Obsidian |
| 4.3 | Extension C — extra specialized agent / context-compaction step | P2 | Not Started | B | Additional LangGraph node implemented and described in README |
| 4.4 | Extension D — impact report (what breaks if `update_headers` changes) | P2 | Not Started | B | `reports/impact_report.md` generated from graph neighbors of the fixed function |
| 4.5 | Extension E — extra efficiency metric (cost $ or quality score) | P2 | Not Started | A | Additional column/metric added to `token_comparison.md` |
| 4.6 | Fill full README against checklist | P0 | Not Started | A+B | Every required section present, with embedded diagrams/screenshots/charts |
| 4.7 | Answer all 8 research questions explicitly | P0 | Not Started | A+B | Each question answered in README and/or linked Obsidian pages |
| 4.8 | Quality pass: ruff clean, files <=150 lines | P1 | Not Started | A+B | `uv run ruff check` passes; no file in `src/` exceeds 150 lines |
| 4.9 | Quality pass: tests pass, >=85% coverage | P1 | Not Started | A+B | `uv run pytest --cov` shows >=85% for `src/graphify_agent` |
| 4.10 | Add prompt log | P1 | Not Started | A+B | `docs/PROMPT_LOG.md` (or similar) documents key prompts used with the agent/LLM |
| 4.11 | Verify clean-clone run instructions | P0 | Not Started | A+B | Fresh `git clone` + `uv sync` + documented commands reproduce graph/agent/compare runs |
| 4.12 | Final repo review + tag release | P1 | Not Started | A | Structure consistent, commit history clean, release tag created |

**Milestone M4:** Submission-ready — full README with visuals, all research questions answered, quality gates passed, extensions documented, release tagged.

---

## Cross-Cutting / Always-On

| ID | Task | Priority | Status | Owner | Definition of Done |
|---|---|---|---|---|---|
| X.1 | Keep `docs/TODO.md` statuses up to date | P1 | In Progress | A+B | Status column reflects reality at each work session |
| X.2 | Keep config values in `config/*.json`, no hardcoding | P1 | Not Started | A+B | No literal limits/paths/model names hardcoded in `src/` |
| X.3 | Keep secrets out of git | P0 | Done (process) | A+B | Only `.env-example` committed; `.env` gitignored |
