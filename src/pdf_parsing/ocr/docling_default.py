from __future__ import annotations

import time
from pathlib import Path

from docling.document_converter import DocumentConverter

from pdf_parsing.core.models import ExtractionResult
from pdf_parsing.ocr.base import OcrBackend


class DoclingDefaultBackend(OcrBackend):
    """Default OCR backend using Docling's DocumentConverter."""
    
    name: str = "docling_default"
    
    def extract(self, pdf_path: Path) -> ExtractionResult:
        start_time = time.time()
        warnings = []
        plaintext = ""
        pages = []
        
        try:
            converter = DocumentConverter()
            result = converter.convert(pdf_path)
            document = result.document
            
            plaintext = document.export_to_markdown()
            
            if hasattr(document, "pages"):
                for page_no, page_data in document.pages.items():
                    pages.append(str(page_data))
            else:
                pages = [plaintext]
                
        except Exception as e:
            warnings.append(str(e))
            
        extraction_time_seconds = time.time() - start_time
        
        return ExtractionResult(
            plaintext=plaintext,
            pages=pages,
            page_count=len(pages),
            extraction_time_seconds=extraction_time_seconds,
            warnings=warnings,
            source_path=str(pdf_path),
            ocr_backend=self.name,
        )
