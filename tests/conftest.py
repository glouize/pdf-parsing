from __future__ import annotations

import pytest
from sqlmodel import SQLModel, create_engine, Session
from pdf_parsing.core.models import BaseRecord, ExtractionResult, ParseResult

@pytest.fixture
def db_session():
    """In-memory SQLite session for testing."""
    engine = create_engine('sqlite://', echo=False)
    # Import example_invoice models to register tables
    from pdf_parsing.document_types.example_invoice.models import InvoiceHeader, InvoiceLineItem
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture
def sample_extraction_result():
    return ExtractionResult(
        plaintext='Invoice #12345\nVendor: Acme Corp\nDate: 2024-01-15\nTotal: $1,250.00\n\nLine Items:\n1. Widget A - Qty: 10 - $50.00 - $500.00\n2. Widget B - Qty: 5 - $150.00 - $750.00',
        pages=['page 1 text...'],
        page_count=1,
        confidence=0.95,
        source_path='/tmp/test.pdf',
        ocr_backend='docling_default',
    )
