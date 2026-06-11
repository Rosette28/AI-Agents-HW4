"""Configuration manager: loads settings from config/ and environment variables."""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"


def load_config(name: str) -> dict:
    """Load ``config/<name>.json`` and return it as a dict."""
    path = CONFIG_DIR / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))
