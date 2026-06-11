# httpie/output/streams.py

## Role

Output stream classes (`RawStream`, `PrettyStream`, `BufferedPrettyStream`,
`EncodedStream`) and `write()` - the most-called function in the graph (16
incoming edges, see `artifacts/GRAPH_REPORT.md`). Consumes
[[httpie.models]] request/response objects and [[httpie.output.processing]]
formatters; used by [[httpie.core]] and [[httpie.downloads]] to print/save
output.

**Navigation:** [[index]] | [[hot]]

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
