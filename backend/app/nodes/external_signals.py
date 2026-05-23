"""
Node 3 — ExternalSignalsNode
Loads urban signals for the selected zones and attaches context explanations.
Deterministic — no LLM calls.
"""
from __future__ import annotations
from typing import Any, Dict, List

from app.models.state import HousingState
from app.services.data_service import get_signals_for_zones
from app.utils.logging import get_logger, log_node_entry, log_node_exit

logger = get_logger(__name__)


async def external_signals_node(state: HousingState) -> Dict[str, Any]:
    """
    LangGraph node: ExternalSignalsNode.
    Retrieves relevant urban signals for all selected zones.
    """
    log_node_entry(logger, "ExternalSignalsNode", state.get("iteration_count", 0))

    selected_zones: List[str] = state.get("selected_zones", [])
    signals = get_signals_for_zones(selected_zones)

    # Enrich each signal with a readability label
    enriched: List[Dict[str, Any]] = []
    for sig in signals:
        enriched.append({
            **sig,
            "impact_label": "Positive signal" if sig["impact"] == "positive" else (
                "Caution signal" if sig["impact"] == "negative" else "Neutral signal"
            ),
            "relevance": "high" if sig["urban_growth_score"] >= 0.70 else (
                "medium" if sig["urban_growth_score"] >= 0.50 else "low"
            ),
        })

    # Sort by urban_growth_score descending
    enriched.sort(key=lambda s: s["urban_growth_score"], reverse=True)

    log_node_exit(
        logger,
        "ExternalSignalsNode",
        f"loaded {len(enriched)} signals for zones {selected_zones}",
    )

    return {"external_signals": enriched}
