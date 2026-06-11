# HTTPie (data/httpie) -- Grphify Graph Report

## Summary

- Total nodes: 225
  - class: 47
  - function: 153
  - module: 25
- Total edges: 445
  - calls: 201
  - defines: 202
  - imports: 42

## Files Analyzed

- `httpie/__init__.py`
- `httpie/__main__.py`
- `httpie/cli.py`
- `httpie/client.py`
- `httpie/compat.py`
- `httpie/config.py`
- `httpie/context.py`
- `httpie/core.py`
- `httpie/downloads.py`
- `httpie/input.py`
- `httpie/models.py`
- `httpie/output/__init__.py`
- `httpie/output/formatters/__init__.py`
- `httpie/output/formatters/colors.py`
- `httpie/output/formatters/headers.py`
- `httpie/output/formatters/json.py`
- `httpie/output/formatters/xml.py`
- `httpie/output/processing.py`
- `httpie/output/streams.py`
- `httpie/plugins/__init__.py`
- `httpie/plugins/base.py`
- `httpie/plugins/builtin.py`
- `httpie/plugins/manager.py`
- `httpie/sessions.py`
- `httpie/utils.py`

## Top Hub Nodes (in_degree + out_degree)

| Node | Type | In | Out |
|---|---|---|---|
| `httpie/core.py::main` | function | 1 | 21 |
| `httpie/input.py` | module | 2 | 16 |
| `httpie/output/streams.py` | module | 2 | 15 |
| `httpie/output/streams.py::write` | function | 16 | 0 |
| `httpie/input.py::HTTPieArgumentParser` | class | 1 | 13 |
| `httpie/output/streams.py::BufferedPrettyStream.iter_body` | function | 3 | 11 |
| `httpie/downloads.py` | module | 1 | 12 |
| `httpie/input.py::HTTPieArgumentParser.parse_args` | function | 2 | 10 |
| `httpie/output/streams.py::PrettyStream.iter_body` | function | 4 | 8 |
| `httpie/plugins/manager.py::PluginManager` | class | 1 | 11 |
