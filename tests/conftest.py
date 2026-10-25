"""Shared pytest fixtures for the SAPS test suite."""

import sys
from pathlib import Path
import numpy as np
import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from saps.utils import load_config


@pytest.fixture
def sample_config():
    """Load default simulation config dictionary."""
    cfg_path = _PROJECT_ROOT / "config" / "simulation_config.yaml"
    return load_config(str(cfg_path))


@pytest.fixture
def sample_latent_vector():
    """Deterministic 256-dim latent vector."""
    rng = np.random.default_rng(seed=42)
    return rng.normal(size=256).astype(np.float32)


@pytest.fixture
def sample_kv_cache():
    """Synthetic Key-Value cache tensor."""
    rng = np.random.default_rng(seed=42)
    k = rng.normal(size=(2, 4, 32, 64)).astype(np.float32)
    v = rng.normal(size=(2, 4, 32, 64)).astype(np.float32)
    return k, v
