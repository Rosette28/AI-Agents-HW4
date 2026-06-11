from graphify_agent.config import CONFIG_DIR, PROJECT_ROOT, load_config


def test_project_root_and_config_dir() -> None:
    assert (PROJECT_ROOT / "config").resolve() == CONFIG_DIR.resolve()


def test_load_config_grphify() -> None:
    cfg = load_config("grphify")

    assert cfg["source_dir"] == "data/httpie/httpie"
    assert cfg["output_graph"] == "artifacts/graph.json"
    assert cfg["output_report"] == "artifacts/GRAPH_REPORT.md"
