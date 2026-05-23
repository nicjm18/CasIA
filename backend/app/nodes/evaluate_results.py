"""
Node 7 — EvaluateResultsNode
Decides whether the current recommendations are acceptable.
Acceptance criteria:
  - at least MIN_RECOMMENDATIONS properties
  - average final_score > MIN_AVERAGE_SCORE
Deterministic — no LLM calls.
"""
from __future__ import annotations
from typing import Any, Dict, List

from app.config import settings
from app.models.state import HousingState
from app.utils.logging import get_logger, log_node_entry, log_node_exit

logger = get_logger(__name__)


async def evaluate_results_node(state: HousingState) -> Dict[str, Any]:
    """
    LangGraph node: EvaluateResultsNode.
    Sets is_solution_acceptable and produces evaluator_feedback.
    """
    log_node_entry(logger, "EvaluateResultsNode", state.get("iteration_count", 0))

    scored: List[Dict[str, Any]] = state.get("scored_properties", [])
    iteration = state.get("iteration_count", 0)
    max_iter = settings.max_iterations

    feedback_parts: List[str] = []
    is_acceptable = False

    n_results = len(scored)
    min_needed = settings.min_recommendations

    if n_results == 0:
        feedback_parts.append(f"No properties found after filtering and scoring.")
    else:
        avg_score = sum(p["scores"]["final_score"] for p in scored) / n_results
        top_score = scored[0]["scores"]["final_score"]
        feedback_parts.append(
            f"Found {n_results} properties. Avg score: {avg_score:.2%}. Top score: {top_score:.2%}."
        )

        if n_results >= min_needed and avg_score >= settings.min_average_score:
            is_acceptable = True
            feedback_parts.append("Solution is ACCEPTABLE — meets quantity and quality thresholds.")
        elif n_results >= min_needed and avg_score < settings.min_average_score:
            feedback_parts.append(
                f"Quantity OK ({n_results} >= {min_needed}) but average score "
                f"{avg_score:.2%} < threshold {settings.min_average_score:.2%}."
            )
        else:
            feedback_parts.append(
                f"Insufficient results: {n_results} < {min_needed} required."
            )

    # Force acceptance at the last iteration to avoid infinite loops
    if not is_acceptable and iteration >= max_iter - 1:
        is_acceptable = True
        feedback_parts.append(
            f"Reached maximum iterations ({max_iter}). "
            "Returning best available results with relaxed criteria."
        )

    feedback = " ".join(feedback_parts)
    log_node_exit(logger, "EvaluateResultsNode", f"acceptable={is_acceptable} — {feedback}")

    return {
        "is_solution_acceptable": is_acceptable,
        "evaluator_feedback": feedback,
        "iteration_count": iteration + 1,
    }
