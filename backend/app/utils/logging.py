"""Structured logging setup for the housing recommendation system."""
import io
import logging
import sys
from typing import Any


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        # Use a UTF-8 stream wrapper so special chars work on Windows
        stream = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        handler = logging.StreamHandler(stream)
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    return logger


def log_node_entry(logger: logging.Logger, node_name: str, iteration: int) -> None:
    logger.info(f"[{node_name}] ENTER - iteration={iteration}")


def log_node_exit(logger: logging.Logger, node_name: str, result_summary: Any) -> None:
    logger.info(f"[{node_name}] EXIT  - {result_summary}")
