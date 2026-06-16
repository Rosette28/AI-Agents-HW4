from pathlib import Path


def read_page(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def list_pages(directory: Path) -> list[Path]:
    return sorted(directory.glob("*.md"))

def write_page(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")