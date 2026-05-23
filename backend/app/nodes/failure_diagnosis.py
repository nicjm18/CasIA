"""
Node 8 — FailureDiagnosisNode
Analyses why the search failed and stores structured failure reasons.
Uses LLM for semantic diagnosis, falls back to rule-based logic.
"""
from __future__ import annotations
import json
from typing import Any, Dict, List

from app.config import settings
from app.models.state import HousingState
from app.services.llm_service import call_llm_text
from app.prompts.templates import FAILURE_DIAGNOSIS_SYSTEM, FAILURE_DIAGNOSIS_USER
from app.utils.logging import get_logger, log_node_entry, log_node_exit

logger = get_logger(__name__)


def _rule_based_diagnosis(
    criteria: Dict[str, Any],
    raw_count: int,
    filtered_count: int,
    scored_count: int,
) -> List[str]:
    """Deterministic fallback when LLM is unavailable."""
    reasons: List[str] = []

    max_budget = criteria.get("max_budget", 0) or 0
    if max_budget < 200_000_000:
        reasons.append("BUDGET_TOO_LOW: Budget below 200M COP limits options significantly in Medellín.")

    if criteria.get("min_area_m2", 0) and criteria["min_area_m2"] > 120:
        reasons.append("AREA_TOO_RESTRICTIVE: Minimum area > 120 m² eliminates most apartments.")

    if criteria.get("max_distance_to_metro_km", 99) < 0.5:
        reasons.append("TRANSPORT_TOO_STRICT: Distance < 0.5 km to metro is very restrictive.")

    preferred = criteria.get("preferred_zones", [])
    if preferred and len(preferred) == 1:
        reasons.append(f"LOCATION_TOO_SPECIFIC: Only one zone ({preferred[0]}) specified.")

    if raw_count > 10 and filtered_count < 3:
        reasons.append("INCOMPATIBLE_CONSTRAINTS: Multiple strict filters combine to eliminate properties.")

    if raw_count < 5:
        reasons.append("INSUFFICIENT_SUPPLY: Very few properties available for selected zones.")

    if not reasons:
        reasons.append("UNKNOWN: Further constraint relaxation may improve results.")

    return reasons


async def failure_diagnosis_node(state: HousingState) -> Dict[str, Any]:
    """
    LangGraph node: FailureDiagnosisNode.
    Diagnoses why the recommendation pipeline produced insufficient results.
    """
    log_node_entry(logger, "FailureDiagnosisNode", state.get("iteration_count", 0))

    criteria = state.get("current_criteria") or {}
    raw_count = len(state.get("raw_properties", []))
    filtered_count = len(state.get("filtered_properties", []))
    scored_count = len(state.get("scored_properties", []))

    # Try LLM diagnosis
    try:
        prompt = (
            FAILURE_DIAGNOSIS_SYSTEM
            + "\n\n"
            + FAILURE_DIAGNOSIS_USER.format(
                result_count=scored_count,
                min_needed=settings.min_recommendations,
                criteria_json=json.dumps(criteria, ensure_ascii=False, indent=2),
                raw_count=raw_count,
                filtered_count=filtered_count,
            )
        )
        llm_response = await call_llm_text(prompt, temperature=0.1)
        reasons = [r.strip() for r in llm_response.strip().splitlines() if r.strip()]
        if not reasons:
            raise ValueError("Empty LLM diagnosis")
    except Exception as exc:
        logger.warning(f"LLM diagnosis failed ({exc}), using rule-based fallback")
        reasons = _rule_based_diagnosis(criteria, raw_count, filtered_count, scored_count)

    log_node_exit(logger, "FailureDiagnosisNode", f"reasons={reasons}")

    return {"failure_reasons": reasons}
