"""
Node 6 — ScorePropertiesNode
Computes the hybrid recommendation score for every filtered property.

final_score = 0.30 * budget + 0.20 * location + 0.15 * area +
              0.15 * transport + 0.10 * investment + 0.10 * semantic
"""
from __future__ import annotations
from typing import Any, Dict, List

from app.models.state import HousingState
from app.services.embedding_service import encode_single, encode_texts
from app.utils.logging import get_logger, log_node_entry, log_node_exit
from app.utils.scoring import (
    area_score,
    budget_score,
    compute_final_score,
    cosine_similarity,
    investment_score_fn,
    location_score,
    transport_score_fn,
)

logger = get_logger(__name__)


def _zone_growth(external_signals: List[Dict[str, Any]], neighborhood_id: str) -> float:
    """Returns the average urban_growth_score for signals in a neighbourhood."""
    relevant = [s for s in external_signals if s.get("neighborhood_id") == neighborhood_id]
    if not relevant:
        return 0.5
    return sum(s["urban_growth_score"] for s in relevant) / len(relevant)


async def score_properties_node(state: HousingState) -> Dict[str, Any]:
    """
    LangGraph node: ScorePropertiesNode.
    Ranks filtered properties using the hybrid scoring formula.
    """
    log_node_entry(logger, "ScorePropertiesNode", state.get("iteration_count", 0))

    criteria: Dict[str, Any] = state.get("current_criteria") or {}
    filtered: List[Dict[str, Any]] = state.get("filtered_properties", [])
    analyzed_zones: List[Dict[str, Any]] = state.get("analyzed_zones", [])
    external_signals: List[Dict[str, Any]] = state.get("external_signals", [])
    user_query: str = state.get("user_query", "")

    if not filtered:
        return {"scored_properties": [], "recommendation_scores": {}}

    # Pre-compute neighbourhood compatibility map
    zone_compat: Dict[str, float] = {
        z["id"]: z.get("compatibility_score", 0.5) for z in analyzed_zones
    }
    preferred_zones: List[str] = criteria.get("preferred_zones", []) or []
    max_budget: float = criteria.get("max_budget") or 0
    min_budget: float = criteria.get("min_budget") or 0
    min_area: float = criteria.get("min_area_m2") or 50
    max_metro: float = criteria.get("max_distance_to_metro_km") or 1.5

    # Batch-encode all property descriptions + the user query for semantic similarity
    texts = [p["description"] for p in filtered]
    prop_embeddings = encode_texts(texts)
    query_embedding = encode_single(user_query)

    scored: List[Dict[str, Any]] = []
    score_map: Dict[str, float] = {}

    for idx, prop in enumerate(filtered):
        nbhd_id = prop.get("neighborhood_id", "")

        b = budget_score(prop["price"], max_budget or prop["price"] * 1.2, min_budget)
        l = location_score(
            prop["zone_safety_score"],
            zone_compat.get(nbhd_id, 0.5),
            preferred_zones,
            nbhd_id,
        )
        a = area_score(prop["area_m2"], min_area, max(min_area * 1.5, 70))
        t = transport_score_fn(prop["distance_to_metro_km"], max_metro or 1.5)
        i = investment_score_fn(
            prop["investment_score"],
            _zone_growth(external_signals, nbhd_id),
        )

        # Semantic similarity
        p_vec = prop_embeddings[idx] if idx < len(prop_embeddings) else []
        s = cosine_similarity(query_embedding, p_vec) if (query_embedding and p_vec) else 0.5
        # Normalise cosine from [-1,1] → [0,1]
        s = (s + 1) / 2

        final = compute_final_score(b, l, a, t, i, s)

        scored.append({
            **prop,
            "scores": {
                "final_score": final,
                "budget_score": round(b, 4),
                "location_score": round(l, 4),
                "area_score": round(a, 4),
                "transport_score": round(t, 4),
                "investment_score": round(i, 4),
                "semantic_score": round(s, 4),
            },
        })
        score_map[prop["id"]] = final

    # Sort descending by final score
    scored.sort(key=lambda p: p["scores"]["final_score"], reverse=True)

    log_node_exit(
        logger,
        "ScorePropertiesNode",
        f"scored {len(scored)} properties — top score={scored[0]['scores']['final_score'] if scored else 0}",
    )

    return {
        "scored_properties": scored,
        "recommendation_scores": score_map,
    }
