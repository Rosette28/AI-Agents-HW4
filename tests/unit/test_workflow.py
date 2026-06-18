from graphify_agent.services.explainer_agent import explain
from graphify_agent.services.suspect_ranker import rank
from graphify_agent.services.code_reader import read_component
from graphify_agent.services.workflow import run_workflow


def test_run_workflow_structure():
    result = run_workflow()
    assert "ranked_candidates" in result
    assert "findings" in result
    assert "explanation" in result


def test_run_workflow_identifies_sessions():
    result = run_workflow()
    assert "httpie.sessions" in result["ranked_candidates"]


def test_rank_sessions_first():
    result = rank(["httpie.client", "httpie.sessions", "httpie.downloads"])
    assert result[0] == "httpie.sessions"


def test_rank_unknown_candidate():
    result = rank(["unknown_module"])
    assert result == ["unknown_module"]


def test_explain_mentions_update_headers():
    result = explain()
    assert "update_headers" in result


def test_read_component_returns_content():
    content = read_component("httpie.sessions")
    assert len(content) > 10
