from __future__ import annotations

import pytest
from pdf_parsing.registry import DocumentRegistry, DocumentConfig

def test_registry_discovers_example_invoice():
    registry = DocumentRegistry()
    registry.discover()
    types = registry.list_types()
    assert "example_invoice" in types

def test_registry_get_valid_config():
    registry = DocumentRegistry()
    registry.discover()
    config = registry.get("example_invoice")
    assert isinstance(config, DocumentConfig)
    assert config.name == "example_invoice"

def test_registry_get_nonexistent_raises():
    registry = DocumentRegistry()
    with pytest.raises(KeyError):
        registry.get("nonexistent_type")
