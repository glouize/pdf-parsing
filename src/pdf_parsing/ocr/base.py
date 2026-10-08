from __future__ import annotations

from pathlib import Path
from typing import Protocol

from pdf_parsing.core.models import ExtractionResult


class OcrBackend(Protocol):
    """Protocol for OCR backends."""
    
    name: str
    
    def extract(self, pdf_path: Path) -> ExtractionResult: ...


def get_ocr_backend(name: str) -> OcrBackend:
    """Factory function to get an OCR backend instance by name."""
    if name == "docling_default":
        from pdf_parsing.ocr.docling_default import DoclingDefaultBackend
        return DoclingDefaultBackend()
    elif name == "docling_tesseract":
        from pdf_parsing.ocr.docling_tesseract import DoclingTesseractBackend
        return DoclingTesseractBackend()
    elif name == "docling_easyocr":
        from pdf_parsing.ocr.docling_easyocr import DoclingEasyOcrBackend
        return DoclingEasyOcrBackend()
    else:
        raise ValueError(f"Unknown OCR backend: {name}")
