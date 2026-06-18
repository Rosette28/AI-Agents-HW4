from graphify_agent.services.compare import (
    _estimate_tokens,
    _graph_guided_metrics,
    _load_naive,
    _md_table,
)


def test_estimate_tokens_basic():
    assert _estimate_tokens("a" * 400) == 100


def test_estimate_tokens_empty():
    assert _estimate_tokens("") == 1


def test_md_table_structure():
    rows = [
        {
            "mode": "graph_guided",
            "tokens_used": 100,
            "llm_calls": 4,
            "files_read": 5,
            "iterations": 1,
            "root_cause_found": True,
        }
    ]
    table = _md_table(rows)
    assert "graph_guided" in table
    assert "root_cause_found" in table
    assert "|" in table


def test_load_naive_schema():
    result = _load_naive()
    assert result["mode"] == "naive"
    assert "tokens_used" in result
    assert "llm_calls" in result
    assert "files_read" in result
    assert "iterations" in result
    assert "root_cause_found" in result


def test_graph_guided_metrics_schema():
    result = _graph_guided_metrics()
    assert result["mode"] == "graph_guided"
    assert result["root_cause_found"] is True
    assert result["tokens_used"] > 0
    assert result["files_read"] == 5


def test_bar_chart_creates_file(tmp_path):
    from graphify_agent.services.compare import _bar_chart

    rows = [
        {"mode": "graph_guided", "tokens_used": 100},
        {"mode": "naive", "tokens_used": 200},
    ]
    out = tmp_path / "chart.png"
    _bar_chart(rows, out)
    assert out.exists()
