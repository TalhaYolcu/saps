"""
Utility functions for the SAPS simulation framework.

Provides configuration loading, reproducibility seeding, device detection,
execution timing, and structured logging.
"""

from __future__ import annotations

import logging
import random
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import numpy as np
import torch
import yaml


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML configuration file and return it as a dictionary.

    Parameters
    ----------
    path : str | Path
        Absolute or relative path to a ``.yaml`` configuration file.

    Returns
    -------
    dict[str, Any]
        Parsed configuration dictionary.

    Raises
    ------
    FileNotFoundError
        If *path* does not point to an existing file.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        config: dict[str, Any] = yaml.safe_load(fh)
    return config


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------

def set_seed(seed: int) -> None:
    """Set random seeds for Python, NumPy, and PyTorch for reproducibility.

    Parameters
    ----------
    seed : int
        The seed value to use across all RNGs.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True  # type: ignore[attr-defined]
        torch.backends.cudnn.benchmark = False       # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Device Detection
# ---------------------------------------------------------------------------

def get_device() -> torch.device:
    """Return the best available PyTorch device (CUDA → CPU).

    Returns
    -------
    torch.device
        ``torch.device("cuda")`` if a GPU is available, otherwise
        ``torch.device("cpu")``.
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


# ---------------------------------------------------------------------------
# Timer
# ---------------------------------------------------------------------------

class Timer:
    """Context manager for measuring wall-clock execution time.

    Usage
    -----
    >>> with Timer("training loop") as t:
    ...     train()
    >>> print(t.elapsed_ms)

    Attributes
    ----------
    label : str
        Human-readable label printed on exit.
    elapsed_s : float
        Elapsed time in seconds (set after exiting the block).
    elapsed_ms : float
        Elapsed time in milliseconds (set after exiting the block).
    """

    def __init__(self, label: str = "block", logger: logging.Logger | None = None) -> None:
        self.label = label
        self._logger = logger
        self.elapsed_s: float = 0.0
        self.elapsed_ms: float = 0.0
        self._start: float = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *exc: object) -> None:
        self.elapsed_s = time.perf_counter() - self._start
        self.elapsed_ms = self.elapsed_s * 1000.0
        msg = f"[Timer] {self.label}: {self.elapsed_ms:.2f} ms"
        if self._logger:
            self._logger.info(msg)
        else:
            print(msg)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logger(
    name: str = "saps",
    level: int = logging.INFO,
    fmt: str = "%(asctime)s | %(name)-12s | %(levelname)-7s | %(message)s",
) -> logging.Logger:
    """Create and return a configured :class:`logging.Logger`.

    If a handler is already attached to the logger, the function returns the
    existing logger without adding duplicate handlers.

    Parameters
    ----------
    name : str
        Logger name (dot-delimited for hierarchy).
    level : int
        Logging level (e.g. ``logging.DEBUG``).
    fmt : str
        Log message format string.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)
    return logger
