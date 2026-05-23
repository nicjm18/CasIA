"""
Node 5 — FilterPropertiesNode
Applies strict filtering, removes duplicates, and drops low-relevance properties.
Deterministic — no LLM calls.
"""
from __future__ import annotations
from typing import Any, Dict, List, Set

from app.models.state import HousingState
from app.utils.logging import get_logger, log_node_entry, log_node_exit

logger = get_logger(__name__)

# Grace margins applied during strict filtering
BUDGET_GRACE = 1.05        # 5% over max budget still considered
AREA_GRACE = 0.90          # 10% under min area still considered
METRO_GRACE = 1.20         # 20% farther from metro still considered
SAFETY_GRACE = 0.90        # 10% below minimum safety still considered


async def filter_properties_node(state: HousingState) -> Dict[str, Any]:
    """
    LangGraph node: FilterPropertiesNode.
    Applies strict criteria, deduplicates, and removes irrelevant properties.
    """
    log_node_entry(logger, "FilterPropertiesNode", state.get("iteration_count", 0))

    criteria: Dict[str, Any] = state.get("current_criteria") or {}
    raw: List[Dict[str, Any]] = state.get("raw_properties", [])

    max_budget = criteria.get("max_budget")
    min_budget = criteria.get("min_budget", 0) or 0
    min_beds = criteria.get("min_bedrooms")
    min_area = criteria.get("min_area_m2")
    max_area = criteria.get("max_area_m2")
    max_metro = criteria.get("max_distance_to_metro_km")
    pet_friendly_required = criteria.get("pet_friendly")
    min_safety = criteria.get("min_safety_score")
    stratum_min = criteria.get("stratum_min")
    stratum_max = criteria.get("stratum_max")
    required_amenities: List[str] = criteria.get("required_amenities", []) or []

    seen_ids: Set[str] = set()
    filtered: List[Dict[str, Any]] = []

    for prop in raw:
        pid = prop["id"]

        # Deduplicate
        if pid in seen_ids:
            continue
        seen_ids.add(pid)

        # Budget (strict with small grace)
        if max_budget and prop["price"] > max_budget * BUDGET_GRACE:
            continue
        if prop["price"] < min_budget:
            continue

        # Bedrooms
        if min_beds and prop["bedrooms"] < min_beds:
            continue

        # Area
        if min_area and prop["area_m2"] < min_area * AREA_GRACE:
            continue
        if max_area and prop["area_m2"] > max_area:
            continue

        # Metro distance
        if max_metro and prop["distance_to_metro_km"] > max_metro * METRO_GRACE:
            continue

        # Pet friendly
        if pet_friendly_required is True and not prop.get("pet_friendly", False):
            continue

        # Safety
        if min_safety and prop["zone_safety_score"] < min_safety * SAFETY_GRACE:
            continue

        # Stratum
        if stratum_min and prop.get("stratum", 0) < stratum_min:
            continue
        if stratum_max and prop.get("stratum", 7) > stratum_max:
            continue

        # Required amenities (case-insensitive partial match)
        if required_amenities:
            prop_amenities_lower = [a.lower() for a in prop.get("amenities", [])]
            has_all = all(
                any(req.lower() in pa for pa in prop_amenities_lower)
                for req in required_amenities
            )
            if not has_all:
                continue

        filtered.append(prop)

    log_node_exit(
        logger,
        "FilterPropertiesNode",
        f"filtered {len(raw)} → {len(filtered)} properties",
    )

    return {"filtered_properties": filtered}
