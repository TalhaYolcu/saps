"""
Publication & Presentation Plotting Module
===========================================

Generates figures and graphs for the 30-minute presentation and final report:
  1. Latency vs SNR (dB)
  2. Inference Accuracy / BLEU Score vs Packet Loss Rate
  3. Bandwidth Savings (%) by SNR
  4. Token Entropy Distribution & Selective ARQ Gating
  5. 4-Panel Executive Summary Dashboard for presentation slides
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np


class SAPSPlotter:
    """Generates comparative plots for SAPS vs Traditional Stack."""

    def __init__(self, output_dir: str = "results") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # Consistent styling
        self.saps_color = "#1E88E5"      # Sapphire Blue
        self.baseline_color = "#E53935"  # Crimson Red
        self.accent_color = "#43A047"    # Emerald Green

    def plot_latency_vs_snr(
        self,
        snr_db: List[float],
        saps_latency: List[float],
        baseline_latency: List[float],
        filename: str = "latency_vs_snr",
    ) -> Path:
        """Plot end-to-end latency comparison across SNR conditions."""
        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

        ax.plot(snr_db, baseline_latency, "o--", color=self.baseline_color, label="Traditional (HTTP/3 + QUIC)", linewidth=2.2, markersize=7)
        ax.plot(snr_db, saps_latency, "s-", color=self.saps_color, label="SAPS (Semantic Protocol Stack)", linewidth=2.5, markersize=7)

        ax.set_title("End-to-End Latency vs Mobile Channel SNR", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Signal-to-Noise Ratio (SNR in dB)", fontsize=12)
        ax.set_ylabel("Latency (ms)", fontsize=12)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(fontsize=11, loc="upper right")

        # Annotation of latency reduction
        if len(snr_db) > 2:
            mid_idx = len(snr_db) // 2
            diff_pct = (baseline_latency[mid_idx] - saps_latency[mid_idx]) / baseline_latency[mid_idx] * 100
            ax.annotate(
                f"-{diff_pct:.0f}% Latency",
                xy=(snr_db[mid_idx], saps_latency[mid_idx]),
                xytext=(snr_db[mid_idx] - 2, saps_latency[mid_idx] + (baseline_latency[mid_idx] - saps_latency[mid_idx]) * 0.4),
                arrowprops=dict(arrowstyle="->", color=self.accent_color, lw=1.5),
                fontsize=11,
                fontweight="bold",
                color=self.accent_color,
            )

        plt.tight_layout()
        out_png = self.output_dir / f"{filename}.png"
        out_pdf = self.output_dir / f"{filename}.pdf"
        fig.savefig(out_png)
        fig.savefig(out_pdf)
        plt.close(fig)
        return out_png

    def plot_bleu_vs_loss_rate(
        self,
        loss_rates: List[float],
        saps_bleu: List[float],
        baseline_bleu: List[float],
        filename: str = "bleu_vs_loss_rate",
    ) -> Path:
        """Plot semantic quality (BLEU score proxy) against fading packet loss rates."""
        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

        pct_loss = [x * 100 for x in loss_rates]
        ax.plot(pct_loss, baseline_bleu, "x--", color=self.baseline_color, label="Traditional Stack (Cliff Effect)", linewidth=2.2, markersize=7)
        ax.plot(pct_loss, saps_bleu, "o-", color=self.saps_color, label="SAPS (Deep-JSCC Graceful Degradation)", linewidth=2.5, markersize=7)

        ax.set_title("Semantic Quality (BLEU) vs Channel Loss Rate", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Packet Loss Rate (%)", fontsize=12)
        ax.set_ylabel("Semantic Fidelity / BLEU Score", fontsize=12)
        ax.set_ylim(0.0, 1.05)
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(fontsize=11, loc="lower left")

        plt.tight_layout()
        out_png = self.output_dir / f"{filename}.png"
        out_pdf = self.output_dir / f"{filename}.pdf"
        fig.savefig(out_png)
        fig.savefig(out_pdf)
        plt.close(fig)
        return out_png

    def plot_bandwidth_savings(
        self,
        snr_db: List[float],
        savings_pct: List[float],
        filename: str = "bandwidth_savings",
    ) -> Path:
        """Bar chart illustrating bandwidth savings percentage."""
        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

        bars = ax.bar([str(s) for s in snr_db], savings_pct, color=self.accent_color, alpha=0.85, width=0.55)

        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{height:.1f}%",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontweight="bold",
                fontsize=10,
            )

        ax.set_title("Total Bandwidth Savings of SAPS over HTTP/3 + QUIC", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("SNR (dB)", fontsize=12)
        ax.set_ylabel("Bandwidth Reduction (%)", fontsize=12)
        ax.set_ylim(0, 100)
        ax.grid(axis="y", linestyle=":", alpha=0.6)

        plt.tight_layout()
        out_png = self.output_dir / f"{filename}.png"
        out_pdf = self.output_dir / f"{filename}.pdf"
        fig.savefig(out_png)
        fig.savefig(out_pdf)
        plt.close(fig)
        return out_png

    def plot_entropy_distribution(
        self,
        entropies: List[float],
        threshold: float = 1.0,
        filename: str = "token_entropy_distribution",
    ) -> Path:
        """Histogram showing token entropy distribution with selective ARQ boundary."""
        fig, ax = plt.subplots(figsize=(8, 5), dpi=300)

        n, bins, patches = ax.hist(entropies, bins=30, color="#90CAF9", edgecolor="#1565C0", alpha=0.85)

        for patch, left_edge in zip(patches, bins[:-1]):
            if left_edge >= threshold:
                patch.set_facecolor("#EF5350")  # Critical tokens (retransmit)
            else:
                patch.set_facecolor("#66BB6A")  # Low-entropy tokens (skippable)

        ax.axvline(threshold, color="#B71C1C", linestyle="--", linewidth=2.5, label=f"Entropy Threshold ({threshold:.1f} nats)")

        ax.set_title("Token Entropy Distribution & IA-STP Selective ARQ", fontsize=14, fontweight="bold", pad=12)
        ax.set_xlabel("Token Shannon Entropy (nats)", fontsize=12)
        ax.set_ylabel("Token Frequency", fontsize=12)
        ax.legend(fontsize=11, loc="upper right")
        ax.grid(True, linestyle=":", alpha=0.6)

        plt.tight_layout()
        out_png = self.output_dir / f"{filename}.png"
        out_pdf = self.output_dir / f"{filename}.pdf"
        fig.savefig(out_png)
        fig.savefig(out_pdf)
        plt.close(fig)
        return out_png

    def plot_presentation_dashboard(
        self,
        data: Dict[str, Any],
        filename: str = "presentation_dashboard",
    ) -> Path:
        """4-Panel Executive Summary Dashboard designed for presentation slides."""
        fig, axs = plt.subplots(2, 2, figsize=(14, 10), dpi=300)

        snr = data["snr_range"]
        saps_lat = data["saps_latency"]
        base_lat = data["base_latency"]

        loss_rates = [l * 100 for l in data["loss_rates"]]
        saps_bleu = data["saps_bleu"]
        base_bleu = data["base_bleu"]

        savings = data["bandwidth_savings"]
        entropies = data["entropies"]
        thresh = data.get("entropy_threshold", 1.0)

        # 1. Latency
        axs[0, 0].plot(snr, base_lat, "o--", color=self.baseline_color, label="Traditional Stack", lw=2)
        axs[0, 0].plot(snr, saps_lat, "s-", color=self.saps_color, label="SAPS (Our Stack)", lw=2.5)
        axs[0, 0].set_title("(A) End-to-End Latency vs SNR", fontsize=12, fontweight="bold")
        axs[0, 0].set_xlabel("SNR (dB)")
        axs[0, 0].set_ylabel("Latency (ms)")
        axs[0, 0].grid(True, linestyle=":")
        axs[0, 0].legend()

        # 2. BLEU Quality
        axs[0, 1].plot(loss_rates, base_bleu, "x--", color=self.baseline_color, label="Traditional (Cliff Effect)", lw=2)
        axs[0, 1].plot(loss_rates, saps_bleu, "o-", color=self.saps_color, label="SAPS (Graceful Deep-JSCC)", lw=2.5)
        axs[0, 1].set_title("(B) Semantic Fidelity (BLEU) vs Packet Loss Rate", fontsize=12, fontweight="bold")
        axs[0, 1].set_xlabel("Packet Loss Rate (%)")
        axs[0, 1].set_ylabel("BLEU Score / Accuracy")
        axs[0, 1].grid(True, linestyle=":")
        axs[0, 1].legend()

        # 3. Bandwidth Savings
        bars = axs[1, 0].bar([str(s) for s in snr], savings, color=self.accent_color, alpha=0.85, width=0.5)
        axs[1, 0].set_title("(C) Bandwidth Reduction vs HTTP/3 (%)", fontsize=12, fontweight="bold")
        axs[1, 0].set_xlabel("SNR (dB)")
        axs[1, 0].set_ylabel("Savings (%)")
        axs[1, 0].set_ylim(0, 100)
        axs[1, 0].grid(axis="y", linestyle=":")

        # 4. Entropy
        axs[1, 1].hist(entropies, bins=25, color="#42A5F5", edgecolor="#1565C0", alpha=0.8)
        axs[1, 1].axvline(thresh, color="#D32F2F", linestyle="--", lw=2, label="ARQ Retransmit Threshold")
        axs[1, 1].set_title("(D) IA-STP Selective ARQ Token Filtering", fontsize=12, fontweight="bold")
        axs[1, 1].set_xlabel("Token Entropy (nats)")
        axs[1, 1].set_ylabel("Frequency")
        axs[1, 1].grid(True, linestyle=":")
        axs[1, 1].legend()

        fig.suptitle(
            "Semantic-Driven Agentic Protocol Stack (SAPS) vs Traditional HTTP/3 + QUIC Baseline\nCSE 476/575 Term Project",
            fontsize=15,
            fontweight="bold",
            y=0.98,
        )
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        out_png = self.output_dir / f"{filename}.png"
        out_pdf = self.output_dir / f"{filename}.pdf"
        fig.savefig(out_png)
        fig.savefig(out_pdf)
        plt.close(fig)
        return out_png
