"""
Node 4 — RetrievePropertiesNode
Loads properties from the dataset that broadly match current criteria.
Uses loose pre-filtering to maximise recall before the stricter FilterPropertiesNode.
Deterministic — no LLM calls.
"""
from __future__ import annotations
from typing import Any, Dict, List

from app.models.state import HousingState
from app.services.data_service import get_properties
from app.utils.logging import get_logger, log_node_entry, log_node_exit

logger = get_logger(__name__)

# How much over budget we still retrieve (filter will apply tighter cutoffs)
BUDGET_RETRIEVAL_MARGIN = 1.30


async def retrieve_properties_node(state: HousingState) -> Dict[str, Any]:
    """
    LangGraph node: RetrievePropertiesNode.
    Loads candidate properties matching city, budget, zones, and type.
    """
    log_node_entry(logger, "RetrievePropertiesNode", state.get("iteration_count", 0))

    criteria: Dict[str, Any] = state.get("current_criteria") or {}
    selected_zones: List[str] = state.get("selected_zones", [])
    all_properties = get_properties()

    city = (criteria.get("city") or "Medellín").lower()
    max_budget = criteria.get("max_budget")
    min_budget = criteria.get("min_budget", 0) or 0
    prop_type = criteria.get("property_type")
    min_beds = criteria.get("min_bedrooms")

    candidates: List[Dict[str, Any]] = []

    for prop in all_properties:
        # City filter
        if prop["city"].lower() != city:
            continue

        # Zone filter — if zones selected, property must be in one of them
        if selected_zones and prop.get("neighborhood_id") not in selected_zones:
            continue

        # Budget filter (with generous margin for retrieval)
        if max_budget and prop["price"] > max_budget * BUDGET_RETRIEVAL_MARGIN:
            continue
        if prop["price"] < min_budget * 0.60:
            continue

        # Property type (optional)
        if prop_type and prop["property_type"].lower() != prop_type.lower():
            continue

        # Bedrooms minimum
        if min_beds and prop["bedrooms"] < min_beds - 1:  # allow 1 under for retrieval
            continue

        candidates.append(prop)

    log_node_exit(
        logger,
        "RetrievePropertiesNode",
        f"retrieved {len(candidates)} / {len(all_properties)} properties",
    )

    return {"raw_properties": candidates}
