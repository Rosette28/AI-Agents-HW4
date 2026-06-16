from pprint import pprint

from graphify_agent.services.workflow import run_workflow


def main() -> None:
    result = run_workflow()

    pprint(result)


if __name__ == "__main__":
    main()