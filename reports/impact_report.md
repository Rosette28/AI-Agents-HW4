# Impact Report — `Session.update_headers` (Extension D)

What could break if `Session.update_headers` in `httpie/sessions.py` changes.

## Graph Neighbors of `sessions.py::Session::update_headers`

From `artifacts/graph.json` (query: `get_neighbors(graph, "httpie/sessions.py::Session::update_headers", depth=2)`):

**Direct callers (depth 1):**
- `httpie/client.py::get_response` — calls `session.update_headers(kwargs['headers'])`

**Indirect callers (depth 2):**
- `httpie/core.py::main` — calls `client.get_response()`, propagating download headers
- `httpie/downloads.py::Download::pre_request` — sets `Accept-Encoding=None` before
  the request, which flows into `update_headers` via `client.get_response()`

## Potential Consequences of Future Changes

| Change | Impact |
|--------|--------|
| Remove the `None` guard (revert fix) | Bug #3 reintroduced: `AttributeError` on `--session --download` |
| Change the decode encoding from `'utf8'` | Sessions with non-UTF-8 header values would break silently |
| Change the `SESSION_IGNORED_HEADER_PREFIXES` logic | Custom session headers might leak into persisted state |
| Rename or remove `update_headers` | `client.py::get_response` would raise `AttributeError` at runtime |
| Make `update_headers` raise on `None` instead of skip | Stricter validation — callers setting `None` headers would fail fast |

## Modules That Would Need Updates If Signature Changes

- `httpie/client.py` — only caller; must be updated if parameter name/type changes
- `tests/test_sessions.py` — `test_download_in_session` directly exercises this path
- Any future code that constructs request headers with `None` values

## Summary

The impact radius is **small but critical**: only `client.py` directly calls
`update_headers`, but the bug path (`downloads → client → sessions`) shows that
indirect side-effects can reach this function from seemingly unrelated subsystems.
The `None` guard added in Task 3.5 is the minimal-impact fix; any deeper refactor
of `update_headers` should be paired with a run of `test_download_in_session`
to catch regressions.
