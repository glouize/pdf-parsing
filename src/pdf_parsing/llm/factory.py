from __future__ import annotations

from pdf_parsing.config import settings
from pdf_parsing.llm.base import LlmClient
from pdf_parsing.llm.openai import OpenAIClient
from pdf_parsing.llm.anthropic import AnthropicClient

def get_llm_client(provider: str | None = None, model: str | None = None) -> LlmClient:
    """Get the appropriate LLM client based on provider."""
    # Assuming settings has LLM_PROVIDER, OPENAI_API_KEY, etc.
    # Fallbacks if not provided directly
    provider = provider or getattr(settings, "LLM_PROVIDER", "openai")
    
    if provider == 'openai':
        model = model or getattr(settings, "OPENAI_MODEL", "gpt-4o")
        api_key = getattr(settings, "OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError("OpenAI API key is missing")
        return OpenAIClient(api_key=api_key, model=model)
        
    elif provider == 'anthropic':
        model = model or getattr(settings, "ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        api_key = getattr(settings, "ANTHROPIC_API_KEY", "")
        if not api_key:
            raise ValueError("Anthropic API key is missing")
        return AnthropicClient(api_key=api_key, model=model)
        
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
