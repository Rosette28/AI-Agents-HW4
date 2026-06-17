# httpie/sessions.py

## Role

**Bug #3 was here — now fixed.** `Session.update_headers` (lines ~95-112) merges
request headers into the persisted session. The bug (`value.decode('utf8')` without
a `None`-check) has been fixed with a 1-line guard (`if value is None: continue`).
Triggered when [[httpie.downloads]] sets `Accept-Encoding: None`. See [[hot]] for
the full investigation brief and fix details.

**Navigation:** [[index]] | [[hot]]

## Classes

- `Session`
  - `__init__`
  - `_get_path`
  - `auth`
  - `auth`
  - `cookies`
  - `cookies`
  - `headers`
  - `update_headers`

## Top-Level Functions

- `get_response`

## Imports

- [[httpie.client]]
- [[httpie.compat]]
- [[httpie.config]]

## Imported By

- [[httpie.cli]]
- [[httpie.input]]
