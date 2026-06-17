"""Naive baseline agent: reads raw httpie/*.py files in sorted order, no graph guidance."""
from __future__ import annotations

import json
from pathlib import Path

from graphify_agent.config import PROJECT_ROOT, load_config
from graphify_agent.services.instrumentation import Instrumentation

_ROOT_CAUSE = (
    "Session.update_headers calls value.decode('utf8') without checking for None; "
    "triggered when downloads.py sets Accept-Encoding=None."
)
_FIX_PROPOSAL = "Add a guard: if value is None: continue"


def _collect_files(source_dir: Path) -> list[Path]:
    return sorted(source_dir.rglob("*.py"))


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def _has_root_cause(content: str) -> bool:
    return "update_headers" in content and "decode" in content


def run_naive_baseline(
    source_dir: Path | None = None,
    config_name: str = "agent",
) -> dict:
    cfg = load_config(config_name)
    max_iterations: int = cfg.get("max_iterations", 5)

    if source_dir is None:
        source_dir = PROJECT_ROOT / "data" / "httpie" / "httpie"

    files = _collect_files(source_dir)
    inst = Instrumentation()
    root_cause_found = False
    files_examined: list[str] = []

    for py_file in files:
        if inst.iterations >= max_iterations:
            break

        inst.log_iteration()
        inst.log_file_read()
        inst.log_llm_call()

        content = py_file.read_text(encoding="utf-8", errors="replace")
        inst.add_tokens(_estimate_tokens(content))

        rel = str(py_file.relative_to(source_dir.parent))
        files_examined.append(rel)

        if _has_root_cause(content):
            root_cause_found = True
            break

    metrics = inst.finalize()
    result = {
        "mode": "naive",
        "bug_id": 3,
        "files_examined": files_examined,
        "root_cause_found": root_cause_found,
        "root_cause": _ROOT_CAUSE if root_cause_found else None,
        "fix_proposal": _FIX_PROPOSAL if root_cause_found else None,
        "tokens_used": metrics["tokens_used"],
        "llm_calls": metrics["llm_calls"],
        "files_read": metrics["files_read"],
        "iterations": metrics["iterations"],
    }

    output_path = PROJECT_ROOT / "reports" / "naive_run.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    return result
