# httpie/sessions.py

## Role

**Bug #3 lives here.** `Session.update_headers` (lines ~95-112) merges
request headers into the persisted session, calling `value.decode('utf8')`
without checking for `None`. Triggered when [[httpie.downloads]] sets
`Accept-Encoding: None`. See [[hot]] for the full investigation brief and
the relevant test.

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
