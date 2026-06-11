import json

from graphify_agent import sdk


def test_run_grphify_writes_artifacts(tmp_path, monkeypatch) -> None:
    source_dir = tmp_path / "data" / "pkg"
    source_dir.mkdir(parents=True)
    (source_dir / "mod.py").write_text("def foo():\n    return 1\n", encoding="utf-8")

    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "grphify_test.json").write_text(
        json.dumps(
            {
                "source_dir": "data/pkg",
                "output_graph": "artifacts/graph.json",
                "output_report": "artifacts/GRAPH_REPORT.md",
                "report_title": "Test Graph",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(sdk, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(sdk, "CONFIG_DIR", config_dir, raising=False)
    monkeypatch.setattr("graphify_agent.config.CONFIG_DIR", config_dir)

    graph = sdk.run_grphify(config_name="grphify_test")

    graph_path = tmp_path / "artifacts" / "graph.json"
    report_path = tmp_path / "artifacts" / "GRAPH_REPORT.md"
    assert graph_path.exists()
    assert report_path.exists()
    assert json.loads(graph_path.read_text(encoding="utf-8")) == graph
    assert "Test Graph" in report_path.read_text(encoding="utf-8")
