from pathlib import Path

from graphify_agent.services.grphify_builder import build_graph


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def test_build_graph_nodes_and_edges(tmp_path: Path) -> None:
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    _write(
        pkg / "a.py",
        "from .b import helper\n\n\nclass Foo:\n    def bar(self):\n        return helper()\n",
    )
    _write(pkg / "b.py", "def helper():\n    return 42\n")

    graph = build_graph(pkg)
    node_ids = {n["id"] for n in graph["nodes"]}

    assert "pkg/a.py" in node_ids
    assert "pkg/b.py" in node_ids
    assert "pkg/a.py::Foo" in node_ids
    assert "pkg/a.py::Foo.bar" in node_ids
    assert "pkg/b.py::helper" in node_ids


def test_build_graph_edge_types(tmp_path: Path) -> None:
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    _write(
        pkg / "a.py",
        "from .b import helper\n\n\ndef caller():\n    return helper()\n",
    )
    _write(pkg / "b.py", "def helper():\n    return 1\n")

    graph = build_graph(pkg)
    edge_types = {e["type"] for e in graph["edges"]}

    assert "defines" in edge_types
    assert "imports" in edge_types
    assert "calls" in edge_types

    calls = [e for e in graph["edges"] if e["type"] == "calls"]
    assert {"source": "pkg/a.py::caller", "target": "pkg/b.py::helper", "type": "calls"} in calls


def test_build_graph_degrees(tmp_path: Path) -> None:
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    _write(pkg / "a.py", "def caller():\n    return callee()\n\n\ndef callee():\n    return 1\n")

    graph = build_graph(pkg)
    by_id = {n["id"]: n for n in graph["nodes"]}

    assert by_id["pkg/a.py::callee"]["metrics"]["in_degree"] >= 1
    assert by_id["pkg/a.py::caller"]["metrics"]["out_degree"] >= 1
