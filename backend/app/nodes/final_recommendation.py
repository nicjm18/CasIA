"""
Node 10 — FinalRecommendationNode
Generates the final ranked recommendation list with LLM-written explanations.
Uses GPT-4o-mini to write personalised property explanations.
"""
from __future__ import annotations
import asyncio
from typing import Any, Dict, List

from app.config import settings
from app.models.state import HousingState
from app.prompts.templates import FINAL_RECOMMENDATION_SYSTEM, FINAL_RECOMMENDATION_USER
from app.services.llm_service import call_llm_text
from app.utils.logging import get_logger, log_node_entry, log_node_exit
from app.utils.scoring import criteria_satisfaction

logger = get_logger(__name__)

TOP_N = 5  # Maximum recommendations to return
MAX_CONCURRENT_LLM = 3  # Rate-limit concurrent explanation calls


async def _generate_explanation(
    prop: Dict[str, Any],
    query: str,
    final_score: float,
) -> str:
    """Generate a personalised explanation for a single property."""
    amenities_str = ", ".join(prop.get("amenities", [])[:5]) or "standard"
    prompt = (
        FINAL_RECOMMENDATION_SYSTEM
        + "\n\n"
        + FINAL_RECOMMENDATION_USER.format(
            title=prop["title"],
            property_type=prop["property_type"],
            neighborhood=prop["neighborhood"],
            price=prop["price"],
            area=prop["area_m2"],
            bedrooms=prop["bedrooms"],
            bathrooms=prop["bathrooms"],
            metro_dist=prop["distance_to_metro_km"],
            safety=prop["zone_safety_score"],
            investment=prop["investment_score"],
            amenities=amenities_str,
            query=query,
            score=final_score,
        )
    )
    explanation = await call_llm_text(prompt, temperature=0.4)
    return explanation.strip() if explanation else _fallback_explanation(prop, final_score)


def _fallback_explanation(prop: Dict[str, Any], score: float) -> str:
    """Rule-based explanation when LLM is unavailable."""
    parts = [
        f"Este {prop['property_type'].lower()} en {prop['neighborhood']} "
        f"ofrece {prop['area_m2']} m² a ${prop['price']:,.0f} COP."
    ]
    if prop["distance_to_metro_km"] < 1.0:
        parts.append(f"Excelente acceso al metro ({prop['distance_to_metro_km']} km).")
    if prop["zone_safety_score"] > 0.8:
        parts.append("Zona de alta seguridad.")
    if prop["investment_score"] > 0.8:
        parts.append("Alto potencial de valorización.")
    parts.append(f"Compatibilidad total: {score:.0%}.")
    return " ".join(parts)


async def final_recommendation_node(state: HousingState) -> Dict[str, Any]:
    """
    LangGraph node: FinalRecommendationNode.
    Takes top-N scored properties, generates explanations, and builds the final output.
    """
    log_node_entry(logger, "FinalRecommendationNode", state.get("iteration_count", 0))

    scored: List[Dict[str, Any]] = state.get("scored_properties", [])
    criteria: Dict[str, Any] = state.get("current_criteria") or {}
    original_criteria: Dict[str, Any] = state.get("original_criteria") or {}
    query: str = state.get("user_query", "")

    top_properties = scored[:TOP_N]

    # Generate explanations with concurrency limit
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_LLM)

    async def _limited_explain(prop: Dict[str, Any]) -> str:
        async with semaphore:
            try:
                return await _generate_explanation(prop, query, prop["scores"]["final_score"])
            except Exception as exc:
                logger.warning(f"Explanation generation failed for {prop['id']}: {exc}")
                return _fallback_explanation(prop, prop["scores"]["final_score"])

    explanations = await asyncio.gather(
        *[_limited_explain(p) for p in top_properties]
    )

    # Build final recommendation objects
    final_recs: List[Dict[str, Any]] = []
    for rank, (prop, explanation) in enumerate(zip(top_properties, explanations), start=1):
        satisfaction = criteria_satisfaction(prop, original_criteria)
        final_recs.append({
            "rank": rank,
            "property": {k: v for k, v in prop.items() if k != "scores"},
            "scores": prop["scores"],
            "explanation": explanation,
            "criteria_satisfaction_pct": satisfaction,
        })

    log_node_exit(
        logger,
        "FinalRecommendationNode",
        f"produced {len(final_recs)} recommendations",
    )

    return {"final_recommendations": final_recs}
