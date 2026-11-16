"""
SAPS Channel Module
====================

Wireless channel models for the Semantic-Driven Agentic Protocol Stack.

Provides AWGN, Rayleigh, and Rician fading channel simulations, plus
NVIDIA Sionna 5G/6G channel model integration.
"""

from .fading import (
    AWGNChannel,
    ChannelModel,
    RayleighChannel,
    RicianChannel,
    calculate_ber,
    calculate_capacity,
)
from .sionna_channel import (
    SIONNA_AVAILABLE,
    SionnaAWGNChannel,
    SionnaFlatFadingChannel,
    Sionna3GPPChannel,
)

__all__ = [
    "ChannelModel",
    "AWGNChannel",
    "RayleighChannel",
    "RicianChannel",
    "calculate_ber",
    "calculate_capacity",
    "SIONNA_AVAILABLE",
    "SionnaAWGNChannel",
    "SionnaFlatFadingChannel",
    "Sionna3GPPChannel",
]
