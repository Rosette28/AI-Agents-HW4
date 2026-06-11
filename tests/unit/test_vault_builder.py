from graphify_agent.services.vault_builder import build_vault_pages, page_name


def _sample_graph() -> dict:
    return {
        "nodes": [
            {"id": "pkg/a.py", "type": "module", "file": "pkg/a.py", "lines": [1, 5],
             "metrics": {"in_degree": 0, "out_degree": 1}},
            {"id": "pkg/b.py", "type": "module", "file": "pkg/b.py", "lines": [1, 5],
             "metrics": {"in_degree": 1, "out_degree": 0}},
            {"id": "pkg/a.py::Foo", "type": "class", "file": "pkg/a.py", "lines": [3, 5],
             "metrics": {"in_degree": 0, "out_degree": 0}},
            {"id": "pkg/a.py::Foo.bar", "type": "function", "file": "pkg/a.py", "lines": [4, 5],
             "metrics": {"in_degree": 0, "out_degree": 0}},
            {"id": "pkg/b.py::helper", "type": "function", "file": "pkg/b.py", "lines": [1, 2],
             "metrics": {"in_degree": 1, "out_degree": 0}},
        ],
        "edges": [
            {"source": "pkg/a.py", "target": "pkg/a.py::Foo", "type": "defines"},
            {"source": "pkg/a.py::Foo", "target": "pkg/a.py::Foo.bar", "type": "defines"},
            {"source": "pkg/b.py", "target": "pkg/b.py::helper", "type": "defines"},
            {"source": "pkg/a.py", "target": "pkg/b.py", "type": "imports"},
        ],
    }


def test_page_name() -> None:
    assert page_name("httpie/output/streams.py") == "httpie.output.streams"
    assert page_name("httpie/__init__.py") == "httpie.__init__"


def test_build_vault_pages_one_per_module() -> None:
    pages = build_vault_pages(_sample_graph())

    assert set(pages) == {"pkg.a", "pkg.b"}


def test_build_vault_pages_links_and_structure() -> None:
    pages = build_vault_pages(_sample_graph())

    page_a = pages["pkg.a"]
    assert "## Classes" in page_a
    assert "`Foo`" in page_a
    assert "`bar`" in page_a
    assert "## Imports" in page_a
    assert "[[pkg.b]]" in page_a

    page_b = pages["pkg.b"]
    assert "## Top-Level Functions" in page_b
    assert "`helper`" in page_b
    assert "## Imported By" in page_b
    assert "[[pkg.a]]" in page_b
