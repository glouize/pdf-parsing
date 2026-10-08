from __future__ import annotations

from pdf_parsing.config import settings
from pdf_parsing.llm.base import LlmClient
from pdf_parsing.llm.openai import OpenAIClient
from pdf_parsing.llm.anthropic import AnthropicClient
from pdf_parsing.llm.gemini import GeminiClient

def get_llm_client(provider: str | None = None, model: str | None = None) -> LlmClient:
    """Get the appropriate LLM client based on provider."""
    provider = provider or settings.default_llm_provider
    
    if provider == 'openai':
        model = model or settings.default_llm_model
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is missing")
        return OpenAIClient(api_key=settings.openai_api_key, model=model)
        
    elif provider == 'anthropic':
        model = model or settings.default_llm_model
        if not settings.anthropic_api_key:
            raise ValueError("Anthropic API key is missing")
        return AnthropicClient(api_key=settings.anthropic_api_key, model=model)
        
    elif provider == 'gemini':
        model = model or settings.default_llm_model
        if not settings.gemini_api_key:
            raise ValueError("Gemini API key is missing")
        return GeminiClient(api_key=settings.gemini_api_key, model=model)
        
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
