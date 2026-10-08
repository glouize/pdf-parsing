from __future__ import annotations

from pathlib import Path

import structlog
from prefect import flow
from prefect.artifacts import create_markdown_artifact

from pdf_parsing.core.models import PipelineResult
from pdf_parsing.flows.document_flow import process_document

logger = structlog.get_logger(__name__)

@flow(name="process-batch", log_prints=True)
def process_batch(
    input_dir: str,
    document_type: str,
    ocr_backend: str | None = None,
    max_concurrency: int = 4,
    fail_fast: bool = False,
) -> list[PipelineResult]:
    """Process a batch of PDFs in a directory."""
    input_path = Path(input_dir)
    if not input_path.is_dir():
        raise ValueError(f"Invalid input directory: {input_dir}")
        
    pdf_files = list(input_path.glob("*.pdf"))
    if not pdf_files:
        logger.warning("No PDF files found", directory=input_dir)
        return []
        
    logger.info("Starting batch processing", count=len(pdf_files), directory=input_dir)
    
    results: list[PipelineResult] = []
    
    futures = []
    for pdf_file in pdf_files:
        future = process_document.submit(
            pdf_path=str(pdf_file),
            document_type=document_type,
            ocr_backend=ocr_backend,
        )
        futures.append(future)
        
    # Wait for results
    for future in futures:
        try:
            result = future.result()
            results.append(result)
            if fail_fast and not result.success:
                raise RuntimeError(f"Pipeline failed for {result.source_path}: {result.error}")
        except Exception as e:
            logger.error("Error retrieving result", error=str(e))
            if fail_fast:
                raise
                
    # Summary stats
    total = len(results)
    succeeded = sum(1 for r in results if r.success)
    failed = total - succeeded
    
    confidences = [
        r.parse_result.confidence_score 
        for r in results 
        if r.success and r.parse_result and r.parse_result.confidence_score is not None
    ]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    
    logger.info(
        "Batch summary",
        total=total,
        succeeded=succeeded,
        failed=failed,
        avg_confidence=avg_confidence
    )
    
    markdown_content = f"""
# Batch Processing Summary
- **Input Directory:** {input_dir}
- **Document Type:** {document_type}
- **Total Files:** {total}
- **Succeeded:** {succeeded}
- **Failed:** {failed}
- **Average Confidence:** {avg_confidence:.2f}
"""
    
    create_markdown_artifact(
        key="batch-summary",
        markdown=markdown_content,
        description=f"Batch processing summary for {input_dir}"
    )
    
    return results
