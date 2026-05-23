"""
Pure scoring utilities — no LLM calls, fully deterministic.
These helpers are called by ScorePropertiesNode.
"""
from __future__ import annotations
import math
from typing import Any, Dict, List, Optional


def budget_score(price: float, max_budget: float, min_budget: float = 0) -> float:
    """
    Returns 1.0 when price is exactly at the sweet spot (80% of max_budget).
    Decays smoothly toward 0 as the price approaches or exceeds max_budget.
    Below min_budget also gets partial score (user might prefer mid-range).
    """
    if max_budget <= 0:
        return 0.5
    # Ideal target: 80% of max budget
    ideal = max_budget * 0.80
    if price <= ideal:
        # Scale from min_budget to ideal
        t = (price - min_budget) / max(ideal - min_budget, 1)
        return min(1.0, 0.6 + 0.4 * t)
    elif price <= max_budget:
        # Slight penalty for being close to ceiling
        ratio = (price - ideal) / (max_budget - ideal)
        return max(0.4, 1.0 - 0.6 * ratio)
    else:
        # Over budget — exponential decay
        over = (price - max_budget) / max_budget
        return max(0.0, 1.0 - 2.5 * over)


def area_score(area: float, min_area: float = 50, ideal_area: float = 80) -> float:
    """Rewards properties meeting or exceeding the minimum area requirement."""
    if area >= ideal_area:
        return 1.0
    if area >= min_area:
        return 0.7 + 0.3 * (area - min_area) / (ideal_area - min_area)
    # Below minimum
    deficit = (min_area - area) / min_area
    return max(0.0, 0.7 - deficit * 1.2)


def transport_score_fn(distance_km: float, max_distance_km: float = 1.5) -> float:
    """Closer to metro = higher score. Exponential decay beyond threshold."""
    if distance_km <= 0.3:
        return 1.0
    if distance_km <= max_distance_km:
        return 1.0 - 0.4 * (distance_km / max_distance_km)
    # Beyond threshold: steeper penalty
    over = distance_km - max_distance_km
    return max(0.0, 0.6 - 0.2 * over)


def location_score(
    zone_safety: float,
    neighborhood_score: float = 0.7,
    preferred_zones: Optional[List[str]] = None,
    neighborhood_id: str = "",
) -> float:
    """Combines safety score with zone preference bonus."""
    base = (zone_safety * 0.6 + neighborhood_score * 0.4)
    # Bonus if property is in a preferred zone
    if preferred_zones and neighborhood_id in preferred_zones:
        base = min(1.0, base + 0.15)
    return round(base, 4)


def investment_score_fn(inv_score: float, urban_growth: float = 0.5) -> float:
    """Blends property-level investment score with broader urban growth signal."""
    return round(inv_score * 0.7 + urban_growth * 0.3, 4)


def compute_final_score(
    b_score: float,
    l_score: float,
    a_score: float,
    t_score: float,
    i_score: float,
    s_score: float,
) -> float:
    """
    Weighted composite score per specification:
      0.30 * budget + 0.20 * location + 0.15 * area +
      0.15 * transport + 0.10 * investment + 0.10 * semantic
    """
    return round(
        0.30 * b_score
        + 0.20 * l_score
        + 0.15 * a_score
        + 0.15 * t_score
        + 0.10 * i_score
        + 0.10 * s_score,
        4,
    )


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    if not vec_a or not vec_b:
        return 0.5
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return round(dot / (norm_a * norm_b), 4)


def criteria_satisfaction(
    prop: Dict[str, Any],
    criteria: Dict[str, Any],
) -> float:
    """
    Returns a percentage [0, 1] of how many stated criteria the property satisfies.
    Only counts criteria that were actually set (non-None).
    """
    checks: List[bool] = []

    if criteria.get("max_budget"):
        checks.append(prop["price"] <= criteria["max_budget"] * 1.05)  # 5% grace
    if criteria.get("min_bedrooms"):
        checks.append(prop["bedrooms"] >= criteria["min_bedrooms"])
    if criteria.get("min_area_m2"):
        checks.append(prop["area_m2"] >= criteria["min_area_m2"] * 0.9)
    if criteria.get("max_distance_to_metro_km"):
        checks.append(prop["distance_to_metro_km"] <= criteria["max_distance_to_metro_km"] * 1.2)
    if criteria.get("pet_friendly") is True:
        checks.append(prop.get("pet_friendly", False) is True)
    if criteria.get("min_safety_score"):
        checks.append(prop["zone_safety_score"] >= criteria["min_safety_score"] * 0.9)
    if criteria.get("property_type"):
        checks.append(prop["property_type"].lower() == criteria["property_type"].lower())
    if criteria.get("preferred_zones"):
        checks.append(prop["neighborhood_id"] in criteria["preferred_zones"])

    if not checks:
        return 1.0
    return round(sum(checks) / len(checks), 3)
