"""
Conditional edge functions for the LangGraph housing recommendation workflow.
Each function receives the current state and returns the name of the next node.
"""
from __future__ import annotations
from typing import Literal

from app.config import settings
from app.models.state import HousingState


def route_after_evaluation(
    state: HousingState,
) -> Literal["final_recommendation", "failure_diagnosis"]:
    """
    Route from EvaluateResultsNode:
      - If solution is acceptable → produce final recommendations
      - Else → diagnose failure and relax constraints
    """
    if state.get("is_solution_acceptable", False):
        return "final_recommendation"
    return "failure_diagnosis"


def should_continue_relaxation(
    state: HousingState,
) -> Literal["retrieve_properties", "final_recommendation"]:
    """
    Route from RelaxConstraintsNode:
      - If we haven't hit the max iteration limit → retry retrieval
      - Else → force final output with best available results
    """
    iteration = state.get("iteration_count", 0)
    if iteration < settings.max_iterations:
        return "retrieve_properties"
    return "final_recommendation"
