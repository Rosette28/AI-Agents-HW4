import pytest

from graphify_agent.config import PROJECT_ROOT
from graphify_agent.services.graph_tools import (
    Graph,
    Node,
    get_neighbors,
    get_node,
    load_graph,
    search_nodes,
)


def test_get_node_found():
    node = Node(
        id="session",
        type="module",
        file="session.py",
        lines=[1, 10],
        metrics={},
    )

    graph = Graph(
        nodes={"session": node},
        outgoing={},
        incoming={},
    )

    assert get_node(graph, "session") == node


def test_get_node_missing():
    graph = Graph(
        nodes={},
        outgoing={},
        incoming={},
    )

    assert get_node(graph, "missing") is None


def test_search_nodes():
    node = Node(
        id="httpie.sessions",
        type="module",
        file="sessions.py",
        lines=[1, 10],
        metrics={},
    )

    graph = Graph(
        nodes={"httpie.sessions": node},
        outgoing={},
        incoming={},
    )

    result = search_nodes(graph, "session")

    assert len(result) == 1
    assert result[0].id == "httpie.sessions"


def test_load_graph_real():
    graph = load_graph(PROJECT_ROOT / "artifacts" / "graph.json")
    assert len(graph.nodes) > 0
    assert len(graph.outgoing) > 0


def test_load_graph_missing_nodes(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"edges": []}', encoding="utf-8")
    with pytest.raises(ValueError, match="nodes"):
        load_graph(bad)


def test_load_graph_missing_edges(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"nodes": []}', encoding="utf-8")
    with pytest.raises(ValueError, match="edges"):
        load_graph(bad)


def test_get_neighbors_finds_adjacent():
    node_a = Node(id="a", type="module", file="a.py", lines=[1, 1], metrics={})
    node_b = Node(id="b", type="module", file="b.py", lines=[1, 1], metrics={})
    graph = Graph(
        nodes={"a": node_a, "b": node_b},
        outgoing={"a": ["b"]},
        incoming={"b": ["a"]},
    )
    neighbors = get_neighbors(graph, "a", depth=1)
    assert any(n.id == "b" for n in neighbors)


def test_get_neighbors_excludes_self():
    node_a = Node(id="a", type="module", file="a.py", lines=[1, 1], metrics={})
    graph = Graph(nodes={"a": node_a}, outgoing={}, incoming={})
    neighbors = get_neighbors(graph, "a", depth=1)
    assert not any(n.id == "a" for n in neighbors)