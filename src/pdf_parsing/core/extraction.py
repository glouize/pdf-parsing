from __future__ import annotations

import hashlib
from pathlib import Path

import structlog

from pdf_parsing.config import settings
from pdf_parsing.core.models import ExtractionResult
from pdf_parsing.ocr.base import get_ocr_backend

logger = structlog.get_logger(__name__)


def extract_document(pdf_path: Path | str, ocr_backend: str | None = None) -> ExtractionResult:
    """Extract plaintext from a PDF using the configured OCR backend."""
    pdf_path_obj = Path(pdf_path)
    
    if ocr_backend is None:
        ocr_backend = settings.default_ocr_backend
        
    logger.info("Extracting document", pdf_path=str(pdf_path_obj), ocr_backend=ocr_backend)
    
    # Generate source_document_id as SHA-256 hash of file contents
    file_hash = ""
    try:
        with open(pdf_path_obj, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        logger.error("Failed to read file for hashing", error=str(e), path=str(pdf_path_obj))
        
    backend = get_ocr_backend(ocr_backend)
    result = backend.extract(pdf_path_obj)
    
    logger.info(
        "Extraction complete",
        source_document_id=file_hash,
        time_seconds=result.extraction_time_seconds,
        pages=result.page_count,
        warnings_count=len(result.warnings)
    )
    
    return result
