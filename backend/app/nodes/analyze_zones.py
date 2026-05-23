"""
Node 2 — AnalyzeZonesNode
Scores all Medellín neighbourhoods against the user's preferences and
selects the best-matching zones for property retrieval.
Fully deterministic — no LLM calls.
"""
from __future__ import annotations
from typing import Any, Dict, List

from app.models.state import HousingState
from app.services.data_service import get_neighborhoods
from app.utils.logging import get_logger, log_node_entry, log_node_exit

logger = get_logger(__name__)

# Minimum compatibility score to be included in selected zones
ZONE_SCORE_THRESHOLD = 0.45


def _score_neighborhood(nbhd: Dict[str, Any], criteria: Dict[str, Any]) -> float:
    """Compute a 0–1 compatibility score between a neighbourhood and user criteria."""
    weights: Dict[str, float] = {
        "safety": 0.30,
        "transport": 0.25,
        "investment": 0.20,
        "lifestyle": 0.15,
        "price": 0.10,
    }

    scores: Dict[str, float] = {}

    # Safety
    min_safety = criteria.get("min_safety_score", 0.0) or 0.0
    safety = nbhd["safety_score"]
    scores["safety"] = min(1.0, safety / max(min_safety, 0.5)) if min_safety else safety

    # Transport
    min_transport = criteria.get("min_transport_score", 0.0) or 0.0
    transport = nbhd["transport_score"]
    scores["transport"] = min(1.0, transport / max(min_transport, 0.5)) if min_transport else transport

    # Investment
    min_investment = criteria.get("min_investment_score", 0.0) or 0.0
    investment = nbhd["investment_score"]
    scores["investment"] = (
        min(1.0, investment / max(min_investment, 0.4)) if min_investment else investment
    )

    # Lifestyle match
    user_tags = set(criteria.get("lifestyle_tags", []))
    nbhd_tags = set(nbhd.get("lifestyle_tags", []))
    if user_tags:
        overlap = len(user_tags & nbhd_tags) / len(user_tags)
        scores["lifestyle"] = overlap
    else:
        scores["lifestyle"] = 0.7  # neutral when user has no lifestyle preference

    # Price compatibility
    max_budget = criteria.get("max_budget")
    avg_price_m2 = nbhd.get("average_price_m2", 5_000_000)
    if max_budget:
        # Estimate if a typical 70m² flat is affordable
        typical_price = avg_price_m2 * 70
        if typical_price <= max_budget:
            scores["price"] = 1.0
        elif typical_price <= max_budget * 1.3:
            scores["price"] = 0.6
        else:
            scores["price"] = 0.2
    else:
        scores["price"] = 0.7

    total = sum(weights[k] * scores[k] for k in weights)
    return round(total, 4)


async def analyze_zones_node(state: HousingState) -> Dict[str, Any]:
    """
    LangGraph node: AnalyzeZonesNode.
    Produces compatibility-scored neighbourhood list and selects top zones.
    """
    log_node_entry(logger, "AnalyzeZonesNode", state.get("iteration_count", 0))

    criteria = state.get("current_criteria") or {}
    neighborhoods = get_neighborhoods()

    # Score every neighbourhood
    analyzed: List[Dict[str, Any]] = []
    for nbhd in neighborhoods:
        score = _score_neighborhood(nbhd, criteria)
        analyzed.append({
            **nbhd,
            "compatibility_score": score,
        })

    # Sort by compatibility score descending
    analyzed.sort(key=lambda n: n["compatibility_score"], reverse=True)

    # Determine selected zones
    preferred = criteria.get("preferred_zones", [])
    if preferred:
        # Always include explicitly requested zones, then add top-scored ones
        selected_ids = list(preferred)
        for a in analyzed:
            if a["id"] not in selected_ids and a["compatibility_score"] >= ZONE_SCORE_THRESHOLD:
                selected_ids.append(a["id"])
                if len(selected_ids) >= 6:
                    break
    else:
        # Select top zones above threshold (at least top 3)
        above = [a["id"] for a in analyzed if a["compatibility_score"] >= ZONE_SCORE_THRESHOLD]
        selected_ids = above[:6] if above else [a["id"] for a in analyzed[:3]]

    log_node_exit(
        logger,
        "AnalyzeZonesNode",
        f"selected {len(selected_ids)} zones — {selected_ids[:3]}",
    )

    return {
        "analyzed_zones": analyzed,
        "selected_zones": selected_ids,
    }
