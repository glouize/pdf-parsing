from __future__ import annotations

import structlog
from prefect import task
from prefect.artifacts import create_markdown_artifact

from pdf_parsing.core.models import ParseResult
from pdf_parsing.core.persistence import persist_records

logger = structlog.get_logger(__name__)

@task(
    name="persist-records",
    retries=1,
    log_prints=True,
)
def persist_task(
    parse_result: ParseResult,
    source_document_id: str,
    source_file_name: str,
) -> list[int]:
    """Persist structured records to database."""
    logger.info("Starting persist_task", source_document_id=source_document_id)
    
    record_ids = persist_records(
        parse_result=parse_result,
        source_document_id=source_document_id,
        source_file_name=source_file_name,
    )
    
    markdown_content = f"""
# Persistence Stats
- **Records Inserted:** {len(record_ids)}
- **Source Document ID:** {source_document_id}
"""
    
    create_markdown_artifact(
        key="persist-stats",
        markdown=markdown_content,
        description=f"Persistence stats for {source_document_id}"
    )
    
    return record_ids
