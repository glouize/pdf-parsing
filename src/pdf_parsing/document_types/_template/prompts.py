from __future__ import annotations

SYSTEM_PROMPT = """
You are an expert at extracting information from documents.
Please extract the structured data according to the schema.

Document context:
{{ context }}

Plaintext:
{{ plaintext }}

Schema:
{{ schema_description }}
"""
