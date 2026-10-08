from __future__ import annotations

from datetime import date
from typing import Optional

from sqlmodel import Field, Relationship

from pdf_parsing.core.models import BaseRecord

class InvoiceHeader(BaseRecord, table=True):
    vendor_name: str
    invoice_number: str
    invoice_date: Optional[date] = None
    due_date: Optional[date] = None
    total_amount: float
    currency: str
    notes: Optional[str] = None
    
    line_items: list["InvoiceLineItem"] = Relationship(back_populates="header")

class InvoiceLineItem(BaseRecord, table=True):
    header_id: Optional[int] = Field(default=None, foreign_key="invoiceheader.id")
    description: str
    quantity: float
    unit_price: float
    line_total: float
    
    header: Optional[InvoiceHeader] = Relationship(back_populates="line_items")
