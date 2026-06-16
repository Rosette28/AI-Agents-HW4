from pathlib import Path

from graphify_agent.services.vault_io import (
    read_page,
    write_page,
)


def test_write_and_read_page(tmp_path: Path):
    page = tmp_path / "page.md"

    write_page(page, "hello")

    assert read_page(page) == "hello"