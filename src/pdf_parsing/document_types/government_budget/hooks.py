from __future__ import annotations

from typing import Any

def pre_parse(text: str) -> str:
    """Hook called before passing text to the LLM."""
    return text

def post_parse(records: list[Any]) -> list[Any]:
    """Hook called after parsing to validate or normalize data."""
    return records
