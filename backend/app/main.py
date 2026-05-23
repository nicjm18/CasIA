"""
FastAPI application entry point for the Housing Recommendation System.
Exposes four endpoints:
  POST /recommendations   — run the LangGraph workflow
  GET  /properties        — list/search properties
  GET  /neighborhoods     — list all neighborhoods
  GET  /graph-state       — debug: return last graph state summary
"""
from __future__ import annotations
import time
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.graph.workflow import get_graph
from app.models.schemas import (
    GraphStateResponse,
    NeighborhoodSchema,
    PropertySchema,
    RecommendationRequest,
    RecommendationResponse,
    RecommendationItem,
    RelaxationStep,
    ScoreBreakdown,
)
from app.models.state import HousingState
from app.services.data_service import get_neighborhoods, get_properties
from app.utils.logging import get_logger

logger = get_logger(__name__)

# Shared storage for last graph state (for /graph-state debug endpoint)
_last_state: Dict[str, Any] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Pre-warm data caches and embedding model on startup."""
    logger.info("Starting Housing Recommendation System...")
    try:
        get_properties()
        get_neighborhoods()
        logger.info("Data caches warmed successfully")
        # Pre-warm embedding model in background
        from app.services.embedding_service import encode_single
        encode_single("Medellín apartment warmup")
        logger.info("Embedding model warmed successfully")
    except Exception as exc:
        logger.warning(f"Startup warmup warning: {exc}")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="Housing Recommendation System",
    description="AI-powered property recommendations for Medellín using LangGraph + GPT-4o-mini",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────────────────────────────────
# POST /recommendations
# ──────────────────────────────────────────────────────────────────────────


@app.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest) -> RecommendationResponse:
    """
    Run the full LangGraph recommendation workflow for a natural language query.
    Returns ranked property recommendations with scores and explanations.
    """
    start_ms = time.time() * 1000
    logger.info(f"New recommendation request: {request.query[:80]}...")

    # Build initial state
    initial_state: HousingState = {
        "user_query": request.query,
        "original_criteria": None,
        "current_criteria": None,
        "extracted_preferences": None,
        "analyzed_zones": [],
        "selected_zones": [],
        "external_signals": [],
        "raw_properties": [],
        "filtered_properties": [],
        "scored_properties": [],
        "recommendation_scores": {},
        "iteration_count": 0,
        "relaxation_level": 0,
        "failure_reasons": [],
        "decision_history": [],
        "final_recommendations": [],
        "evaluator_feedback": "",
        "is_solution_acceptable": False,
        "error_message": None,
    }

    try:
        graph = get_graph()
        final_state: HousingState = await graph.ainvoke(initial_state)
    except Exception as exc:
        logger.error(f"Graph execution failed: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Recommendation engine error: {str(exc)}")

    # Persist for debug endpoint
    global _last_state
    _last_state = dict(final_state)

    elapsed_ms = time.time() * 1000 - start_ms
    recs = final_state.get("final_recommendations", [])

    # Serialise recommendations
    items: List[RecommendationItem] = []
    for rec in recs:
        prop_data = rec["property"]
        scores_data = rec["scores"]
        items.append(
            RecommendationItem(
                property=PropertySchema(**prop_data),
                scores=ScoreBreakdown(**scores_data),
                explanation=rec.get("explanation", ""),
                criteria_satisfaction_pct=rec.get("criteria_satisfaction_pct", 0.0),
                rank=rec.get("rank", 0),
            )
        )

    history: List[RelaxationStep] = [
        RelaxationStep(**h) for h in final_state.get("decision_history", [])
    ]

    return RecommendationResponse(
        status="success" if items else "partial",
        query=request.query,
        recommendations=items,
        total_found=len(final_state.get("scored_properties", [])),
        iterations_used=final_state.get("iteration_count", 0),
        relaxation_applied=final_state.get("relaxation_level", 0) > 0,
        relaxation_history=history,
        evaluator_feedback=final_state.get("evaluator_feedback", ""),
        processing_time_ms=round(elapsed_ms, 1),
        graph_state_summary={
            "raw_properties": len(final_state.get("raw_properties", [])),
            "filtered_properties": len(final_state.get("filtered_properties", [])),
            "scored_properties": len(final_state.get("scored_properties", [])),
            "selected_zones": final_state.get("selected_zones", []),
            "relaxation_level": final_state.get("relaxation_level", 0),
            "failure_reasons": final_state.get("failure_reasons", []),
        },
    )


# ──────────────────────────────────────────────────────────────────────────
# GET /properties
# ──────────────────────────────────────────────────────────────────────────


@app.get("/properties", response_model=List[PropertySchema])
async def list_properties(
    neighborhood_id: Optional[str] = Query(default=None),
    property_type: Optional[str] = Query(default=None),
    max_price: Optional[float] = Query(default=None),
    min_price: Optional[float] = Query(default=None),
    min_bedrooms: Optional[int] = Query(default=None),
    pet_friendly: Optional[bool] = Query(default=None),
    limit: int = Query(default=50, le=300),
    offset: int = Query(default=0, ge=0),
) -> List[PropertySchema]:
    """List properties with optional filtering parameters."""
    props = get_properties()

    if neighborhood_id:
        props = [p for p in props if p.get("neighborhood_id") == neighborhood_id]
    if property_type:
        props = [p for p in props if p["property_type"].lower() == property_type.lower()]
    if max_price:
        props = [p for p in props if p["price"] <= max_price]
    if min_price:
        props = [p for p in props if p["price"] >= min_price]
    if min_bedrooms:
        props = [p for p in props if p["bedrooms"] >= min_bedrooms]
    if pet_friendly is not None:
        props = [p for p in props if p.get("pet_friendly") == pet_friendly]

    paginated = props[offset: offset + limit]
    return [PropertySchema(**p) for p in paginated]


# ──────────────────────────────────────────────────────────────────────────
# GET /neighborhoods
# ──────────────────────────────────────────────────────────────────────────


@app.get("/neighborhoods", response_model=List[NeighborhoodSchema])
async def list_neighborhoods() -> List[NeighborhoodSchema]:
    """Return all Medellín neighborhoods with scores and metadata."""
    return [NeighborhoodSchema(**n) for n in get_neighborhoods()]


# ──────────────────────────────────────────────────────────────────────────
# GET /graph-state  (debug)
# ──────────────────────────────────────────────────────────────────────────


@app.get("/graph-state", response_model=GraphStateResponse)
async def get_graph_state() -> GraphStateResponse:
    """Return a summary of the last graph execution state (debug endpoint)."""
    if not _last_state:
        raise HTTPException(status_code=404, detail="No graph execution found yet.")
    return GraphStateResponse(
        iteration_count=_last_state.get("iteration_count", 0),
        relaxation_level=_last_state.get("relaxation_level", 0),
        is_solution_acceptable=_last_state.get("is_solution_acceptable", False),
        selected_zones=_last_state.get("selected_zones", []),
        raw_properties_count=len(_last_state.get("raw_properties", [])),
        filtered_properties_count=len(_last_state.get("filtered_properties", [])),
        scored_properties_count=len(_last_state.get("scored_properties", [])),
        failure_reasons=_last_state.get("failure_reasons", []),
        decision_history=_last_state.get("decision_history", []),
        evaluator_feedback=_last_state.get("evaluator_feedback", ""),
        current_criteria=_last_state.get("current_criteria"),
    )


# ──────────────────────────────────────────────────────────────────────────
# Health check
# ──────────────────────────────────────────────────────────────────────────


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
