from __future__ import annotations

from typing import TypeVar
import instructor
from google import genai
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class GeminiClient:
    """LLM client for Gemini using instructor and google-genai."""
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-pro") -> None:
        self.provider_name = "gemini"
        raw_client = genai.Client(api_key=api_key)
        self.client = instructor.from_gemini(
            client=raw_client,
            mode=instructor.Mode.GEMINI_JSON,
        )
        self.model = model

    def parse(
        self,
        text: str,
        prompt: str,
        response_model: type[T],
        max_retries: int = 3,
    ) -> T:
        return self.client.chat.completions.create(
            model=self.model,
            response_model=response_model,
            max_retries=max_retries,
            messages=[
                {"role": "user", "content": f"{prompt}\n\nDocument text:\n{text}"}
            ],
        )
