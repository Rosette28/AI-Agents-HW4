from pathlib import Path

from graphify_agent.services.vault_io import read_page


def read_component(component_name: str) -> str:
    path = Path(
        f"obsidian/components/{component_name}.md"
    )

    return read_page(path)