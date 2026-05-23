"""
Data service — loads and caches the three JSON datasets.
All node code should access data through this service.
"""
from __future__ import annotations
import json
import os
from functools import lru_cache
from typing import Any, Dict, List

from app.config import settings
from app.utils.logging import get_logger

logger = get_logger(__name__)

_BASE = os.path.join(os.path.dirname(__file__), "..", "..", settings.data_dir)


def _load_json(filename: str) -> Any:
    path = os.path.normpath(os.path.join(_BASE, filename))
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def get_properties() -> List[Dict[str, Any]]:
    data = _load_json("properties.json")
    logger.info(f"Loaded {len(data)} properties from dataset")
    return data


@lru_cache(maxsize=1)
def get_neighborhoods() -> List[Dict[str, Any]]:
    data = _load_json("neighborhoods.json")
    logger.info(f"Loaded {len(data)} neighborhoods from dataset")
    return data


@lru_cache(maxsize=1)
def get_urban_signals() -> List[Dict[str, Any]]:
    data = _load_json("urban_signals.json")
    logger.info(f"Loaded {len(data)} urban signals from dataset")
    return data


def get_neighborhood_by_id(nbhd_id: str) -> Dict[str, Any] | None:
    return next((n for n in get_neighborhoods() if n["id"] == nbhd_id), None)


def get_signals_for_zones(zone_ids: List[str]) -> List[Dict[str, Any]]:
    return [s for s in get_urban_signals() if s.get("neighborhood_id") in zone_ids]
