from __future__ import annotations

import json
from unittest.mock import patch, MagicMock
from pdf_parsing.parsing.prompt_builder import build_prompt, get_schema_description
from pdf_parsing.parsing.api import parse_text
from pdf_parsing.core.models import ParseResult, ExtractionResult
from pydantic import BaseModel, Field

class DummySchema(BaseModel):
    name: str = Field(..., description="The name")
    age: int = Field(..., description="The age")

def test_prompt_template_rendering():
    prompt = build_prompt("My text", DummySchema)
    assert "My text" in prompt
    assert "The name" in prompt

def test_schema_description_generation():
    desc = get_schema_description(DummySchema)
    assert "name" in desc
    assert "age" in desc

def test_parse_result_validation():
    result = ParseResult(
        parsed_data={"name": "Alice", "age": 30},
        raw_response='{"name": "Alice", "age": 30}',
        model_name="dummy-model",
        prompt_tokens=10,
        completion_tokens=5,
        cost=0.001
    )
    assert result.parsed_data["name"] == "Alice"

@patch('pdf_parsing.parsing.api.generate_response')
def test_parse_text_mocked(mock_generate_response):
    mock_generate_response.return_value = ParseResult(
        parsed_data={"name": "Bob", "age": 25},
        raw_response='{"name": "Bob", "age": 25}',
        model_name="mock-model",
        prompt_tokens=1,
        completion_tokens=1,
        cost=0.0
    )
    
    extraction = ExtractionResult(
        plaintext="Bob is 25",
        pages=["Bob is 25"],
        page_count=1,
        confidence=1.0,
        source_path="/tmp/test.pdf",
        ocr_backend="mock"
    )
    
    result = parse_text(extraction, DummySchema)
    assert result.parsed_data["name"] == "Bob"
