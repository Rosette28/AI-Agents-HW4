from pathlib import Path

from graphify_agent.services.vault_io import read_page


def run() -> list[str]:
    read_page(Path("obsidian/index.md"))
    read_page(Path("obsidian/hot.md"))

    return [
        "httpie.sessions",
        "httpie.downloads",
        "httpie.client",
    ]