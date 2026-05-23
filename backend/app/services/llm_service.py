"""
LLM service — wraps OpenRouter/OpenAI-compatible API.
Used only for semantic reasoning; deterministic logic stays in utils/.
"""
from __future__ import annotations
from typing import Any, Dict, Optional, Type

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from app.config import settings
from app.utils.logging import get_logger

logger = get_logger(__name__)


def get_llm(temperature: float = 0.1, max_tokens: int = 2048) -> ChatOpenAI:
    """Return a ChatOpenAI instance pointed at OpenRouter."""
    return ChatOpenAI(
        model=settings.llm_model,
        temperature=temperature,
        max_tokens=max_tokens,
        openai_api_key=settings.openrouter_api_key,
        openai_api_base=settings.openrouter_base_url,
        default_headers={
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Housing Recommendation System",
        },
    )


async def call_llm_structured(
    prompt: str,
    schema: Type[BaseModel],
    temperature: float = 0.0,
) -> Dict[str, Any]:
    """
    Call the LLM and parse the response against a Pydantic schema.
    Returns the schema's dict representation.
    Falls back to an empty dict on failure so the graph can retry.
    """
    llm = get_llm(temperature=temperature)
    structured_llm = llm.with_structured_output(schema)
    try:
        result = await structured_llm.ainvoke(prompt)
        logger.debug(f"LLM structured output: {result}")
        return result.model_dump()
    except Exception as exc:
        logger.error(f"LLM call failed: {exc}")
        raise


async def call_llm_text(prompt: str, temperature: float = 0.3) -> str:
    """Call the LLM and return the raw text response."""
    llm = get_llm(temperature=temperature)
    try:
        response = await llm.ainvoke(prompt)
        return response.content
    except Exception as exc:
        logger.error(f"LLM text call failed: {exc}")
        return ""
