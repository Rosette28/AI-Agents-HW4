# httpie/output/streams.py

## Classes

- `BaseStream`
  - `__init__`
  - `__iter__`
  - `get_headers`
  - `iter_body`
- `BinarySuppressedError`
- `BufferedPrettyStream`
  - `iter_body`
- `EncodedStream`
  - `__init__`
  - `iter_body`
- `PrettyStream`
  - `__init__`
  - `get_headers`
  - `iter_body`
  - `process_body`
- `RawStream`
  - `__init__`
  - `iter_body`

## Top-Level Functions

- `build_output_stream`
- `get_stream_type`
- `write`
- `write_with_colors_win_py3`

## Imports

- [[httpie.compat]]
- [[httpie.context]]
- [[httpie.input]]
- [[httpie.models]]
- [[httpie.output.processing]]

## Imported By

- [[httpie.core]]
- [[httpie.downloads]]
