from __future__ import annotations

import time
from typing import TypeVar, get_args, get_origin
import structlog
from jinja2 import Template
from pydantic import BaseModel

from pdf_parsing.config import settings
from pdf_parsing.core.models import ExtractionResult, ParseResult
from pdf_parsing.llm.factory import get_llm_client

logger = structlog.get_logger(__name__)

T = TypeVar("T", bound=BaseModel)

def _generate_schema_description(model: type[BaseModel]) -> str:
    """Generate a text description of a Pydantic model's schema."""
    lines = []
    for field_name, field_info in model.model_fields.items():
        desc = field_info.description or "No description provided."
        lines.append(f"- {field_name}: {desc}")
    return "\n".join(lines)

def parse_document(
    extraction_result: ExtractionResult,
    prompt_template: str,
    response_model: type[T],
    context: str = '',
    llm_provider: str | None = None,
    llm_model: str | None = None,
    max_retries: int | None = None,
) -> ParseResult:
    """Parse text into structured data using an LLM."""
    start_time = time.time()
    
    # Determine if response model is a list or a single model
    is_list = False
    actual_model = response_model
    origin = get_origin(response_model)
    if origin is list or origin is list:
        is_list = True
        args = get_args(response_model)
        if args:
            actual_model = args[0]
            
    schema_desc = _generate_schema_description(actual_model) if issubclass(actual_model, BaseModel) else ""
    
    template = Template(prompt_template)
    prompt = template.render(
        plaintext=extraction_result.plaintext,
        schema_description=schema_desc,
        context=context
    )
    
    client = get_llm_client(provider=llm_provider, model=llm_model)
    retries = max_retries if max_retries is not None else getattr(settings, "MAX_RETRIES", 3)
    
    logger.info("Parsing document", provider=client.provider_name, model=client.model)
    
    try:
        result = client.parse(
            text=extraction_result.plaintext,
            prompt=prompt,
            response_model=response_model,
            max_retries=retries
        )
    except Exception as e:
        logger.error("Parsing failed", error=str(e))
        raise

    parse_time = time.time() - start_time
    
    records = result if is_list and isinstance(result, list) else [result]
    
    return ParseResult(
        records=records,
        model_used=client.model,
        parse_time_seconds=parse_time
    )
