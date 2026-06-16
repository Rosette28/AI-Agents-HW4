from graphify_agent.services.navigator_agent import run as navigate
from graphify_agent.services.suspect_ranker import rank
from graphify_agent.services.code_reader import read_component
from graphify_agent.services.explainer_agent import explain


def run_workflow() -> dict:
    candidates = navigate()

    ranked = rank(candidates)

    findings = []

    for component in ranked:
        content = read_component(component)
        findings.append(
            {
                "component": component,
                "content_length": len(content),
            }
        )

    return {
        "ranked_candidates": ranked,
        "findings": findings,
        "explanation": explain(),
    }