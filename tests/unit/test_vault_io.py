from pathlib import Path

from graphify_agent.services.vault_io import list_pages, read_page, write_page


def test_write_and_read_page(tmp_path: Path):
    page = tmp_path / "page.md"
    write_page(page, "hello")
    assert read_page(page) == "hello"


def test_list_pages(tmp_path: Path):
    for name in ["b.md", "a.md", "c.md"]:
        (tmp_path / name).write_text("x", encoding="utf-8")
    pages = list_pages(tmp_path)
    assert [p.name for p in pages] == ["a.md", "b.md", "c.md"]