"""
LangGraph workflow definition for the housing recommendation system.

Graph topology:
  START
  → parse_preferences
  → analyze_zones
  → external_signals
  → retrieve_properties
  → filter_properties
  → score_properties
  → evaluate_results
     ├─ [acceptable] → final_recommendation → END
     └─ [not acceptable] → failure_diagnosis
                           → relax_constraints
                              ├─ [iter < max] → retrieve_properties  (loop)
                              └─ [iter >= max] → final_recommendation → END
"""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from app.graph.edges import route_after_evaluation, should_continue_relaxation
from app.models.state import HousingState
from app.nodes.analyze_zones import analyze_zones_node
from app.nodes.evaluate_results import evaluate_results_node
from app.nodes.external_signals import external_signals_node
from app.nodes.failure_diagnosis import failure_diagnosis_node
from app.nodes.filter_properties import filter_properties_node
from app.nodes.final_recommendation import final_recommendation_node
from app.nodes.parse_preferences import parse_user_preferences_node
from app.nodes.relax_constraints import relax_constraints_node
from app.nodes.retrieve_properties import retrieve_properties_node
from app.nodes.score_properties import score_properties_node


def build_graph() -> StateGraph:
    """Construct and compile the LangGraph StateGraph."""
    graph = StateGraph(HousingState)

    # ── Register nodes ────────────────────────────────────────────────
    graph.add_node("parse_preferences",    parse_user_preferences_node)
    graph.add_node("analyze_zones",        analyze_zones_node)
    graph.add_node("external_signals",     external_signals_node)
    graph.add_node("retrieve_properties",  retrieve_properties_node)
    graph.add_node("filter_properties",    filter_properties_node)
    graph.add_node("score_properties",     score_properties_node)
    graph.add_node("evaluate_results",     evaluate_results_node)
    graph.add_node("failure_diagnosis",    failure_diagnosis_node)
    graph.add_node("relax_constraints",    relax_constraints_node)
    graph.add_node("final_recommendation", final_recommendation_node)

    # ── Static edges (linear pipeline) ───────────────────────────────
    graph.add_edge(START,                  "parse_preferences")
    graph.add_edge("parse_preferences",    "analyze_zones")
    graph.add_edge("analyze_zones",        "external_signals")
    graph.add_edge("external_signals",     "retrieve_properties")
    graph.add_edge("retrieve_properties",  "filter_properties")
    graph.add_edge("filter_properties",    "score_properties")
    graph.add_edge("score_properties",     "evaluate_results")

    # ── Conditional edge: evaluate → (final | diagnose) ──────────────
    graph.add_conditional_edges(
        "evaluate_results",
        route_after_evaluation,
        {
            "final_recommendation": "final_recommendation",
            "failure_diagnosis":    "failure_diagnosis",
        },
    )

    # ── Retry loop: diagnose → relax → retrieve (or force final) ──────
    graph.add_edge("failure_diagnosis",    "relax_constraints")
    graph.add_conditional_edges(
        "relax_constraints",
        should_continue_relaxation,
        {
            "retrieve_properties":  "retrieve_properties",
            "final_recommendation": "final_recommendation",
        },
    )

    # ── Terminal edge ─────────────────────────────────────────────────
    graph.add_edge("final_recommendation", END)

    return graph


def get_compiled_graph():
    """Return the compiled, executable LangGraph app."""
    return build_graph().compile()


# Module-level singleton — compiled once on import
_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = get_compiled_graph()
    return _compiled_graph
