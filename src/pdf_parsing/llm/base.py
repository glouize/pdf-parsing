from __future__ import annotations

from typing import Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class LlmClient(Protocol):
    """Protocol for LLM clients used for structured data extraction."""
    provider_name: str
    
    def parse(
        self,
        text: str,
        prompt: str,
        response_model: type[T],
        max_retries: int = 3,
    ) -> T:
        ...
