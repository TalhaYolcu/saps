#!/usr/bin/env python
"""
run_saps.py — Main entry point for the SAPS protocol stack simulation.

Usage
-----
    python scripts/run_saps.py --config config/simulation_config.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict

# Ensure project root is on sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from saps.utils import load_config, set_seed, get_device, setup_logger, Timer
from saps.simulator.engine import SAPSSimulator
from saps.evaluation.metrics import MetricsCalculator


def run_simulation(config: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the full SAPS 6-layer simulation and return aggregated metrics."""
    logger = setup_logger("saps.simulation")
    device = get_device()
    logger.info("Simulation Device: %s", device)

    sim = SAPSSimulator(config)
    snr_range = config.get("channel", {}).get("snr_range_db", [0, 5, 10, 15, 20, 25, 30])
    num_packets = int(config.get("simulation", {}).get("num_agents", 5)) * 10
    latent_dim = int(config.get("physical_layer", {}).get("latent_dim", 256))

    logger.info("Running SAPS sweep across SNR: %s dB (%d packets per SNR point)...", snr_range, num_packets)
    results = sim.run_sweep(
        snr_values=snr_range,
        num_packets_per_snr=num_packets,
        latent_dim=latent_dim,
        seed=int(config.get("simulation", {}).get("seed", 42)),
    )

    lat_stats = MetricsCalculator.compute_latency(results["latencies_ms"])
    logger.info("Sweep complete! Mean Latency: %.2f ms | BLEU range: [%.2f, %.2f]",
                lat_stats.mean_ms, min(results["bleu_by_snr"]), max(results["bleu_by_snr"]))

    return {
        "sweep_results": results,
        "latency_stats": lat_stats,
        "airl_stats": sim.airl.stats,
        "transport_stats": sim.transport.get_stats(),
        "mac_stats": sim.datalink.get_queue_stats(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the SAPS protocol stack simulation.")
    parser.add_argument("--config", type=str, default="config/simulation_config.yaml", help="Path to config YAML")
    args = parser.parse_args()

    config = load_config(args.config)
    set_seed(config.get("simulation", {}).get("seed", 42))

    logger = setup_logger("saps.main")
    logger.info("=" * 65)
    logger.info("  SAPS (Semantic-Driven Agentic Protocol Stack) Simulation  ")
    logger.info("  CSE 476/575 Fall 2026 Term Project                       ")
    logger.info("=" * 65)

    with Timer("Full SAPS simulation execution", logger=logger):
        metrics = run_simulation(config)

    logger.info("-" * 65)
    logger.info("RESULTS SUMMARY ACROSS ALL 6 LAYERS:")
    logger.info("-" * 65)
    lat = metrics["latency_stats"]
    logger.info("  [Layer 1-4] Mean Latency:       %.2f ms (p95: %.2f ms, max: %.2f ms)", lat.mean_ms, lat.p95_ms, lat.max_ms)
    logger.info("  [Layer 6]   AIRL Offloads:      %d / %d accepted",
                metrics["airl_stats"]["negotiations_accepted"], metrics["airl_stats"]["negotiations_initiated"])
    logger.info("  [Layer 4]   IA-STP Packets:     %d total (%d retransmitted, %d skipped)",
                metrics["transport_stats"].total_packets,
                metrics["transport_stats"].packets_retransmitted,
                metrics["transport_stats"].packets_skipped)
    logger.info("  [Layer 2]   SP-MAC Frames:      %d enqueued, %d dequeued",
                metrics["mac_stats"].get("total_enqueued", 0),
                metrics["mac_stats"].get("total_dequeued", 0))
    logger.info("=" * 65)


if __name__ == "__main__":
    main()
