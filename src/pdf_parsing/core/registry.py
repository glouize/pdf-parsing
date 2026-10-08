from __future__ import annotations

import importlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import structlog
import yaml

from pdf_parsing.config import settings

logger = structlog.get_logger(__name__)

@dataclass
class DocumentTypeConfig:
    name: str
    version: str
    ocr_backend: str
    llm_provider: str
    llm_model: str
    prompt_template: str
    confidence_threshold: float
    max_retries: int
    retry_on_validation_error: bool
    tables: dict
    prompt_text: str = ""
    parent_model: type | None = None
    child_models: list[type] = field(default_factory=list)
    hooks_module: Any = None


class DocumentTypeRegistry:
    def __init__(self) -> None:
        self._types: dict[str, DocumentTypeConfig] = {}

    def discover(self, base_dir: Path | None = None) -> None:
        if base_dir is None:
            base_dir = settings.document_types_dir

        if not base_dir.exists():
            return

        for path in base_dir.iterdir():
            if not path.is_dir() or path.name.startswith("_"):
                continue

            config_file = path / "config.yaml"
            if not config_file.exists():
                continue

            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config_data = yaml.safe_load(f)
                
                config = DocumentTypeConfig(**config_data)
                
                # Import models
                models_module_name = f"pdf_parsing.document_types.{path.name}.models"
                try:
                    models_module = importlib.import_module(models_module_name)
                    parent_model_name = config.tables.get("parent")
                    if parent_model_name:
                        config.parent_model = getattr(models_module, parent_model_name, None)
                    
                    for child_name in config.tables.get("children", []):
                        child_model = getattr(models_module, child_name, None)
                        if child_model:
                            config.child_models.append(child_model)
                except ImportError as e:
                    logger.warning("Failed to import models", doc_type=path.name, error=str(e))
                
                # Import prompts
                prompts_module_name = f"pdf_parsing.document_types.{path.name}.prompts"
                if ":" in config.prompt_template:
                    mod_ref, var_ref = config.prompt_template.split(":", 1)
                    if mod_ref == "prompts":
                        try:
                            prompts_module = importlib.import_module(prompts_module_name)
                            config.prompt_text = getattr(prompts_module, var_ref, "")
                        except ImportError as e:
                            logger.warning("Failed to import prompts", doc_type=path.name, error=str(e))
                
                # Import hooks
                hooks_module_name = f"pdf_parsing.document_types.{path.name}.hooks"
                try:
                    config.hooks_module = importlib.import_module(hooks_module_name)
                except ImportError:
                    pass # Hooks are optional
                
                self.register(config)
            except Exception as e:
                logger.warning("Failed to load document type", doc_type=path.name, error=str(e))

    def get(self, name: str) -> DocumentTypeConfig:
        if name not in self._types:
            raise KeyError(f"Document type '{name}' not found.")
        return self._types[name]

    def list_types(self) -> list[str]:
        return list(self._types.keys())

    def register(self, config: DocumentTypeConfig) -> None:
        self._types[config.name] = config

registry = DocumentTypeRegistry()
registry.discover()
