from __future__ import annotations

import unittest
from unittest.mock import patch, MagicMock
from pdf_parsing.extraction.api import extract_document
from pdf_parsing.extraction.backends import get_backend
from pdf_parsing.core.models import ExtractionResult

def test_backend_factory():
    backend = get_backend("docling")
    assert backend is not None

def test_extraction_result_validation():
    result = ExtractionResult(
        plaintext="Test",
        pages=["Test"],
        page_count=1,
        confidence=0.9,
        source_path="/tmp/test.pdf",
        ocr_backend="test_backend"
    )
    assert result.plaintext == "Test"

@patch('pdf_parsing.extraction.api.get_backend')
def test_extract_document_calls_backend(mock_get_backend):
    mock_backend = MagicMock()
    mock_get_backend.return_value = mock_backend
    mock_backend.extract.return_value = ExtractionResult(
        plaintext="Mock text",
        pages=["Mock text"],
        page_count=1,
        confidence=1.0,
        source_path="/tmp/test.pdf",
        ocr_backend="mock"
    )

    result = extract_document("/tmp/test.pdf", backend_name="mock")
    
    mock_get_backend.assert_called_once_with("mock")
    mock_backend.extract.assert_called_once_with("/tmp/test.pdf")
    assert result.plaintext == "Mock text"
