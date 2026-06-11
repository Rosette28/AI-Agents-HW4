"""SDK layer: single entry point for the graphify_agent package."""

from __future__ import annotations

import json
from typing import Any

from graphify_agent.config import PROJECT_ROOT, load_config
from graphify_agent.services.grphify_builder import build_graph
from graphify_agent.services.grphify_report import build_report
from graphify_agent.services.vault_builder import build_vault_pages


def run_grphify(config_name: str = "grphify") -> dict[str, Any]:
    """Build the codebase graph and write ``graph.json`` + ``GRAPH_REPORT.md``.

    Settings (source/output paths) come from ``config/<config_name>.json``
    so they are not hardcoded here.
    """
    cfg = load_config(config_name)
    source_dir = PROJECT_ROOT / cfg["source_dir"]
    graph = build_graph(source_dir)
    report = build_report(graph, title=cfg.get("report_title", "Grphify Graph Report"))

    graph_path = PROJECT_ROOT / cfg["output_graph"]
    report_path = PROJECT_ROOT / cfg["output_report"]
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    graph_path.write_text(json.dumps(graph, indent=2), encoding="utf-8")
    report_path.write_text(report, encoding="utf-8")

    return graph


def run_vault_build(config_name: str = "vault", graph_config_name: str = "grphify") -> dict[str, str]:
    """Generate one cross-linked Obsidian page per module under
    ``components_dir``, derived from ``artifacts/graph.json``.

    Settings come from ``config/<config_name>.json``; no paths are
    hardcoded here.
    """
    cfg = load_config(config_name)
    graph_path = PROJECT_ROOT / load_config(graph_config_name)["output_graph"]
    graph = json.loads(graph_path.read_text(encoding="utf-8"))

    pages = build_vault_pages(graph)

    components_dir = PROJECT_ROOT / cfg["components_dir"]
    components_dir.mkdir(parents=True, exist_ok=True)
    for name, content in pages.items():
        (components_dir / f"{name}.md").write_text(content, encoding="utf-8")

    return pages
