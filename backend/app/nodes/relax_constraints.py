"""
Node 9 — RelaxConstraintsNode
Progressively relaxes ONE constraint per iteration following a strict order:
  Level 1: budget +5%
  Level 2: expand to nearby neighbourhoods
  Level 3: reduce minimum area by 15%
  Level 4: relax metro distance threshold by 50%

Maintains full decision history for traceability.
Deterministic — no LLM calls.
"""
from __future__ import annotations
import copy
from datetime import datetime
from typing import Any, Dict, List

from app.models.state import HousingState
from app.utils.logging import get_logger, log_node_entry, log_node_exit

logger = get_logger(__name__)

# Ordered relaxation strategies — index = relaxation_level (1-based)
RELAXATION_STEPS = [
    # (level, label, description)
    (1, "budget_relaxed",        "Budget increased by 5%"),
    (2, "zone_expanded",         "Search expanded to adjacent neighbourhoods"),
    (3, "area_relaxed",          "Minimum area reduced by 15%"),
    (4, "transport_relaxed",     "Maximum metro distance increased by 50%"),
]

# Neighbourhood adjacency map (shared borders / short commute)
ADJACENT_ZONES: Dict[str, List[str]] = {
    "el_poblado":       ["envigado", "laureles", "el_estadio"],
    "laureles":         ["el_estadio", "floresta", "la_america", "belen"],
    "envigado":         ["el_poblado", "sabaneta", "itagui"],
    "sabaneta":         ["envigado", "itagui"],
    "bello":            ["castilla", "aranjuez"],
    "itagui":           ["envigado", "sabaneta", "belen"],
    "robledo":          ["laureles", "la_america"],
    "belen":            ["laureles", "itagui", "la_america"],
    "castilla":         ["bello", "robledo"],
    "floresta":         ["laureles", "la_america"],
    "la_america":       ["laureles", "floresta", "belen"],
    "buenos_aires":     ["manrique", "el_estadio"],
    "manrique":         ["buenos_aires", "castilla"],
    "san_antonio_prado": ["itagui", "belen"],
    "el_estadio":       ["laureles", "la_america", "buenos_aires"],
}


def _expand_zones(current_zones: List[str], analyzed_zones: List[Dict[str, Any]]) -> List[str]:
    """Add neighbours of currently selected zones."""
    expanded = list(current_zones)
    for zone_id in current_zones:
        for adj in ADJACENT_ZONES.get(zone_id, []):
            if adj not in expanded:
                expanded.append(adj)

    # Also add top-scored un-selected zones
    zone_scores = {z["id"]: z.get("compatibility_score", 0) for z in analyzed_zones}
    remaining = sorted(
        [zid for zid in zone_scores if zid not in expanded],
        key=lambda zid: zone_scores[zid],
        reverse=True,
    )
    expanded.extend(remaining[:2])
    return expanded


async def relax_constraints_node(state: HousingState) -> Dict[str, Any]:
    """
    LangGraph node: RelaxConstraintsNode.
    Applies the next relaxation step and records it in decision_history.
    """
    log_node_entry(logger, "RelaxConstraintsNode", state.get("iteration_count", 0))

    criteria: Dict[str, Any] = copy.deepcopy(state.get("current_criteria") or {})
    relaxation_level: int = state.get("relaxation_level", 0)
    history: List[Dict[str, Any]] = list(state.get("decision_history", []))
    analyzed_zones: List[Dict[str, Any]] = state.get("analyzed_zones", [])
    selected_zones: List[str] = list(state.get("selected_zones", []))
    iteration = state.get("iteration_count", 0)

    next_level = relaxation_level + 1
    timestamp = datetime.utcnow().isoformat()
    new_selected_zones = selected_zones  # default: unchanged

    record: Dict[str, Any] = {
        "iteration": iteration,
        "relaxation_level": next_level,
        "action": "no_change",
        "changed_field": "none",
        "old_value": None,
        "new_value": None,
        "reason": "No further relaxation available",
        "timestamp": timestamp,
    }

    if next_level == 1:
        # Relax budget +5%
        old_budget = criteria.get("max_budget")
        if old_budget:
            new_budget = round(old_budget * 1.05)
            criteria["max_budget"] = new_budget
            record.update({
                "action": "budget_relaxed",
                "changed_field": "max_budget",
                "old_value": old_budget,
                "new_value": new_budget,
                "reason": "Insufficient results — budget relaxed by 5%",
            })
            logger.info(f"Budget relaxed: {old_budget:,.0f} -> {new_budget:,.0f} COP")

    elif next_level == 2:
        # Expand to adjacent neighbourhoods
        old_zones = list(selected_zones)
        new_zones = _expand_zones(selected_zones, analyzed_zones)
        new_selected_zones = new_zones
        record.update({
            "action": "zone_expanded",
            "changed_field": "selected_zones",
            "old_value": old_zones,
            "new_value": new_zones,
            "reason": f"Insufficient results — search expanded from {len(old_zones)} to {len(new_zones)} zones",
        })
        logger.info(f"Zones expanded: {old_zones} -> {new_zones}")

    elif next_level == 3:
        # Reduce minimum area by 15%
        old_area = criteria.get("min_area_m2")
        if old_area:
            new_area = round(old_area * 0.85, 1)
            criteria["min_area_m2"] = new_area
            record.update({
                "action": "area_relaxed",
                "changed_field": "min_area_m2",
                "old_value": old_area,
                "new_value": new_area,
                "reason": "Insufficient results — minimum area reduced by 15%",
            })
            logger.info(f"Min area relaxed: {old_area} -> {new_area} m²")

    elif next_level == 4:
        # Relax transport distance by 50%
        old_metro = criteria.get("max_distance_to_metro_km")
        if old_metro:
            new_metro = round(old_metro * 1.5, 2)
            criteria["max_distance_to_metro_km"] = new_metro
            record.update({
                "action": "transport_relaxed",
                "changed_field": "max_distance_to_metro_km",
                "old_value": old_metro,
                "new_value": new_metro,
                "reason": "Insufficient results — metro distance threshold relaxed by 50%",
            })
            logger.info(f"Metro distance relaxed: {old_metro} -> {new_metro} km")

    history.append(record)
    log_node_exit(
        logger,
        "RelaxConstraintsNode",
        f"level={next_level} action={record['action']}",
    )

    return {
        "current_criteria": criteria,
        "relaxation_level": next_level,
        "decision_history": history,
        "selected_zones": new_selected_zones,
    }
