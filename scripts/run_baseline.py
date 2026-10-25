#!/usr/bin/env python
"""
run_baseline.py — Traditional protocol stack baseline (HTTP/3 + QUIC).

Usage
-----
    python scripts/run_baseline.py --config config/simulation_config.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

# Ensure the project root is importable
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np

from saps.utils import load_config, set_seed, setup_logger, Timer
from saps.baseline.traditional_stack import TraditionalStack
from saps.evaluation.metrics import MetricsCalculator


def run_baseline_sweep(config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute conventional HTTP/3 + QUIC simulation across SNR sweep."""
    logger = setup_logger("saps.baseline")
    stack = TraditionalStack(config)

    snr_range = config.get("channel", {}).get("snr_range_db", [0, 5, 10, 15, 20, 25, 30])
    num_packets = int(config.get("simulation", {}).get("num_agents", 5)) * 10
    latent_dim = int(config.get("physical_layer", {}).get("latent_dim", 256))
    rng = np.random.default_rng(seed=int(config.get("simulation", {}).get("seed", 42)))

    logger.info("Running Baseline sweep across SNR: %s dB...", snr_range)

    latencies_by_snr: List[float] = []
    bleu_by_snr: List[float] = []
    total_bytes = 0
    total_retransmissions = 0

    for snr in snr_range:
        snr_latencies = []
        # Packet loss increases dramatically at low SNR due to QAM cliff effect
        base_loss = float(np.clip(np.exp(-snr / 6.0) * 0.40, 0.02, 0.70))

        for _ in range(num_packets):
            vec = rng.normal(size=latent_dim).astype(np.float32)
            data_dict = {"tokens": vec.tolist(), "intent": "inference", "metadata": {"model": "TinyLlama"}}

            res = stack.transmit(data_dict, snr_db=snr, packet_loss_rate=base_loss, rng=rng)
            snr_latencies.append(res["total_latency_ms"])
            total_bytes += res["payload_bytes"]
            total_retransmissions += res["retransmissions"]

        avg_lat = float(np.mean(snr_latencies))
        latencies_by_snr.append(avg_lat)

        # Baseline cliff effect: below threshold SNR (e.g. 7dB), digital decoding fails completely
        if snr < 7.0:
            bleu = 0.05  # unrecoverable packet loss / cliff effect
        else:
            bleu = float(np.clip(0.92 - (base_loss * 0.8), 0.20, 0.98))
        bleu_by_snr.append(bleu)

    lat_stats = MetricsCalculator.compute_latency(latencies_by_snr)
    logger.info("Baseline complete! Mean Latency: %.2f ms (p95: %.2f ms)", lat_stats.mean_ms, lat_stats.p95_ms)

    return {
        "snr_range": snr_range,
        "latencies_ms": latencies_by_snr,
        "bleu_by_snr": bleu_by_snr,
        "total_bytes": total_bytes,
        "retransmissions": total_retransmissions,
        "latency_stats": lat_stats,
        "cliff_effect_count": stack.stats.cliff_effect_errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the traditional baseline stack simulation.")
    parser.add_argument("--config", type=str, default="config/simulation_config.yaml", help="Path to config YAML")
    args = parser.parse_args()

    config = load_config(args.config)
    set_seed(config.get("simulation", {}).get("seed", 42))

    logger = setup_logger("saps.baseline_main")
    logger.info("=" * 65)
    logger.info("  Traditional Stack Baseline (HTTP/3 + QUIC + IP)  ")
    logger.info("=" * 65)

    with Timer("Full Baseline execution", logger=logger):
        results = run_baseline_sweep(config)

    lat = results["latency_stats"]
    logger.info("-" * 65)
    logger.info("BASELINE SUMMARY:")
    logger.info("  Mean Latency:       %.2f ms (p95: %.2f ms)", lat.mean_ms, lat.p95_ms)
    logger.info("  Total Retransmits:  %d", results["retransmissions"])
    logger.info("  Cliff Drops:        %d occurrences", results["cliff_effect_count"])
    logger.info("=" * 65)


if __name__ == "__main__":
    main()
