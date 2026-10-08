from __future__ import annotations

import instructor
from anthropic import Anthropic
from pydantic import BaseModel

from pdf_parsing.llm.base import T

class AnthropicClient:
    """Anthropic client for structured extraction using instructor."""
    
    def __init__(self, api_key: str, model: str = 'claude-sonnet-4-20250514'):
        self.provider_name = 'anthropic'
        raw_client = Anthropic(api_key=api_key)
        self.client = instructor.from_anthropic(raw_client)
        self.model = model

    def parse(
        self, 
        text: str, 
        prompt: str, 
        response_model: type[T], 
        max_retries: int = 3
    ) -> T:
        return self.client.messages.create(
            model=self.model,
            response_model=response_model,
            max_retries=max_retries,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": f"{prompt}\n\n{text}"}
            ],
        )
