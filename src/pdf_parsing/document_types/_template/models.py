from __future__ import annotations

from sqlmodel import Field

from pdf_parsing.core.models import BaseRecord

# TODO: Subclass BaseRecord to create your document models.
# Make sure to set table=True in your SQLModel classes.
# Example:
# class __DOCUMENT_TYPE_NAME_PASCAL__Header(BaseRecord, table=True):
#     __tablename__ = "your_table_name"
#     some_field: str
