from graphify_agent.services.graph_tools import (
    Graph,
    Node,
    get_node,
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