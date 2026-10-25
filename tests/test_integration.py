"""Integration tests for the complete SAPS protocol stack simulation."""

import numpy as np
import pytest
from saps.simulator.engine import SAPSSimulator
from saps.baseline.traditional_stack import TraditionalStack
from saps.evaluation.metrics import MetricsCalculator


def test_full_saps_stack_traversal(sample_config, sample_latent_vector):
    sim = SAPSSimulator(sample_config)

    trace = sim.simulate_packet_transfer(
        latent_vector=sample_latent_vector,
        token_entropy=2.1,
        snr_db=15.0,
    )

    assert trace.delivered is True
    assert trace.total_latency_ms > 0
    assert trace.airl_time_ms > 0
    assert trace.app_time_ms > 0
    assert trace.transport_time_ms > 0
    assert trace.mac_time_ms > 0
    assert trace.phy_time_ms > 0


def test_saps_vs_baseline_latency_comparison(sample_config):
    sim = SAPSSimulator(sample_config)
    stack = TraditionalStack(sample_config)

    snr_points = [5.0, 15.0, 25.0]
    saps_res = sim.run_sweep(snr_values=snr_points, num_packets_per_snr=10, seed=42)

    rng = np.random.default_rng(seed=42)
    base_lats = []
    for snr in snr_points:
        for _ in range(10):
            res = stack.transmit({"tokens": [1.0] * 64}, snr_db=snr, packet_loss_rate=0.1, rng=rng)
            base_lats.append(res["total_latency_ms"])

    saps_lat = MetricsCalculator.compute_latency(saps_res["latencies_ms"])
    base_lat = MetricsCalculator.compute_latency(base_lats)

    # SAPS should have lower average latency due to selective skip and latent streaming
    assert saps_lat.mean_ms < base_lat.mean_ms
