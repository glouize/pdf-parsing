from __future__ import annotations

import time
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, EasyOcrOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline

from pdf_parsing.core.models import ExtractionResult
from pdf_parsing.ocr.base import OcrBackend


class DoclingEasyOcrBackend(OcrBackend):
    """OCR backend using Docling configured with EasyOCR."""
    
    name: str = "docling_easyocr"
    
    def extract(self, pdf_path: Path) -> ExtractionResult:
        start_time = time.time()
        warnings = []
        plaintext = ""
        pages = []
        
        try:
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = True
            pipeline_options.ocr_options = EasyOcrOptions()
            
            converter = DocumentConverter(
                format_options={
                    InputFormat.PDF: PdfFormatOption(
                        pipeline_cls=StandardPdfPipeline,
                        pipeline_options=pipeline_options,
                    )
                }
            )
            
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
