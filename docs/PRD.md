# Product Requirements Document (PRD)

## 1. Project Overview & Context

This project is the deliverable for **EX04 — Reverse Engineering, Debugging and Token-Efficient Agentic AI with Grphify and Obsidian**.

The product being built is a small **toolkit + AI agent** (`graphify_agent`) that:

1. Generates a graph representation (`graph.json`, `GRAPH_REPORT.md`) of an unfamiliar codebase using **Grphify**.
2. Organizes that knowledge into a navigable **Obsidian vault** (`index.md`, `hot.md`, component pages).
3. Runs a **graph-guided AI agent** (CrewAI or LangGraph) that uses the graph and vault first, and only then reads specific source files, to locate, explain, and help fix a real bug.
4. Compares this **graph-guided mode** against a **naive mode** (raw file dumping) on token usage, files read, and iteration count.

**Target codebase:** HTTPie via its BugsInPy entry (`data/httpie`), checked out at the buggy commit for **Bug #3**.

**Target bug:** `httpie/sessions.py::Session.update_headers` calls `value.decode('utf8')` without a `None` check, causing an `AttributeError` for sessions with explicitly-unset headers.

---

## 2. User Problem

The "user" of this product is a **developer dropped into an unfamiliar, medium-sized codebase** who needs to find and fix a specific bug without reading the whole project.

Today this means either:

- Reading files linearly until something looks relevant (slow, easy to miss cross-module dependencies, "Lost in the Middle" effect with large LLM contexts), or
- Pasting large chunks of the codebase into an LLM (expensive, noisy, and often exceeds useful context windows).

This project addresses that problem by building a **persistent knowledge layer** (graph + Obsidian vault) that lets a human or an AI agent navigate directly to the relevant area of the system before reading any code.

---

## 3. Audience

- **Primary:** The two students completing this assignment (developers and reviewers of their own work).
- **Secondary:** The course instructor/grader, evaluating the repository as an external reader via the README and Obsidian vault.
- **Tertiary (illustrative):** Any developer onboarding onto HTTPie (or a similarly sized OSS project) who wants a reusable graph-guided investigation workflow.

---

## 4. Goals & Success Metrics (KPIs)

| Goal | Metric / KPI | Acceptance Criterion |
|--------|--------|--------|
| Build a usable knowledge graph of HTTPie | `artifacts/graph.json` + `GRAPH_REPORT.md` produced | Files exist, cover `httpie/` package, openable in Obsidian |
| Build a navigable Obsidian vault | `obsidian/index.md`, `obsidian/hot.md`, component pages | All required pages present and cross-linked |
| Reverse-engineer the architecture | Block diagram + OOP schema | Both diagrams produced, embedded in README |
| Locate & explain Bug #3 via agent | Agent identifies `sessions.py::update_headers` as root cause | Agent's final report names the correct file/function/line |
| Fix the bug | Failing test passes after fix | Relevant `tests/test_sessions.py` test passes post-fix, fails pre-fix |
| Prove token savings | `reports/token_comparison.md` | Graph-guided mode shows fewer tokens, fewer files read, and/or fewer iterations than naive mode, with numbers reported even if the result is negative |
| Show the approach generalizes (Task F) | `reports/multi_bug_summary.md` | Graph-guided agent re-run on all 5 BugsInPy HTTPie bugs, with results summarized per bug |
| Code quality | Ruff clean, files ≤150 lines, tests for `src/` | `uv run ruff check` passes; `uv run pytest` passes for `tests/` |

---

## 5. Functional Requirements

### FR1 — Graph Generation
Run Grphify against `data/httpie` and persist output to `artifacts/`.

### FR2 — Obsidian Vault
Maintain:

- `obsidian/index.md` (system map)
- `obsidian/hot.md` (bug-focused context)
- Per-component pages

All pages must be cross-linked.

### FR3 — Graph-Reading Tools
Provide functions to:

- Load `graph.json`
- Query a node's neighbors
- Read a named Obsidian page

### FR4 — Graph-Guided Agent
Implement a CrewAI/LangGraph workflow with distinct roles (e.g., Navigator → Suspect Ranker → Code Reader → Explainer) that must consult the graph/vault before requesting code snippets.

### FR5 — Naive Baseline Agent
Implement an equivalent workflow that receives raw files or large chunks without graph guidance, using the same instrumentation.

### FR6 — Instrumentation
Both agents log:

- Token counts
- LLM call counts
- Files/units read
- Iteration counts

Outputs are stored in `reports/`.

### FR7 — Stop Condition
Agents must enforce a max-rounds limit to avoid unbounded loops.

### FR8 — Fix Application
Apply the real one-line fix to:

```python
data/httpie/httpie/sessions.py
```

and verify via the relevant test.

### FR9 — Before/After Artifacts
Re-run Grphify and update Obsidian pages after the fix. Capture:

- Before screenshots
- After screenshots
- Diff summary

