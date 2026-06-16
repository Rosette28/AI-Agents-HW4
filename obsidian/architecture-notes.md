# Architecture Notes — HTTPie Reverse Engineering

**Navigation:** [[index]] | [[hot]]

---

## 1. Macro Pass: Clusters, Hubs, and Bridges

The Grphify graph contains **225 nodes** and **445 edges** across 25 source files
(modules, classes, top-level functions).

### Top Hub Nodes (by total degree)

| Node | In-degree | Out-degree | Role |
|------|-----------|------------|------|
| `httpie/core.py::main` | ~5 | 21 | Primary orchestrator |
| `httpie/output/streams.py::write` | 16 | ~3 | Output sink |
| `httpie/input.py::HTTPieArgumentParser` | ~8 | ~10 | CLI parsing hub |
| `httpie/sessions.py::Session` | ~6 | ~8 | Session state hub |
| `httpie/plugins/manager.py::PluginManager` | ~7 | ~6 | Plugin registry |

### Identified Clusters

- **CLI / Input cluster**: `cli.py` → `input.py` → `HTTPieArgumentParser`; receives user args and transforms them into request objects.
- **Client / Session cluster**: `client.py::get_response` ↔ `sessions.py::Session`; manages HTTP execution and persistent state.
- **Output cluster**: `output/streams.py`, `output/processing.py`, `output/formatters/`; consumes `models.py` objects and writes to stdout.
- **Plugin cluster**: `plugins/manager.py`, `plugins/base.py`, `plugins/builtin/`; loaded by `core.py`.
- **Download cluster**: `downloads.py` + `models.py`; sits between the client layer and the output layer.

### Key Bridge Nodes

- `core.py::main` — bridges every cluster (CLI, Client, Downloads, Output, Plugins).
- `client.py::get_response` — bridges the input/session/download layers.
- `models.py` — bridges client output to the output-formatting cluster (imported by both `downloads.py` and `output/streams.py`).

---

## 2. Sessions Community Investigation

Focus: the sub-graph surrounding [[httpie.sessions]].

### Direct Neighbors

**Imports (outgoing):**
- [[httpie.client]] — `sessions.py` calls `client.get_response()` to execute session-aware requests
- [[httpie.compat]] — Python 2/3 compatibility shims
- [[httpie.config]] — reads/writes session JSON files from disk

**Imported By (incoming):**
- [[httpie.cli]] — CLI layer passes `--session` argument down
- [[httpie.input]] — input processing layer references `SessionOrPath` type

### Execution Path for Bug #3

```
cli.py (--session + --download flags)
  └─► core.py::main
        └─► downloads.py::Download.pre_request()   ← sets Accept-Encoding=None
              └─► client.py::get_response()
                    └─► Session.update_headers()    ← crashes on None.decode('utf8')
```

### Why This Sub-Graph Is Interesting

`sessions.py` acts as a **state persistence layer** injected into the HTTP client
pipeline. It's not a pure utility — it mutates request headers in-place, making it
a stateful participant in the request lifecycle. This is why a side-effect from
`downloads.py` (setting a header to `None`) can reach `sessions.py` at all:
both modules interact with the same mutable header dict passed through
`client.get_response()`.

The graph makes this path visible: `downloads.py` and `sessions.py` have no
direct import relationship, but they are connected via `client.py` — the bridge
node that makes Bug #3 possible.

---

## 3. Anomalies: God Nodes, Mixed Responsibilities, Orphans

### God Node: `httpie/core.py::main`

- **21 outgoing edges** — highest in the entire graph.
- Coordinates: CLI argument parsing, HTTP client, downloads, output streams, plugin loading, context management.
- Violation: a single function that knows about every subsystem. Any change to any subsystem potentially requires touching `core.py`.
- Mitigation present: each subsystem is well-encapsulated (separate modules); `main` is primarily a composition root, not a logic holder. Acceptable for a CLI tool, but still a single point of coupling.

### Mixed Responsibilities: `httpie/sessions.py::Session`

`Session` handles four distinct concerns in one class:
1. **Persistence** — reading/writing JSON files from disk (`_get_path`, `__init__`)
2. **Header management** — `update_headers` (site of Bug #3)
3. **Auth management** — `auth` property
4. **Cookie management** — `cookies` property

The bug lives precisely in the header-management responsibility, which mixes
byte-decoding logic with header-merging logic without input validation.

### Orphan Candidates

Running `search_nodes(graph, "compat")` shows `httpie.compat` has **0 incoming
edges from non-standard modules** — it is used only via import, never called
directly, and has no callers in the call-edge layer. It is effectively a utility
shim module with no graph centrality.

Similarly, `httpie.__main__` has 1 outgoing edge (`core.py`) and 0 incoming edges
from other application modules — it is the true entry point, with no upstream
callers in the application graph.

---

## See Also

- [[hot]] — Bug #3 full investigation brief
- [[index]] — System structure overview
- [[httpie.sessions]] — Sessions module component page
- [[httpie.client]] — Client module component page
- [[httpie.downloads]] — Downloads module component page
- `artifacts/GRAPH_REPORT.md` — full hub-node table and edge type counts
