# PRD — `graph_tools` Module (Graph Query Layer)

Parent document: `docs/PRD.md`. Architecture: `docs/PLAN.md` Sections 1.3, 1.4, 5.1, 6.1.

## 1. Description & Theoretical Background

`graph_tools.py` is the read-only query layer over the codebase graph
produced by Grphify (`artifacts/graph.json`). Conceptually, the graph models
the codebase as a **directed graph** `G = (V, E)`:

- **Nodes (`V`)**: files, classes, and functions/methods in `data/httpie`
  (e.g., `httpie/sessions.py::Session.update_headers`).
- **Edges (`E`)**: structural/usage relations between nodes — `calls`,
  `imports`, `defines`, `inherits` — as emitted by Grphify.

This module is the single point through which both the graph-guided agent
(`docs/PRD_graph_guided_agent.md`) and the naive baseline
(`docs/PRD_naive_baseline_agent.md`, for comparison only) can access graph
structure. It implements three classic graph-navigation primitives used in
codebase-comprehension tooling:

- **Lookup** (`get_node`): O(1) id -> node resolution, analogous to a hash
  index over a graph database.
- **Bounded BFS / neighborhood expansion** (`get_neighbors`): a
  breadth-first traversal up to `depth` hops, the standard way to find
  "what is structurally close to X" without loading the whole graph.
- **Lexical search** (`search_nodes`): substring/keyword matching over node
  `id`/`file`/`symbol` fields — a lightweight stand-in for a full search
  index, sufficient at HTTPie's scale (~5,600 LOC, ~45 files).

## 2. Requirements, Input/Output, Performance Metrics

### Functional Requirements

- **GT-FR1**: `load_graph(path: Path) -> Graph` — parses `artifacts/graph.json`
  into an in-memory `Graph` (nodes dict + adjacency list). Must validate the
  schema in `docs/PLAN.md` Section 6.1 and raise a clear error on malformed
  input.
- **GT-FR2**: `get_node(graph: Graph, node_id: str) -> Node | None` — exact
  id lookup.
- **GT-FR3**: `get_neighbors(graph: Graph, node_id: str, depth: int = 1) ->
  list[Node]` — BFS over both outgoing and incoming edges up to `depth`
  hops, deduplicated, excluding the start node itself.
- **GT-FR4**: `search_nodes(graph: Graph, query: str) -> list[Node]` —
  case-insensitive substring match over `id`, `file`, and `symbol`; returns
  results ordered by match position (prefix matches first).

### Input / Output Contract

- **Input**: `artifacts/graph.json` (schema per `docs/PLAN.md` 6.1: `nodes[]`
  with `id`, `type`, `file`, `lines`, `metrics.in_degree`/`out_degree`;
  `edges[]` with `source`, `target`, `type`).
- **Output**: in-memory `Graph`/`Node` objects (typed dataclasses), never
  re-serialized — `graph_tools` is read-only.

### Performance Metrics / Targets

- `load_graph` must complete in well under 1 second for the HTTPie graph
  (~45 files, low hundreds of nodes) — no specific SLA needed at this scale,
  but the implementation must be O(V+E) for loading, not O(V²).
- `get_neighbors(depth=2)` must return in well under 100ms for any node in
  the HTTPie graph.
- Memory: the entire graph must fit comfortably in memory as plain Python
  objects (no external graph DB needed at this scale).

## 3. Constraints, Limitations, Alternatives Considered

### Constraints

- Must consume Grphify's `graph.json` output as-is (ADR-005) — no separate
  graph representation is built or persisted.
- Read-only: `graph_tools` never writes back to `artifacts/`.
- Must work with the graph generated for the *buggy* commit of `data/httpie`
  (Section 1.5/1.13 of `docs/TODO.md`); a second graph (post-fix, Task 3.8)
  is loaded the same way but treated as a separate file.

### Alternatives Considered

- **Use a real graph database (e.g., NetworkX, Neo4j)**: rejected — at
  HTTPie's scale (~45 files), an in-memory dict/adjacency-list
  implementation is simpler, has zero extra dependencies, and meets all
  performance targets. NetworkX remains an option if `get_neighbors`
  centrality logic (used by `SuspectRanker`, see
  `docs/PRD_graph_guided_agent.md`) needs more advanced algorithms later.
- **Full-text/embedding search instead of substring search**: rejected for
  `search_nodes` — overkill for ~45 files and adds an LLM/embedding
  dependency to a module that should remain fast and offline.

## 4. Success Criteria & Test Scenarios

### Success Criteria

- `load_graph` successfully loads `artifacts/graph.json` for `data/httpie`
  and exposes at least the `httpie/sessions.py` nodes.
- `get_neighbors("httpie/sessions.py::Session.update_headers", depth=1)`
  returns the nodes that call or are called by `update_headers` (per the
  graph), enabling the Navigator agent to find `get_response` in
  `sessions.py` and downstream callers in `client.py`/`downloads.py`.
- `search_nodes("update_headers")` returns the `Session.update_headers`
  node.
- All functions covered by unit tests in `tests/unit/` with >=85% coverage
  (NFR3).

### Test Scenarios

1. **Load valid graph**: given a small fixture `graph.json` (2-3 nodes, 2
   edges), `load_graph` returns a `Graph` with matching node/edge counts.
2. **Load malformed graph**: given a `graph.json` missing the `edges` key,
   `load_graph` raises a descriptive `ValueError`.
3. **Node lookup hit/miss**: `get_node(graph, "exists")` returns the node;
   `get_node(graph, "missing")` returns `None`.
4. **Neighbor depth=1 vs depth=2**: on a fixture graph `A -> B -> C`,
   `get_neighbors(graph, "A", depth=1) == [B]` and
   `get_neighbors(graph, "A", depth=2) == [B, C]`.
5. **Search ordering**: `search_nodes(graph, "session")` ranks a node whose
   `id` starts with "session" above one where "session" appears mid-string.
6. **Real graph smoke test (integration)**: `load_graph("artifacts/graph.json")`
   on the actual generated HTTPie graph succeeds and contains a node for
   `httpie/sessions.py`.
