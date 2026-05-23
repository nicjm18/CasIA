"""
Embedding service using sentence-transformers (local, no API calls needed).
Used for semantic similarity scoring between user query and property descriptions.
"""
from __future__ import annotations
from functools import lru_cache
from typing import List

from app.config import settings
from app.utils.logging import get_logger

logger = get_logger(__name__)

# Lazy singleton — model loads on first call to avoid startup cost
_model = None


def _get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedding model: {settings.embedding_model}")
            _model = SentenceTransformer(settings.embedding_model)
            logger.info("Embedding model loaded successfully")
        except ImportError:
            logger.warning("sentence-transformers not installed — falling back to zero-vector embeddings")
            _model = None
    return _model


def encode_texts(texts: List[str]) -> List[List[float]]:
    """
    Encode a list of texts to embedding vectors.
    Returns a list of float lists (one per input text).
    Falls back to empty lists if sentence-transformers is unavailable.
    """
    model = _get_model()
    if model is None:
        return [[] for _ in texts]
    try:
        embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return [emb.tolist() for emb in embeddings]
    except Exception as exc:
        logger.error(f"Embedding encoding failed: {exc}")
        return [[] for _ in texts]


def encode_single(text: str) -> List[float]:
    vecs = encode_texts([text])
    return vecs[0] if vecs else []
