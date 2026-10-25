"""Unit tests for Layer 4 — Intent-Aware Selective Transport Protocol (IA-STP)."""

import numpy as np
import pytest
from saps.layers.transport import IASTP, TransportLayer


def test_shannon_entropy_calculation():
    # Uniform distribution: highest entropy
    p_uniform = np.array([0.25, 0.25, 0.25, 0.25])
    h_uniform = IASTP.compute_entropy(p_uniform)

    # Deterministic distribution: 0 entropy
    p_det = np.array([1.0, 0.0, 0.0, 0.0])
    h_det = IASTP.compute_entropy(p_det)

    assert h_det == 0.0
    assert h_uniform > 1.3


def test_selective_arq_retransmit_critical():
    proto = IASTP(entropy_threshold=1.0, max_retransmits=2)
    tokens = np.array([1, 2, 3])

    # High-entropy packet (critical)
    pkt_crit = proto.create_packet(tokens, entropy=2.5)
    assert pkt_crit.is_critical is True

    action1 = proto.selective_arq(pkt_crit, lost=True)
    assert action1 == "retransmit"
    assert pkt_crit.retransmit_count == 1


def test_selective_arq_skip_non_critical():
    proto = IASTP(entropy_threshold=1.0)
    tokens = np.array([10, 20])

    # Low-entropy packet (e.g. stop word)
    pkt_low = proto.create_packet(tokens, entropy=0.3)
    assert pkt_low.is_critical is False

    # When lost, IA-STP should skip it to save latency!
    action = proto.selective_arq(pkt_low, lost=True)
    assert action == "skip"
    assert proto.stats.packets_skipped == 1
