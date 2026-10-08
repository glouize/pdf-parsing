from __future__ import annotations

import hashlib
import time
from pathlib import Path

import structlog
from prefect import flow

from pdf_parsing.core.models import PipelineResult
from pdf_parsing.core.registry import registry
from pdf_parsing.flows.tasks.extract import extract_task
from pdf_parsing.flows.tasks.parse import parse_task
from pdf_parsing.flows.tasks.persist import persist_task

logger = structlog.get_logger(__name__)

@flow(name="process-document", log_prints=True)
def process_document(
    pdf_path: str,
    document_type: str,
    ocr_backend: str | None = None,
) -> PipelineResult:
    """End-to-end pipeline for a single document."""
    start_time = time.time()
    
    # Generate source_document_id
    try:
        with open(pdf_path, "rb") as f:
            source_document_id = hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        logger.error("Failed to hash PDF file", error=str(e), path=pdf_path)
        return PipelineResult(
            success=False,
            document_type=document_type,
            source_path=pdf_path,
            error=f"Failed to read file: {e}",
            processing_time_seconds=time.time() - start_time
        )
        
    source_file_name = Path(pdf_path).name
    
    try:
        # Extract
        extraction_result = extract_task(pdf_path, ocr_backend)
        
        # Parse
        parse_result = parse_task(extraction_result, document_type)
        
        # Check confidence
        config = registry.get(document_type)
        if parse_result.confidence_score is not None and parse_result.confidence_score < config.confidence_threshold:
            logger.warning(
                "Low confidence score",
                score=parse_result.confidence_score,
                threshold=config.confidence_threshold
            )
            
        # Persist
        record_ids = persist_task(
            parse_result=parse_result,
            source_document_id=source_document_id,
            source_file_name=source_file_name
        )
        
        processing_time = time.time() - start_time
        
        return PipelineResult(
            success=True,
            document_type=document_type,
            source_path=pdf_path,
            record_ids=record_ids,
            extraction_result=extraction_result,
            parse_result=parse_result,
            processing_time_seconds=processing_time,
        )
        
    except Exception as e:
        logger.exception("Pipeline failed", error=str(e), path=pdf_path)
        processing_time = time.time() - start_time
        return PipelineResult(
            success=False,
            document_type=document_type,
            source_path=pdf_path,
            error=str(e),
            processing_time_seconds=processing_time,
        )
