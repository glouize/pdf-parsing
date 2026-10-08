from __future__ import annotations

import structlog
from prefect import task, tags
from prefect.artifacts import create_markdown_artifact

from pdf_parsing.core.models import ExtractionResult, ParseResult
from pdf_parsing.core.parsing import parse_document
from pdf_parsing.core.registry import registry

logger = structlog.get_logger(__name__)

@task(
    name="parse-document",
    retries=3,
    retry_delay_seconds=[30, 60, 120],  # exponential backoff for LLM rate limits
    log_prints=True,
)
def parse_task(
    extraction_result: ExtractionResult,
    document_type_name: str,
) -> ParseResult:
    """Parse extracted text into structured records."""
    logger.info("Starting parse_task", document_type=document_type_name)
    config = registry.get(document_type_name)
    
    with tags(document_type_name):
        result = parse_document(
            extraction_result=extraction_result,
            prompt_text=config.prompt_text,
            parent_model=config.parent_model,
            llm_provider=config.llm_provider,
            llm_model=config.llm_model,
            max_retries=config.max_retries,
        )
        
    # Create Prefect artifact
    markdown_content = f"""
# Parse Stats
- **Model Used:** {result.model_used}
- **Parse Time (s):** {result.parse_time_seconds:.2f}
- **Confidence Score:** {result.confidence_score}
- **Prompt Tokens:** {result.prompt_tokens}
- **Completion Tokens:** {result.completion_tokens}
- **Records Extracted:** {len(result.records)}
"""
    
    create_markdown_artifact(
        key="parse-stats",
        markdown=markdown_content,
        description=f"Parse stats for {document_type_name}"
    )
    
    return result
