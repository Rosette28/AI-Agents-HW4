import sys


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "graph":
        from graphify_agent.sdk import run_grphify

        graph = run_grphify()
        print(
            f"Wrote artifacts/graph.json ({len(graph['nodes'])} nodes, "
            f"{len(graph['edges'])} edges) and artifacts/GRAPH_REPORT.md"
        )
    elif len(sys.argv) > 1 and sys.argv[1] == "vault":
        from graphify_agent.sdk import run_vault_build

        pages = run_vault_build()
        print(f"Wrote {len(pages)} pages to obsidian/components/")
    else:
        print("Hello from graphify-agent!")
