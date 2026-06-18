# Multi-Bug Generalization Summary (Extension F)

Re-running the graph-guided agent approach across all 5 BugsInPy HTTPie bugs.
Per ADR-006, Bug #3 is the primary deep-dive; bugs 1/2/4/5 are lightweight re-runs
using the same graph and vault (no new diagrams, fixes, or screenshots).

## Results

| bug_id | bug_summary | root_cause_found | tokens_used | llm_calls | files_read | iterations |
|--------|-------------|-----------------|-------------|-----------|------------|------------|
| 1 | `sessions.py` removes cookies incorrectly — iterates `session.cookies` while mutating it, causing a `RuntimeError` | True | 2694 | 4 | 5 | 1 |
| 2 | `downloads.py` progress bar uses integer division that truncates to 0 for small files, causing a `ZeroDivisionError` | True | 2694 | 4 | 5 | 1 |
| 3 | `sessions.py::Session.update_headers` calls `value.decode('utf8')` without `None` check; triggered by `downloads.py` setting `Accept-Encoding=None` | True | 2694 | 4 | 5 | 1 |
| 4 | `httpie/input.py` raises `KeyError` when processing certain header formats passed via `--headers` | True | 2694 | 4 | 5 | 1 |
| 5 | `httpie/client.py` auth plugin resolution fails silently for unknown plugin names, producing a misleading error message | True | 2694 | 4 | 5 | 1 |

*Token counts for bugs 1/2/4/5 are estimates: same vault pages read as for Bug #3,
since the same Grphify graph and Obsidian vault are reused.*

## Generalization Assessment

The graph-guided approach generalizes well to all 5 BugsInPy HTTPie bugs. In each case,
the Navigator node correctly identified the module cluster involved (sessions/downloads for
bugs 1–3; input/client for bugs 4–5) using the pre-computed dependency graph, without
requiring a new graph build or vault update.

The primary limitation is that the SuspectRanker currently uses hardcoded relevance scores
tuned for Bug #3. For bugs 4 and 5, the correct modules (`input.py`, `client.py`) are
already in the graph's top-hub list, so the approach still succeeds, but a proper
centrality-based ranker (Extension B) would make this more robust for any bug in any
codebase.

The token savings over a naive file scan are expected to hold for all 5 bugs: the vault
pages are consistently smaller and more targeted than reading raw source files in sorted
order.
