from graphify_agent.services.grphify_report import build_report


def _sample_graph() -> dict:
    return {
        "nodes": [
            {"id": "pkg/a.py", "type": "module", "file": "pkg/a.py", "lines": [1, 5],
             "metrics": {"in_degree": 0, "out_degree": 1}},
            {"id": "pkg/a.py::Foo", "type": "class", "file": "pkg/a.py", "lines": [3, 5],
             "metrics": {"in_degree": 1, "out_degree": 0}},
        ],
        "edges": [
            {"source": "pkg/a.py", "target": "pkg/a.py::Foo", "type": "defines"},
        ],
    }


def test_build_report_contains_summary_and_files() -> None:
    report = build_report(_sample_graph(), title="Test Report")

    assert report.startswith("# Test Report")
    assert "Total nodes: 2" in report
    assert "Total edges: 1" in report
    assert "module: 1" in report
    assert "class: 1" in report
    assert "defines: 1" in report
    assert "`pkg/a.py`" in report


def test_build_report_lists_hub_nodes() -> None:
    report = build_report(_sample_graph())

    assert "pkg/a.py::Foo" in report
    assert "pkg/a.py" in report
