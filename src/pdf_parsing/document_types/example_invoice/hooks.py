from __future__ import annotations

from typing import Any

from pdf_parsing.document_types.example_invoice.models import InvoiceHeader

def post_parse(records: list[Any]) -> list[Any]:
    """Hook called after parsing to normalize currency codes."""
    for record in records:
        if isinstance(record, InvoiceHeader) and record.currency:
            record.currency = record.currency.upper()
    return records
