# Hot - Bug #3 Investigation Focus

This page is the entry point for the Bug #3 investigation (Tasks C-E). The
graph-guided agent (`docs/PRD_graph_guided_agent.md`) is expected to read
this page (and [[index]]) before requesting any source code.

**Repository:** `data/httpie` (BugsInPy `projects/httpie`, bug 3)
**Buggy commit:** `8c33e5e3d31d3cd6476c4d9bc963a4c529f883d2`
**Fixed commit:** `589887939507ff26d36ec74bd2c045819cfa3d56`

## Primary Suspect

[[httpie.sessions]] -> `Session.update_headers` (lines ~95-112 of
`httpie/sessions.py`).

```python
def update_headers(self, request_headers):
    for name, value in request_headers.items():
        value = value.decode('utf8')   # <-- line 104: crashes if value is None
        if name == 'User-Agent' and value.startswith('HTTPie/'):
            continue
        for prefix in SESSION_IGNORED_HEADER_PREFIXES:
            if name.lower().startswith(prefix.lower()):
                break
        else:
            self['headers'][name] = value
```

**Symptom:** `AttributeError: 'NoneType' object has no attribute 'decode'`.

## How It's Triggered

[[httpie.downloads]] sets `request_headers['Accept-Encoding'] = None` to
disable gzip during `--download` mode (see [[index]] navigation path 3).
This `None` value flows into `Session.update_headers` via
`get_response()` -> `session.update_headers(kwargs['headers'])`, which
calls `.decode('utf8')` on it unconditionally.

## Relevant Test

`tests/test_sessions.py::TestSession::test_download_in_session`

- This test did **not exist** at the buggy commit - it was added together
  with the fix in the fixed commit. It was ported into the buggy checkout's
  `tests/test_sessions.py` (plus the `from tempfile import gettempdir`
  import) without applying the source fix - see `docs/TODO.md` task 1.7.
- **Confirmed to fail pre-fix** with the exact `AttributeError` above, at
  `httpie/sessions.py:104` inside `Session.update_headers`.
- Run via: `data/httpie/.venv/Scripts/python -m pytest tests/test_sessions.py::TestSession::test_download_in_session -q`
  (from `data/httpie/`).

## Fix Applied (Task 3.5 ✅)

```python
for name, value in request_headers.items():
    if value is None:
        continue  # guard: skip headers explicitly unset (e.g. Accept-Encoding)
    value = value.decode('utf8')
    ...
```

A `None`-check guard added before the `.decode('utf8')` call at line 104 of
`data/httpie/httpie/sessions.py`. **`test_download_in_session` now passes.**
See README "Bug Description, Root Cause & Fix" for the full verification record.

## Knowns

- Root cause is isolated to `Session.update_headers` in [[httpie.sessions]]
  (47 classes / 153 functions in the whole graph, but only this one method
  has the unguarded `.decode`).
- `Session` is also used by [[httpie.client]] (`get_response`) and is
  imported by [[httpie.cli]] and [[httpie.input]] (see "Imported By" on
  [[httpie.sessions]]).
- The bug only manifests when a request header value is explicitly `None`
  - currently only [[httpie.downloads]] does this (`Accept-Encoding`).

## Unknowns / Open Questions

- Whether other call sites could also pass `None`-valued headers into
  `update_headers` in the future (graph shows [[httpie.sessions]] is
  imported by [[httpie.cli]] and [[httpie.input]] as well as
  [[httpie.client]] - worth checking via `get_neighbors` in Task 2.8+).
- Whether the fix should also guard `Session.headers` reads elsewhere
  (out of scope per `docs/PRD.md`, but worth a one-line note in the final
  report - candidate for Extension D, "impact report").

## Known Unrelated Issue (Task 1.8 - documented, not fixed)

`tests/test_sessions.py::TestSession::test_session_ignored_header_prefixes`
also fails in this environment, **independently of Bug #3**:

- CLI argument `'Content-Type: text/plain'` is parsed with a leading space
  preserved (`args.headers['Content-Type'] == ' text/plain'`).
- `requests==2.23.0` (pinned by `bugs/3/requirements.txt`) raises
  `requests.exceptions.InvalidHeader` for header values with leading
  whitespace (`check_header_validity`).
- Verified to fail identically on **both** the buggy and fixed
  `sessions.py` -> unrelated to Bug #3, a pre-existing
  HTTPie/`requests`-version incompatibility. Excluded from this
  investigation's scope (see `docs/TODO.md` 1.8 and `docs/PRD.md`
  "Out of Scope").

## See Also

- [[index]] - full system map and navigation paths
- [[httpie.sessions]], [[httpie.downloads]], [[httpie.client]] - component
  pages for the modules involved
- `artifacts/graph.json` / `artifacts/GRAPH_REPORT.md` - full graph data
