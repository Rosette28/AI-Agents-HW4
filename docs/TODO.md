# TODO

## Phase 1 — Setup & Decisions
- [x] uv project initialized (`pyproject.toml`, `uv.lock`, `.python-version`)
- [x] Repo + bug chosen: HTTPie (BugsInPy `projects/httpie`), Bug #3
- [x] README justification written
- [x] Target code cloned into `data/httpie/` at buggy commit `8c33e5e3d31d3cd6476c4d9bc963a4c529f883d2`
- [x] Separate `.venv` (Python 3.8) created in `data/httpie/` with bug-3 pinned dependencies + `setuptools`
- [ ] Resolve test discovery: BugsInPy's `run_test.sh` references
      `tests/test_sessions.py::TestSession::test_download_in_session`, which
      does not exist at this commit (likely a BugsInPy metadata mismatch for
      this project version). Need to identify the correct test that exercises
      `Session.update_headers` (the `value.decode('utf8')` on `None` bug in
      `httpie/sessions.py`).
- [ ] `tests/test_sessions.py::TestSession::test_session_ignored_header_prefixes`
      currently fails with `requests.exceptions.InvalidHeader` — appears
      unrelated to Bug #3 (likely an env/library-version issue); investigate.
- [ ] Create skeleton docs: `docs/PRD.md`, `docs/PLAN.md`
- [ ] Run Grphify on `data/httpie/` -> `artifacts/graph.json`, `artifacts/GRAPH_REPORT.md`
- [ ] Build Obsidian vault: `obsidian/index.md`, `obsidian/hot.md`
- [ ] Take "before" screenshots of the graph view
