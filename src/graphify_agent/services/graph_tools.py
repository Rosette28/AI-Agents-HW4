```python
from __future__ import annotations

import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Node:
    id: str
    type: str
    file: str
    lines: list[int]
    metrics: dict


@dataclass
class Graph:
    nodes: dict[str, Node]
    outgoing: dict[str, list[str]]
    incoming: dict[str, list[str]]


def load_graph(path: Path) -> Graph:
    data = json.loads(path.read_text(encoding="utf-8"))

    if "nodes" not in data:
        raise ValueError("graph.json missing 'nodes'")

    if "edges" not in data:
        raise ValueError("graph.json missing 'edges'")

    nodes = {}

    for item in data["nodes"]:
        nodes[item["id"]] = Node(
            id=item["id"],
            type=item["type"],
            file=item["file"],
            lines=item["lines"],
            metrics=item.get("metrics", {}),
        )

    outgoing = {}
    incoming = {}

    for edge in data["edges"]:
        source = edge["source"]
        target = edge["target"]

        outgoing.setdefault(source, []).append(target)
        incoming.setdefault(target, []).append(source)

    return Graph(
        nodes=nodes,
        outgoing=outgoing,
        incoming=incoming,
    )


def get_node(graph: Graph, node_id: str) -> Node | None:
    return graph.nodes.get(node_id)


def get_neighbors(
    graph: Graph,
    node_id: str,
    depth: int = 1,
) -> list[Node]:

    visited = {node_id}
    queue = deque([(node_id, 0)])

    while queue:
        current, level = queue.popleft()

        if level >= depth:
            continue

        neighbors = (
            graph.outgoing.get(current, [])
            + graph.incoming.get(current, [])
        )

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, level + 1))

    visited.remove(node_id)

    return [
        graph.nodes[node]
        for node in visited
        if node in graph.nodes
    ]


def search_nodes(
    graph: Graph,
    query: str,
) -> list[Node]:

    query = query.lower()

    matches = []

    for node in graph.nodes.values():

        haystack = " ".join(
            [
                node.id,
                node.file,
            ]
        ).lower()

        position = haystack.find(query)

        if position >= 0:
            matches.append((position, node))

    matches.sort(key=lambda item: item[0])

    return [node for _, node in matches]
```
