"""Builds Obsidian vault pages (one per module) from a Grphify graph.

Obsidian's Graph View renders ``[[wikilinks]]`` between Markdown notes, not
``artifacts/graph.json`` directly. This module turns the module-level
``imports`` edges of the graph into a set of cross-linked Markdown pages
under ``obsidian/components/`` so the codebase's module dependency graph
becomes visible in Obsidian's Graph View.
"""

from __future__ import annotations

from typing import Any


def page_name(module_id: str) -> str:
    """Convert a module node id (e.g. ``httpie/output/streams.py``) to a
    flat, collision-free Obsidian page name (e.g. ``httpie.output.streams``).
    """
    return module_id[:-len(".py")].replace("/", ".") if module_id.endswith(".py") else module_id


def build_vault_pages(graph: dict[str, Any]) -> dict[str, str]:
    """Return ``{page_name: markdown_content}`` for every module in ``graph``."""
    nodes = {n["id"]: n for n in graph["nodes"]}
    edges = graph["edges"]

    children: dict[str, list[str]] = {}
    for edge in edges:
        if edge["type"] == "defines":
            children.setdefault(edge["source"], []).append(edge["target"])

    imports_out: dict[str, list[str]] = {}
    imports_in: dict[str, list[str]] = {}
    for edge in edges:
        if edge["type"] == "imports":
            imports_out.setdefault(edge["source"], []).append(edge["target"])
            imports_in.setdefault(edge["target"], []).append(edge["source"])

    pages: dict[str, str] = {}
    for module_id, node in nodes.items():
        if node["type"] != "module":
            continue
        pages[page_name(module_id)] = _render_module_page(module_id, nodes, children, imports_out, imports_in)

    return pages


def _render_module_page(
    module_id: str,
    nodes: dict[str, dict[str, Any]],
    children: dict[str, list[str]],
    imports_out: dict[str, list[str]],
    imports_in: dict[str, list[str]],
) -> str:
    lines = [f"# {module_id}", ""]

    classes = [c for c in children.get(module_id, []) if nodes[c]["type"] == "class"]
    funcs = [f for f in children.get(module_id, []) if nodes[f]["type"] == "function"]

    if classes:
        lines.append("## Classes")
        lines.append("")
        for class_id in sorted(classes):
            lines.append(f"- `{nodes[class_id]['id'].split('::')[-1]}`")
            for method_id in sorted(children.get(class_id, [])):
                lines.append(f"  - `{nodes[method_id]['id'].split('.')[-1]}`")
        lines.append("")

    if funcs:
        lines.append("## Top-Level Functions")
        lines.append("")
        for func_id in sorted(funcs):
            lines.append(f"- `{nodes[func_id]['id'].split('::')[-1]}`")
        lines.append("")

    out_targets = sorted({page_name(t) for t in imports_out.get(module_id, [])})
    if out_targets:
        lines.append("## Imports")
        lines.append("")
        for target in out_targets:
            lines.append(f"- [[{target}]]")
        lines.append("")

    in_sources = sorted({page_name(s) for s in imports_in.get(module_id, [])})
    if in_sources:
        lines.append("## Imported By")
        lines.append("")
        for source in in_sources:
            lines.append(f"- [[{source}]]")
        lines.append("")

    return "\n".join(lines)
