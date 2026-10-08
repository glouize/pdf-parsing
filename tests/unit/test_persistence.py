from __future__ import annotations

from sqlmodel import Session, select
from pdf_parsing.document_types.example_invoice.models import InvoiceHeader, InvoiceLineItem
from pdf_parsing.persistence.api import save_record

def test_insert_parent_record(db_session: Session):
    header = InvoiceHeader(
        invoice_number="INV-001",
        vendor_name="Test Vendor",
        date="2023-01-01",
        total_amount=100.0,
        source_document_id="doc123",
        extracted_at="2023-01-01T12:00:00Z"
    )
    
    db_session.add(header)
    db_session.commit()
    
    saved = db_session.exec(select(InvoiceHeader)).first()
    assert saved is not None
    assert saved.invoice_number == "INV-001"
    assert saved.source_document_id == "doc123"

def test_insert_parent_with_child_records(db_session: Session):
    header = InvoiceHeader(
        invoice_number="INV-002",
        vendor_name="Vendor 2",
        date="2023-01-02",
        total_amount=200.0,
        source_document_id="doc456",
        extracted_at="2023-01-01T12:00:00Z"
    )
    db_session.add(header)
    db_session.commit()
    
    line1 = InvoiceLineItem(
        description="Item 1",
        quantity=2.0,
        unit_price=50.0,
        line_total=100.0,
        invoice_id=header.id
    )
    line2 = InvoiceLineItem(
        description="Item 2",
        quantity=1.0,
        unit_price=100.0,
        line_total=100.0,
        invoice_id=header.id
    )
    db_session.add(line1)
    db_session.add(line2)
    db_session.commit()
    
    lines = db_session.exec(select(InvoiceLineItem).where(InvoiceLineItem.invoice_id == header.id)).all()
    assert len(lines) == 2
