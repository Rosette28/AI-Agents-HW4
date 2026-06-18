"""Build the {nodes, edges} graph by AST-walking a Python package (Grphify step)."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

_DEF_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)


def _mk_node(id_: str, type_: str, file: str, lines: list[int]) -> dict[str, Any]:
    return {"id": id_, "type": type_, "file": file, "lines": lines}


def _node_id(rel_path: str, *parts: str) -> str:
    suffix = ".".join(parts)
    return f"{rel_path}::{suffix}" if suffix else rel_path


def _module_name(rel_path: Path) -> str:
    return rel_path.with_suffix("").as_posix().replace("/", ".")


def build_graph(source_dir: Path) -> dict[str, Any]:
    """Build a ``{nodes, edges}`` graph for all ``*.py`` files under ``source_dir``."""
    source_dir = Path(source_dir)
    package_root = source_dir.parent
    py_files = sorted(source_dir.rglob("*.py"))
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, str]] = []
    module_by_dotted: dict[str, str] = {}
    simple_name_index: dict[str, list[str]] = {}
    trees: dict[str, ast.Module] = {}
    for path in py_files:
        rel = path.relative_to(package_root).as_posix()
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source, filename=rel)
        trees[rel] = tree
        nodes[rel] = _mk_node(rel, "module", rel, [1, len(source.splitlines())])
        module_by_dotted[_module_name(path.relative_to(package_root))] = rel
    _add_definitions(trees, nodes, edges, simple_name_index)
    _add_imports(trees, module_by_dotted, edges)
    _add_calls(trees, simple_name_index, edges)
    _compute_degrees(nodes, edges)
    return {"nodes": list(nodes.values()), "edges": edges}


def _add_definitions(
    trees: dict[str, ast.Module], nodes: dict[str, dict], edges: list, name_idx: dict
) -> None:
    for rel, tree in trees.items():
        for item in tree.body:
            if isinstance(item, ast.ClassDef):
                class_id = _node_id(rel, item.name)
                nodes[class_id] = _mk_node(class_id, "class", rel, [item.lineno, item.end_lineno or item.lineno])
                edges.append({"source": rel, "target": class_id, "type": "defines"})
                name_idx.setdefault(item.name, []).append(class_id)
                for sub in item.body:
                    if isinstance(sub, _DEF_TYPES):
                        m_id = _node_id(rel, item.name, sub.name)
                        nodes[m_id] = _mk_node(m_id, "function", rel, [sub.lineno, sub.end_lineno or sub.lineno])
                        edges.append({"source": class_id, "target": m_id, "type": "defines"})
                        # Exclude dunders from call resolution: they flood the graph with noise.
                        if not (sub.name.startswith("__") and sub.name.endswith("__")):
                            name_idx.setdefault(sub.name, []).append(m_id)
            elif isinstance(item, _DEF_TYPES):
                f_id = _node_id(rel, item.name)
                nodes[f_id] = _mk_node(f_id, "function", rel, [item.lineno, item.end_lineno or item.lineno])
                edges.append({"source": rel, "target": f_id, "type": "defines"})
                name_idx.setdefault(item.name, []).append(f_id)


def _resolve_relative(rel: str, level: int, module: str | None) -> str | None:
    """Resolve a ``from . import X`` / ``from ..pkg import X`` target dotted name."""
    parts = _module_name(Path(rel)).split(".")
    base = parts[:-level] if level else parts[:-1]
    if module:
        base = base + module.split(".")
    return ".".join(base) if base else None


def _add_imports(
    trees: dict[str, ast.Module], module_by_dotted: dict[str, str], edges: list
) -> None:
    for rel, tree in trees.items():
        for item in ast.walk(tree):
            if isinstance(item, ast.ImportFrom):
                target = None
                if item.level:
                    dotted = _resolve_relative(rel, item.level, item.module)
                    target = module_by_dotted.get(dotted) if dotted else None
                elif item.module:
                    target = module_by_dotted.get(item.module) or module_by_dotted.get(
                        f"httpie.{item.module}"
                    )
                if target and target != rel:
                    edges.append({"source": rel, "target": target, "type": "imports"})
            elif isinstance(item, ast.Import):
                for alias in item.names:
                    target = module_by_dotted.get(alias.name)
                    if target and target != rel:
                        edges.append({"source": rel, "target": target, "type": "imports"})


def _add_calls(
    trees: dict[str, ast.Module], simple_name_index: dict[str, list[str]], edges: list
) -> None:
    for rel, tree in trees.items():
        funcs: list[tuple[str, ast.AST]] = []
        for item in tree.body:
            if isinstance(item, _DEF_TYPES):
                funcs.append((_node_id(rel, item.name), item))
            elif isinstance(item, ast.ClassDef):
                for sub in item.body:
                    if isinstance(sub, _DEF_TYPES):
                        funcs.append((_node_id(rel, item.name, sub.name), sub))
        for caller_id, func_node in funcs:
            for call in ast.walk(func_node):
                if not isinstance(call, ast.Call):
                    continue
                name = None
                if isinstance(call.func, ast.Name):
                    name = call.func.id
                elif isinstance(call.func, ast.Attribute):
                    name = call.func.attr
                if not name:
                    continue
                for target_id in simple_name_index.get(name, []):
                    if target_id != caller_id:
                        edges.append({"source": caller_id, "target": target_id, "type": "calls"})


def _compute_degrees(nodes: dict[str, dict], edges: list) -> None:
    for node in nodes.values():
        node["metrics"] = {"in_degree": 0, "out_degree": 0}
    for edge in edges:
        if edge["source"] in nodes:
            nodes[edge["source"]]["metrics"]["out_degree"] += 1
        if edge["target"] in nodes:
            nodes[edge["target"]]["metrics"]["in_degree"] += 1
