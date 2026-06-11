"""Markdown report generator for graphs produced by ``grphify_builder``."""

from __future__ import annotations

from typing import Any


def build_report(graph: dict[str, Any], title: str = "Grphify Graph Report") -> str:
    """Render a Markdown summary of ``graph`` (as built by ``build_graph``)."""
    nodes = graph["nodes"]
    edges = graph["edges"]

    by_type: dict[str, int] = {}
    for node in nodes:
        by_type[node["type"]] = by_type.get(node["type"], 0) + 1

    edge_by_type: dict[str, int] = {}
    for edge in edges:
        edge_by_type[edge["type"]] = edge_by_type.get(edge["type"], 0) + 1

    files = sorted({node["file"] for node in nodes if node["type"] == "module"})

    hubs = sorted(
        nodes,
        key=lambda n: n["metrics"]["in_degree"] + n["metrics"]["out_degree"],
        reverse=True,
    )[:10]

    lines = [f"# {title}", "", "## Summary", ""]
    lines.append(f"- Total nodes: {len(nodes)}")
    for node_type, count in sorted(by_type.items()):
        lines.append(f"  - {node_type}: {count}")
    lines.append(f"- Total edges: {len(edges)}")
    for edge_type, count in sorted(edge_by_type.items()):
        lines.append(f"  - {edge_type}: {count}")
    lines.append("")

    lines.append("## Files Analyzed")
    lines.append("")
    for f in files:
        lines.append(f"- `{f}`")
    lines.append("")

    lines.append("## Top Hub Nodes (in_degree + out_degree)")
    lines.append("")
    lines.append("| Node | Type | In | Out |")
    lines.append("|---|---|---|---|")
    for node in hubs:
        m = node["metrics"]
        lines.append(f"| `{node['id']}` | {node['type']} | {m['in_degree']} | {m['out_degree']} |")
    lines.append("")

    return "\n".join(lines)