### FR10 — Extensions (Task F)
Implement at least one original extension per task area (A–E), documented in Obsidian and README. The primary extension is **multi-bug generalization**: re-run the graph-guided agent built for Bug #3 against all 5 BugsInPy HTTPie bugs and summarize results in `reports/multi_bug_summary.md` (see ADR-006).

---

## 6. Non-Functional Requirements

### NFR1 — Reproducibility
`uv sync` plus documented commands must reproduce the environment from a clean clone (per course guidelines V3).

### NFR2 — Code Quality

- Source files ≤150 lines
- `ruff check` clean
- No hardcoded config values
- Configuration in `config/*.json`
- Secrets via `.env`
- `.env-example` provided

### NFR3 — Test Coverage

- ≥85% coverage for `src/graphify_agent`
- Mirrored `tests/unit` and `tests/integration` structure

### NFR4 — Cost/Efficiency

- Prefer LangGraph if working with limited free LLM accounts
- Cap LLM calls per run via configuration

### NFR5 — Isolation

The target codebase (`data/httpie`) and its dependencies/virtual environment must not pollute the main project's `uv` environment.

### NFR6 — Documentation

README and Obsidian vault must be understandable by an external reader with no prior context, including screenshots and diagrams.

---

## 7. User Stories / Use Cases

### Student Investigator

As a student investigator, I run Grphify on `data/httpie` so I get a `graph.json` I can explore in Obsidian before touching any source file.

### Student Investigator (Bug Analysis)

As a student investigator, I open `obsidian/hot.md` to see the suspects, relevant tests, and open questions for Bug #3 before running the agent.

### Graph-Guided Agent

As the graph-guided agent, I read:

- `index.md`
- `hot.md`
- `graph.json` neighbors of suspect nodes

and only request the specific function body in `sessions.py` once I have a concrete hypothesis.

### Naive Baseline Agent

As the naive baseline agent, I am given raw file contents (e.g., all of `httpie/`) and asked to find and explain the same bug, with the same instrumentation recording token and file usage.

### Grader / External Reader

As a grader or external reader, I open the README and can follow:

Repository choice → Architecture → Agent workflow → Bug → Fix → Before/After → Token comparison → Extensions

with diagrams and screenshots throughout.

---

## 8. Assumptions, Dependencies, Constraints, Out of Scope

### Assumptions

- HTTPie at the chosen buggy commit is a representative, sufficiently large codebase (~45 Python files, ~5,600 LOC) for graphing and architecture extraction.
- An LLM API key (Anthropic/OpenAI) is available for agent runs.
- If quota is limited, LangGraph is used to bound calls.

### Dependencies

- Grphify (graph generation tool)
- Obsidian (for viewing/editing the vault; vault files remain plain Markdown)
- CrewAI or LangGraph plus an LLM provider SDK
- BugsInPy metadata for HTTPie Bug #3 (buggy/fixed commit pair and test)

### Constraints

- Python 3.7/3.8 required to run HTTPie's BugsInPy test suites
- Separate `.venv` under `data/httpie`
- Main project targets Python 3.11+
- Environments must remain isolated
- Bug #3 is the single primary deep-dive bug for Tasks A-E (graph, vault,
  diagrams, agent run, fix, before/after, token comparison); the remaining 4
  BugsInPy HTTPie bugs are used only for the Task F multi-bug generalization
  extension (ADR-006), not for full per-bug deliverables

### Out of Scope

- Full per-bug deliverables (diagrams, vault pages, before/after
  screenshots, individual token comparisons) for HTTPie bugs other than
  Bug #3 — bugs 1, 2, 4, 5 are only used for the lightweight Task F
  multi-bug agent re-run (ADR-006)
- Fixing bugs 1, 2, 4, 5 in `data/httpie` (the agent investigates them but
  no source fix is applied/verified for them)
- Production deployment of the agent or graph tooling
- Full CI/CD pipeline for HTTPie itself
- Supporting codebases other than HTTPie within this submission

---

## 9. Timeline & Milestones

Aligned with `docs/PLAN.md` phases.

| Phase | Milestone | Key Deliverables |
|--------|--------|--------|
| Phase 1 — Setup & Knowledge Base | Repo/bug chosen, environment setup, Grphify run, vault skeleton | `graph.json`, `GRAPH_REPORT.md`, `index.md`, `hot.md`, before screenshots |
| Phase 2 — Reverse Engineering & Agent | Architecture diagrams, agent workflow implemented and run | Block diagram, OOP schema, agent trace, root-cause explanation |
| Phase 3 — Baseline & Fix | Naive baseline run, comparison report, fix applied and verified | `reports/token_comparison.md`, fixed code, passing test, after screenshots |
| Phase 4 — Extensions & Polish | Extensions implemented, README/docs complete, quality pass | Full README, all research questions answered, Ruff/tests clean, tagged release |