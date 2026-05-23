"""Pydantic schemas for API request/response serialisation."""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ── Request ────────────────────────────────────────────────────────────────


class RecommendationRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Natural language description of housing requirements",
        examples=[
            "Necesito un apartamento familiar en Medellín por menos de 450 millones de pesos, "
            "cerca al metro, zona segura y buen potencial de inversión a largo plazo."
        ],
    )


# ── Parsed criteria ────────────────────────────────────────────────────────


class ParsedCriteriaResponse(BaseModel):
    city: str
    max_budget: Optional[float]
    min_budget: Optional[float]
    property_type: Optional[str]
    min_bedrooms: Optional[int]
    min_area_m2: Optional[float]
    preferred_zones: List[str]
    max_distance_to_metro_km: Optional[float]
    pet_friendly: Optional[bool]
    min_safety_score: Optional[float]
    lifestyle_tags: List[str]


# ── Property ───────────────────────────────────────────────────────────────


class PropertySchema(BaseModel):
    id: str
    title: str
    city: str
    neighborhood: str
    neighborhood_id: str
    price: float
    area_m2: float
    bedrooms: int
    bathrooms: int
    parking_spots: int
    property_type: str
    stratum: int
    distance_to_metro_km: float
    description: str
    amenities: List[str]
    pet_friendly: bool
    zone_safety_score: float
    investment_score: float
    transport_score: float
    latitude: float
    longitude: float
    available: bool
    listing_date: str
    price_per_m2: float


# ── Recommendation ─────────────────────────────────────────────────────────


class ScoreBreakdown(BaseModel):
    final_score: float
    budget_score: float
    location_score: float
    area_score: float
    transport_score: float
    investment_score: float
    semantic_score: float


class RecommendationItem(BaseModel):
    property: PropertySchema
    scores: ScoreBreakdown
    explanation: str
    criteria_satisfaction_pct: float
    rank: int


class RelaxationStep(BaseModel):
    iteration: int
    relaxation_level: int
    action: str
    changed_field: str
    old_value: Any
    new_value: Any
    reason: str


class RecommendationResponse(BaseModel):
    status: str                             # "success" | "partial" | "error"
    query: str
    recommendations: List[RecommendationItem]
    total_found: int
    iterations_used: int
    relaxation_applied: bool
    relaxation_history: List[RelaxationStep]
    evaluator_feedback: str
    processing_time_ms: float
    graph_state_summary: Dict[str, Any]


# ── Neighborhood ───────────────────────────────────────────────────────────


class NeighborhoodSchema(BaseModel):
    id: str
    name: str
    city: str
    safety_score: float
    transport_score: float
    investment_score: float
    average_price_m2: float
    lifestyle_tags: List[str]
    green_areas_score: float
    latitude: float
    longitude: float
    description: str
    metro_station: str
    avg_stratum: float


# ── Graph state (debug) ────────────────────────────────────────────────────


class GraphStateResponse(BaseModel):
    iteration_count: int
    relaxation_level: int
    is_solution_acceptable: bool
    selected_zones: List[str]
    raw_properties_count: int
    filtered_properties_count: int
    scored_properties_count: int
    failure_reasons: List[str]
    decision_history: List[Dict[str, Any]]
    evaluator_feedback: str
    current_criteria: Optional[Dict[str, Any]]
