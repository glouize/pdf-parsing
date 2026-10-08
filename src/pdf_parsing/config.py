"""Application-wide configuration using pydantic-settings."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration loaded from environment variables and .env file.

    All settings are prefixed with ``PDF_PARSING_`` in the environment.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PDF_PARSING_",
        extra="ignore",
    )

    # ── Database ──────────────────────────────────────────────────────
    database_url: str = "sqlite:///pdf_parsing.db"

    # ── OCR ───────────────────────────────────────────────────────────
    default_ocr_backend: str = "docling_default"

    # ── LLM ───────────────────────────────────────────────────────────
    default_llm_provider: str = "gemini"
    default_llm_model: str = "gemini-2.5-pro"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""

    # ── Parsing ───────────────────────────────────────────────────────
    default_confidence_threshold: float = 0.85
    max_retries: int = 3

    # ── Paths ─────────────────────────────────────────────────────────
    document_types_dir: Path = Path(__file__).parent / "document_types"

    # ── Dash ──────────────────────────────────────────────────────────
    dash_host: str = "0.0.0.0"
    dash_port: int = 8050
    dash_debug: bool = False

    # ── Prefect ───────────────────────────────────────────────────────
    prefect_api_url: str = ""


settings = Settings()
