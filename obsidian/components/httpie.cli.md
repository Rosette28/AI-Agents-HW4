# httpie/cli.py

## Role

Sets up the CLI argument parser and help formatting (`HTTPieHelpFormatter`).
Entry point for argument parsing - hands off to [[httpie.input]] for the
actual `HTTPieArgumentParser`/request-item parsing logic.

**Navigation:** [[index]] | [[hot]]

## Classes

- `HTTPieHelpFormatter`
  - `__init__`
  - `_split_lines`

## Imports

- [[httpie.input]]
- [[httpie.output.formatters.colors]]
- [[httpie.plugins.builtin]]
- [[httpie.sessions]]

## Imported By

- [[httpie.core]]
