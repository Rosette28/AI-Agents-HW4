# Index - HTTPie System Map

This vault documents `data/httpie` (HTTPie at the BugsInPy Bug #3 buggy
commit, `8c33e5e3...`) for EX04. Component pages under
`obsidian/components/` are auto-generated from `artifacts/graph.json` by
`graphify-agent vault` (see `docs/TODO.md` 1.13/1.14); this page and
[[hot]] are hand-written navigation aids on top of that graph.

For the active bug investigation, start at [[hot]].

## System Structure

HTTPie's `httpie/` package (25 modules, ~3,700 LOC) breaks down into the
following areas:

### Entry Points
- [[httpie.__main__]] - `python -m httpie` entry point
- [[httpie.core]] - `main()`, the top-level orchestrator (highest-degree hub
  in the graph - see `artifacts/GRAPH_REPORT.md`)

### CLI & Argument Parsing
- [[httpie.cli]] - argument parser setup, help formatting
  (`HTTPieHelpFormatter`)
- [[httpie.input]] - `HTTPieArgumentParser`, request-item parsing (one of
  the largest hubs by combined in/out degree)

### HTTP Client & Request/Response Flow
- [[httpie.client]] - builds `requests` kwargs, sends the request
- [[httpie.models]] - `HTTPRequest`/`HTTPResponse` wrapper models
- [[httpie.context]] - `Environment` (stdin/stdout/stderr, config dir)

### Sessions & Configuration
- [[httpie.sessions]] - **`Session.update_headers` is Bug #3's location**
  (see [[hot]])
- [[httpie.config]] - `Config`/`BaseConfigDict`, JSON config file handling
- [[httpie.compat]] - Python 2/3 compatibility shims

### Output Formatting
- [[httpie.output.streams]] - `RawStream`/`PrettyStream`/`BufferedPrettyStream`,
  `write()` (a major hub - 16 incoming edges)
- [[httpie.output.processing]] - output processor pipeline
- [[httpie.output.__init__]] - output package entry point
- [[httpie.output.formatters.__init__]] - formatter registry
- [[httpie.output.formatters.colors]] - `ColorFormatter` (Pygments-based)
- [[httpie.output.formatters.headers]] - header formatting
- [[httpie.output.formatters.json]] - JSON body formatting
- [[httpie.output.formatters.xml]] - XML body formatting

### Downloads
- [[httpie.downloads]] - `--download` mode, `ProgressReporterThread`
  (the path that triggers Bug #3 via `Accept-Encoding: None`)

### Plugins
- [[httpie.plugins.__init__]] - plugin package entry point
- [[httpie.plugins.base]] - `AuthPlugin`/`FormatterPlugin`/`ConverterPlugin`
  base classes
- [[httpie.plugins.builtin]] - built-in auth plugins (`HTTPBasicAuth`, etc.)
- [[httpie.plugins.manager]] - `PluginManager`

### Utilities
- [[httpie.utils]] - misc helpers
- [[httpie.__init__]] - package metadata (`__version__`, etc.)

## Primary Navigation Paths

These are the main ways to traverse the graph depending on what you're
investigating:

1. **CLI invocation -> response printed** (the "happy path"):
   [[httpie.__main__]] -> [[httpie.core]] (`main`) ->
   [[httpie.cli]] / [[httpie.input]] (parse args) ->
   [[httpie.client]] (build & send request) ->
   [[httpie.models]] (wrap response) ->
   [[httpie.output.streams]] / [[httpie.output.processing]] (format & print).

2. **Session-aware request** (Bug #3's path):
   [[httpie.client]] -> [[httpie.sessions]] (`get_response`,
   `Session.update_headers`) -> [[httpie.config]] (load/save session JSON).

3. **Download mode** (triggers Bug #3):
   [[httpie.cli]] / [[httpie.input]] (`--download` flag) ->
   [[httpie.downloads]] (sets `Accept-Encoding: None`) ->
   [[httpie.sessions]] (`update_headers` crashes on `None.decode`).

4. **Output formatting**:
   [[httpie.output.processing]] -> [[httpie.output.formatters.__init__]] ->
   one of [[httpie.output.formatters.colors]] /
   [[httpie.output.formatters.headers]] /
   [[httpie.output.formatters.json]] / [[httpie.output.formatters.xml]].

5. **Plugin resolution** (auth, formatters, converters):
   [[httpie.plugins.manager]] -> [[httpie.plugins.base]] /
   [[httpie.plugins.builtin]].

## Reference Artifacts

- `artifacts/graph.json` - full node/edge graph (machine-readable)
- `artifacts/GRAPH_REPORT.md` - summary stats and top hub nodes
- `obsidian/components/*.md` - one auto-generated page per module
