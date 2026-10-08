from __future__ import annotations

import instructor
from openai import OpenAI
from pydantic import BaseModel

from pdf_parsing.llm.base import T

class OpenAIClient:
    """OpenAI client for structured extraction using instructor."""
    
    def __init__(self, api_key: str, model: str = 'gpt-4o'):
        self.provider_name = 'openai'
        raw_client = OpenAI(api_key=api_key)
        self.client = instructor.from_openai(raw_client)
        self.model = model

    def parse(
        self, 
        text: str, 
        prompt: str, 
        response_model: type[T], 
        max_retries: int = 3
    ) -> T:
        return self.client.chat.completions.create(
            model=self.model,
            response_model=response_model,
            max_retries=max_retries,
            messages=[
                {"role": "system", "content": prompt}, 
                {"role": "user", "content": text}
            ],
        )
