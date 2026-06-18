from pathlib import Path


from graphify_agent.services.naive_baseline import (
    _collect_files,
    run_naive_baseline,
)


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def test_happy_path(tmp_path, monkeypatch):
    """Finds root cause on first file — stops immediately."""
    src = tmp_path / "httpie"
    src.mkdir()
    _write(src / "sessions.py", "def update_headers():\n    value.decode('utf8')\n")

    monkeypatch.setattr(
        "graphify_agent.services.naive_baseline.PROJECT_ROOT", tmp_path
    )

    result = run_naive_baseline(source_dir=src, config_name="agent")

    assert result["root_cause_found"] is True
    assert result["iterations"] == 1
    assert result["files_read"] == 1
    assert result["llm_calls"] == 1


def test_max_iterations_exhaustion(tmp_path, monkeypatch):
    """Stops at max_iterations when root cause is never found."""
    src = tmp_path / "httpie"
    src.mkdir()
    for i in range(10):
        _write(src / f"mod{i}.py", f"# module {i}\ndef foo(): pass\n")

    monkeypatch.setattr(
        "graphify_agent.services.naive_baseline.PROJECT_ROOT", tmp_path
    )

    result = run_naive_baseline(source_dir=src, config_name="agent")

    assert result["root_cause_found"] is False
    assert result["iterations"] == 5   # max_iterations from config/agent.json
    assert result["root_cause"] is None


def test_deterministic_file_order(tmp_path):
    """Two calls with the same directory produce the same file order."""
    src = tmp_path / "httpie"
    src.mkdir()
    for name in ["z.py", "a.py", "m.py"]:
        _write(src / name, "# x\n")

    files1 = _collect_files(src)
    files2 = _collect_files(src)
    assert files1 == files2
    assert [f.name for f in files1] == ["a.py", "m.py", "z.py"]


def test_schema_parity(tmp_path, monkeypatch):
    """naive_run.json has the expected key set for compare.py."""
    src = tmp_path / "httpie"
    src.mkdir()
    _write(src / "sessions.py", "def update_headers():\n    value.decode('utf8')\n")

    monkeypatch.setattr(
        "graphify_agent.services.naive_baseline.PROJECT_ROOT", tmp_path
    )

    result = run_naive_baseline(source_dir=src, config_name="agent")

    expected_keys = {
        "mode", "bug_id", "files_examined", "root_cause_found",
        "root_cause", "fix_proposal", "tokens_used", "llm_calls",
        "files_read", "iterations",
    }
    assert set(result.keys()) == expected_keys
    assert result["mode"] == "naive"


def test_no_graph_vault_imports():
    """naive_baseline.py must not import graph_tools or vault_io."""
    path = Path(__file__).parents[2] / "src" / "graphify_agent" / "services" / "naive_baseline.py"
    source = path.read_text(encoding="utf-8")
    assert "graph_tools" not in source
    assert "vault_io" not in source
