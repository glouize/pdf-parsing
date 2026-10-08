from __future__ import annotations

import hashlib

import structlog
from prefect import task
from prefect.artifacts import create_markdown_artifact

from pdf_parsing.core.extraction import extract_document
from pdf_parsing.core.models import ExtractionResult

logger = structlog.get_logger(__name__)

def hash_file_contents(context, parameters):
    pdf_path = parameters.get("pdf_path")
    try:
        with open(pdf_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

@task(
    name="extract-document",
    retries=2,
    retry_delay_seconds=10,
    log_prints=True,
    cache_key_fn=hash_file_contents,
)
def extract_task(pdf_path: str, ocr_backend: str | None = None) -> ExtractionResult:
    """Extract plaintext from a PDF."""
    logger.info("Starting extract_task", pdf_path=pdf_path)
    result = extract_document(pdf_path, ocr_backend)
    
    # Create Prefect artifact
    markdown_content = f"""
# Extraction Stats
- **Page Count:** {result.page_count}
- **Extraction Time (s):** {result.extraction_time_seconds:.2f}
- **Warnings:** {len(result.warnings)}

## Warnings Details
"""
    for w in result.warnings:
        markdown_content += f"- {w}\n"
        
    create_markdown_artifact(
        key="extraction-stats",
        markdown=markdown_content,
        description=f"Extraction stats for {pdf_path}"
    )
    
    return result
