"""Layer 4 — Transport Layer: Intent-Aware Selective Transport Protocol (IA-STP).

Implements selective ARQ based on token entropy: high-entropy (critical)
tokens are retransmitted upon loss; low-entropy (predictable) tokens are
skipped to save bandwidth.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class TokenPacket:
    """A packet wrapping one or more tokens with metadata."""
    packet_id: int
    tokens: np.ndarray               # raw token values or embeddings
    entropy: float                    # Shannon entropy of the token(s)
    is_critical: bool = False         # set by the transport layer
    acknowledged: bool = False
    retransmit_count: int = 0


@dataclass
class TransportStats:
    """Accumulated statistics for an IA-STP session."""
    total_packets: int = 0
    critical_packets: int = 0
    packets_lost: int = 0
    packets_retransmitted: int = 0
    packets_skipped: int = 0
    total_tokens: int = 0
    tokens_skipped: int = 0


class IASTP:
    """Intent-Aware Selective Transport Protocol.

    Parameters
    ----------
    entropy_threshold : float
        Tokens with entropy above this value are considered *critical*.
    max_retransmits : int
        Maximum retransmission attempts for a critical lost packet.
    """

    def __init__(
        self,
        entropy_threshold: float = 1.0,
        max_retransmits: int = 3,
    ) -> None:
        self.entropy_threshold = entropy_threshold
        self.max_retransmits = max_retransmits
        self.stats = TransportStats()
        self._next_id = 0

    # ------------------------------------------------------------------ #
    #  Entropy Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def compute_entropy(probs: np.ndarray) -> float:
        """Compute Shannon entropy of a probability distribution.

        Parameters
        ----------
        probs : np.ndarray
            Probability distribution (must sum to 1, all >= 0).

        Returns
        -------
        float
            Entropy in *nats* (using natural log).
        """
        probs = np.asarray(probs, dtype=np.float64)
        # Filter out zeros to avoid log(0)
        probs = probs[probs > 0]
        return float(-np.sum(probs * np.log(probs)))

    def classify_token(self, entropy: float) -> bool:
        """Return ``True`` if the token is *critical* (high entropy)."""
        return entropy > self.entropy_threshold

    # ------------------------------------------------------------------ #
    #  Packet Creation
    # ------------------------------------------------------------------ #

    def create_packet(self, tokens: np.ndarray, entropy: float) -> TokenPacket:
        """Wrap tokens into a :class:`TokenPacket` with criticality label."""
        pkt = TokenPacket(
            packet_id=self._next_id,
            tokens=tokens,
            entropy=entropy,
            is_critical=self.classify_token(entropy),
        )
        self._next_id += 1
        self.stats.total_packets += 1
        self.stats.total_tokens += int(np.prod(tokens.shape))
        if pkt.is_critical:
            self.stats.critical_packets += 1
        return pkt

    # ------------------------------------------------------------------ #
    #  Selective ARQ
    # ------------------------------------------------------------------ #

    def selective_arq(
        self,
        packet: TokenPacket,
        lost: bool,
    ) -> str:
        """Decide what to do with a (potentially lost) packet.

        Parameters
        ----------
        packet : TokenPacket
            The packet under consideration.
        lost : bool
            Whether the packet was lost in transit.

        Returns
        -------
        str
            One of ``"ack"``, ``"retransmit"``, or ``"skip"``.
        """
        if not lost:
            packet.acknowledged = True
            return "ack"

        self.stats.packets_lost += 1

        if packet.is_critical and packet.retransmit_count < self.max_retransmits:
            packet.retransmit_count += 1
            self.stats.packets_retransmitted += 1
            return "retransmit"

        # Non-critical or exhausted retransmits → skip
        self.stats.packets_skipped += 1
        self.stats.tokens_skipped += int(np.prod(packet.tokens.shape))
        return "skip"

    # ------------------------------------------------------------------ #
    #  Batch Transmission Simulation
    # ------------------------------------------------------------------ #

    def transmit_batch(
        self,
        token_list: List[np.ndarray],
        entropy_list: List[float],
        loss_rate: float = 0.1,
        rng: Optional[np.random.Generator] = None,
    ) -> Tuple[List[TokenPacket], TransportStats]:
        """Simulate transmitting a batch of token packets over a lossy link.

        Parameters
        ----------
        token_list : list of np.ndarray
            Each element is the token data for one packet.
        entropy_list : list of float
            Entropy value for each packet.
        loss_rate : float
            Probability of a packet being lost.
        rng : np.random.Generator, optional
            Random number generator for reproducibility.

        Returns
        -------
        (delivered_packets, stats)
        """
        if rng is None:
            rng = np.random.default_rng(seed=42)

        delivered: List[TokenPacket] = []

        for tokens, entropy in zip(token_list, entropy_list):
            pkt = self.create_packet(tokens, entropy)
            lost = rng.random() < loss_rate
            action = self.selective_arq(pkt, lost)

            # Retry loop for retransmissions
            while action == "retransmit":
                lost = rng.random() < loss_rate
                action = self.selective_arq(pkt, lost)

            if action == "ack":
                delivered.append(pkt)

        return delivered, self.stats

    def get_stats(self) -> TransportStats:
        """Return a copy of the current transport statistics."""
        return TransportStats(
            total_packets=self.stats.total_packets,
            critical_packets=self.stats.critical_packets,
            packets_lost=self.stats.packets_lost,
            packets_retransmitted=self.stats.packets_retransmitted,
            packets_skipped=self.stats.packets_skipped,
            total_tokens=self.stats.total_tokens,
            tokens_skipped=self.stats.tokens_skipped,
        )

    def reset_stats(self) -> None:
        """Reset accumulated statistics."""
        self.stats = TransportStats()
        self._next_id = 0


class TransportLayer:
    """Transport Layer wrapper for the SAPS protocol stack.

    Wraps the Intent-Aware Selective Transport Protocol (IA-STP).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        cfg = config or {}
        tp_cfg = cfg.get("transport_layer", {})
        entropy_threshold = float(tp_cfg.get("entropy_threshold", 1.0))
        max_retransmits = int(tp_cfg.get("max_retransmissions", 3))
        self.proto = IASTP(
            entropy_threshold=entropy_threshold,
            max_retransmits=max_retransmits,
        )

    def send_tokens(
        self,
        token_arrays: List[np.ndarray],
        entropies: List[float],
        loss_rate: float = 0.05,
    ) -> Tuple[List[TokenPacket], TransportStats]:
        """Transmit a series of tokens through IA-STP."""
        return self.proto.transmit_batch(token_arrays, entropies, loss_rate=loss_rate)

    def get_stats(self) -> TransportStats:
        return self.proto.get_stats()

