"""
LangGraph shared state definition for the housing recommendation workflow.
All nodes read from and write to this strongly-typed state.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, TypedDict


class UserCriteria(TypedDict, total=False):
    """Structured preferences extracted from the user's natural language query."""
    city: str
    max_budget: float
    min_budget: float
    property_type: Optional[str]       # None = any type
    min_bedrooms: Optional[int]
    max_bedrooms: Optional[int]
    min_area_m2: Optional[float]
    max_area_m2: Optional[float]
    preferred_zones: List[str]          # neighborhood names / IDs
    max_distance_to_metro_km: Optional[float]
    pet_friendly: Optional[bool]
    min_safety_score: Optional[float]
    min_investment_score: Optional[float]
    min_transport_score: Optional[float]
    required_amenities: List[str]
    lifestyle_tags: List[str]
    stratum_min: Optional[int]
    stratum_max: Optional[int]


class DecisionRecord(TypedDict):
    """Audit trail entry recording what changed and why."""
    iteration: int
    relaxation_level: int
    action: str                 # e.g. "budget_relaxed", "zone_expanded"
    changed_field: str
    old_value: Any
    new_value: Any
    reason: str
    timestamp: str


class HousingState(TypedDict):
    """
    Central shared state flowing through every LangGraph node.
    Each node receives the full state and returns a partial update dict.
    """
    # ── Input ──────────────────────────────────────────────────────────
    user_query: str                             # raw natural language input

    # ── Preference extraction ──────────────────────────────────────────
    original_criteria: Optional[UserCriteria]  # immutable copy of first parse
    current_criteria: Optional[UserCriteria]   # may be relaxed over iterations
    extracted_preferences: Optional[Dict[str, Any]]  # raw LLM output

    # ── Zone analysis ─────────────────────────────────────────────────
    analyzed_zones: List[Dict[str, Any]]        # all scored neighborhoods
    selected_zones: List[str]                   # neighborhood IDs to search

    # ── External signals ──────────────────────────────────────────────
    external_signals: List[Dict[str, Any]]      # urban context for selected zones

    # ── Property pipeline ─────────────────────────────────────────────
    raw_properties: List[Dict[str, Any]]        # retrieved from dataset
    filtered_properties: List[Dict[str, Any]]   # after strict filter pass
    scored_properties: List[Dict[str, Any]]     # with computed scores

    # ── Evaluation & iteration ────────────────────────────────────────
    recommendation_scores: Dict[str, float]     # prop_id -> final_score
    iteration_count: int
    relaxation_level: int                       # 0 = no relaxation, 4 = max
    failure_reasons: List[str]
    decision_history: List[DecisionRecord]
    is_solution_acceptable: bool
    evaluator_feedback: str

    # ── Output ────────────────────────────────────────────────────────
    final_recommendations: List[Dict[str, Any]]
    error_message: Optional[str]
