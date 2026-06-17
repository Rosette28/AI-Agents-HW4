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
    elif len(sys.argv) > 1 and sys.argv[1] == "agent":
        mode = "graph_guided"
        for arg in sys.argv[2:]:
            if arg.startswith("--mode="):
                mode = arg.split("=", 1)[1]
            elif arg == "--mode" and sys.argv.index(arg) + 1 < len(sys.argv):
                mode = sys.argv[sys.argv.index(arg) + 1]
        if mode == "naive":
            from graphify_agent.services.naive_baseline import run_naive_baseline
            result = run_naive_baseline()
            print(f"Wrote reports/naive_run.json (root_cause_found={result['root_cause_found']}, "
                  f"tokens={result['tokens_used']}, iterations={result['iterations']})")
        else:
            from graphify_agent.services.workflow import run_workflow
            import json
            from graphify_agent.config import PROJECT_ROOT
            result = run_workflow()
            out = PROJECT_ROOT / "reports" / "graph_guided_run.json"
            out.write_text(json.dumps(result, indent=2), encoding="utf-8")
            print(f"Wrote reports/graph_guided_run.json")
    elif len(sys.argv) > 1 and sys.argv[1] == "compare":
        from graphify_agent.services.compare import run_compare
        out = run_compare()
        print(f"Wrote {out} and reports/token_comparison.png")
    else:
        print("Hello from graphify-agent!")
