# httpie/models.py

## Role

Defines `HTTPMessage`/`HTTPRequest`/`HTTPResponse`, thin wrappers around
`requests` request/response objects exposing `headers`, `body`,
`iter_body`/`iter_lines`. Used by [[httpie.downloads]] and
[[httpie.output.streams]] to read response data for display/saving.

**Navigation:** [[index]] | [[hot]]

## Classes

- `HTTPMessage`
  - `__init__`
  - `body`
  - `content_type`
  - `encoding`
  - `headers`
  - `iter_body`
  - `iter_lines`
- `HTTPRequest`
  - `body`
  - `encoding`
  - `headers`
  - `iter_body`
  - `iter_lines`
- `HTTPResponse`
  - `body`
  - `encoding`
  - `headers`
  - `iter_body`
  - `iter_lines`

## Imports

- [[httpie.compat]]

## Imported By

- [[httpie.downloads]]
- [[httpie.output.streams]]
