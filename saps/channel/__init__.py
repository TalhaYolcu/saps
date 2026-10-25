"""
SAPS Channel Module
====================

Wireless channel models for the Semantic-Driven Agentic Protocol Stack.

Provides AWGN, Rayleigh, and Rician fading channel simulations for
evaluating mobile AI-agent communication over realistic wireless links.
"""

from .fading import (
    AWGNChannel,
    ChannelModel,
    RayleighChannel,
    RicianChannel,
    calculate_ber,
    calculate_capacity,
)

__all__ = [
    "ChannelModel",
    "AWGNChannel",
    "RayleighChannel",
    "RicianChannel",
    "calculate_ber",
    "calculate_capacity",
]
