# httpie/client.py

## Role

Builds the `requests` keyword arguments from parsed CLI args
(`get_requests_kwargs`) and sends the request (`get_response`). Bridges the
CLI/input layer to [[httpie.sessions]] (`get_response` calls
`session.update_headers`) and to [[httpie.models]] for response wrapping.

**Navigation:** [[index]] | [[hot]]

## Top-Level Functions

- `dump_request`
- `encode_headers`
- `get_default_headers`
- `get_requests_kwargs`
- `get_requests_session`
- `get_response`

## Imports

- [[httpie.compat]]

## Imported By

- [[httpie.core]]
- [[httpie.sessions]]
