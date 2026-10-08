"""Shared data models used across the pipeline."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel


# ── Pipeline data-transfer objects ────────────────────────────────────


class ExtractionResult(BaseModel):
    """Output of the PDF → plaintext extraction stage."""

    plaintext: str
    pages: list[str] = Field(default_factory=list)
    page_count: int = 0
    confidence: float | None = None
    extraction_time_seconds: float = 0.0
    warnings: list[str] = Field(default_factory=list)
    source_path: str = ""
    ocr_backend: str = ""


class ParseResult(BaseModel):
    """Output of the plaintext → structured data parsing stage."""

    records: list[Any] = Field(default_factory=list)
    raw_response: str | None = None
    confidence_score: float | None = None
    model_used: str = ""
    parse_time_seconds: float = 0.0
    prompt_tokens: int | None = None
    completion_tokens: int | None = None


class PipelineResult(BaseModel):
    """End-to-end result of processing a single document."""

    success: bool
    document_type: str
    source_path: str
    record_ids: list[int] = Field(default_factory=list)
    extraction_result: ExtractionResult | None = None
    parse_result: ParseResult | None = None
    error: str | None = None
    processing_time_seconds: float = 0.0


# ── SQL base model ────────────────────────────────────────────────────


class BaseRecord(SQLModel):
    """Base class for all document-type SQL table models.

    Provides common audit fields.  Concrete document types should subclass
    this, add their own columns, and set ``table=True``.
    """

    id: int | None = SQLField(default=None, primary_key=True)
    source_document_id: str = SQLField(
        index=True,
        description="Unique identifier for the source PDF (e.g. file hash).",
    )
    source_file_name: str = SQLField(
        default="",
        description="Original filename of the source PDF.",
    )
    extracted_at: datetime = SQLField(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when this record was extracted.",
    )
    confidence_score: float | None = SQLField(
        default=None,
        description="LLM-reported confidence for this extraction.",
    )
    validated: bool = SQLField(
        default=False,
        description="Whether a human has validated this record.",
    )
