"""
Node 1 — ParseUserPreferencesNode
Parses the natural language query into a structured UserCriteria dict.
Uses GPT-4o-mini with Pydantic structured output via LangChain.
"""
from __future__ import annotations
import copy
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.models.state import HousingState
from app.prompts.templates import PARSE_PREFERENCES_SYSTEM, PARSE_PREFERENCES_USER
from app.services.llm_service import call_llm_structured
from app.utils.logging import get_logger, log_node_entry, log_node_exit

logger = get_logger(__name__)


class ExtractedPreferences(BaseModel):
    """Pydantic schema used for LLM structured output."""
    city: str = Field(default="Medellín")
    max_budget: Optional[float] = Field(default=None, description="Maximum budget in COP")
    min_budget: Optional[float] = Field(default=None, description="Minimum budget in COP")
    property_type: Optional[str] = Field(default=None, description="Apartamento, Casa, Penthouse, etc.")
    min_bedrooms: Optional[int] = Field(default=None, ge=0)
    max_bedrooms: Optional[int] = Field(default=None, ge=0)
    min_area_m2: Optional[float] = Field(default=None, description="Minimum area in square metres")
    max_area_m2: Optional[float] = Field(default=None)
    preferred_zones: List[str] = Field(default_factory=list, description="Neighbourhood IDs")
    max_distance_to_metro_km: Optional[float] = Field(default=None)
    pet_friendly: Optional[bool] = Field(default=None)
    min_safety_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    min_investment_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    min_transport_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    required_amenities: List[str] = Field(default_factory=list)
    lifestyle_tags: List[str] = Field(default_factory=list)
    stratum_min: Optional[int] = Field(default=None, ge=1, le=6)
    stratum_max: Optional[int] = Field(default=None, ge=1, le=6)


async def parse_user_preferences_node(state: HousingState) -> Dict[str, Any]:
    """
    LangGraph node: ParseUserPreferencesNode.
    Converts free-text query → structured UserCriteria.
    """
    log_node_entry(logger, "ParseUserPreferencesNode", state.get("iteration_count", 0))

    query = state["user_query"]
    prompt = (
        PARSE_PREFERENCES_SYSTEM
        + "\n\n"
        + PARSE_PREFERENCES_USER.format(query=query)
    )

    try:
        raw = await call_llm_structured(prompt, ExtractedPreferences, temperature=0.0)
    except Exception as exc:
        logger.error(f"Preference extraction failed: {exc}")
        # Provide safe defaults so the graph can continue with relaxed criteria
        raw = {
            "city": "Medellín",
            "max_budget": 600_000_000,
            "min_budget": 100_000_000,
            "property_type": None,
            "min_bedrooms": None,
            "preferred_zones": [],
            "lifestyle_tags": [],
            "required_amenities": [],
        }

    # Infer min_budget from max_budget if absent
    if raw.get("max_budget") and not raw.get("min_budget"):
        raw["min_budget"] = raw["max_budget"] * 0.40

    criteria: Dict[str, Any] = {k: v for k, v in raw.items() if v is not None and v != []}

    log_node_exit(
        logger,
        "ParseUserPreferencesNode",
        f"budget={criteria.get('max_budget')}, zones={criteria.get('preferred_zones')}",
    )

    return {
        "extracted_preferences": raw,
        "original_criteria": copy.deepcopy(criteria),
        "current_criteria": criteria,
    }
