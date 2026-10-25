# SAPS — Semantic-Driven Agentic Protocol Stack for Mobile AI Agents

> Redesigning the internet protocol stack from the ground up for AI-native communication over mobile wireless channels.

## Overview

SAPS is a 6-layer network protocol stack simulation that replaces traditional byte-oriented protocols with **semantic-aware** layers. Instead of treating data as opaque bit-streams, each layer understands token entropy, intent vectors, and latent representations to route, transport, and encode data for AI agents over mobile wireless channels.

The stack is evaluated against a conventional **HTTP/3 + QUIC** baseline under identical Rayleigh/Rician fading channel conditions, comparing latency, semantic fidelity (BLEU), bandwidth efficiency, and energy consumption.

## System Architecture

```
┌─────────────────────────────────────────────────┐
│  Layer 6 — AIRL  (AI-to-AI Resource & Liaison)  │  Inter-agent negotiation, context sync, offloading
├─────────────────────────────────────────────────┤
│  Layer 5 — Application Layer                    │  KV-cache management, latent vector compression
├─────────────────────────────────────────────────┤
│  Layer 4 — IA-STP  (Intent-Aware Semantic TP)   │  Entropy-gated selective ARQ, semantic transport
├─────────────────────────────────────────────────┤
│  Layer 3 — V-CCR  (Vector-space Context Routing)│  FAISS-based intent-vector routing
├─────────────────────────────────────────────────┤
│  Layer 2 — SP-MAC (Semantic-Priority MAC)       │  Criticality-aware priority queuing
├─────────────────────────────────────────────────┤
│  Layer 1 — Deep-JSCC  (Physical Layer)          │  Joint source-channel coding via neural encoder/decoder
└─────────────────────────────────────────────────┘
```

| Layer | Name | Traditional Equivalent | Key Innovation |
|-------|------|----------------------|----------------|
| 6 | AIRL | — | AI-native resource negotiation & context sync |
| 5 | Application | HTTP/3 | KV-cache windowing & latent compression |
| 4 | IA-STP | QUIC / TCP | Entropy-gated selective ARQ |
| 3 | V-CCR | IP | FAISS intent-vector routing |
| 2 | SP-MAC | MAC / LLC | Semantic-priority queuing |
| 1 | Deep-JSCC | PHY (OFDM, etc.) | Neural joint source-channel coding |

## Installation

```bash
# Clone the repository
cd saps/

# Create a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Run the SAPS simulation

```bash
python scripts/run_saps.py --config config/simulation_config.yaml
```

### Run the traditional baseline (HTTP/3 + QUIC)

```bash
python scripts/run_baseline.py --config config/simulation_config.yaml
```

### Run the full comparison and generate plots

```bash
python scripts/run_comparison.py --config config/simulation_config.yaml
```

Results (plots and CSVs) are saved to the `results/` directory.

## Project Structure

```
saps/
├── config/
│   ├── __init__.py
│   └── simulation_config.yaml      # All simulation parameters
├── saps/
│   ├── __init__.py                  # Package init (__version__)
│   ├── utils.py                     # Config loading, seeding, timing
│   ├── physical/                    # Layer 1 — Deep-JSCC
│   ├── datalink/                    # Layer 2 — SP-MAC
│   ├── network/                     # Layer 3 — V-CCR
│   ├── transport/                   # Layer 4 — IA-STP
│   ├── application/                 # Layer 5 — Application
│   └── airl/                        # Layer 6 — AIRL
├── evaluation/
│   └── __init__.py                  # Metric computation & plotting
├── scripts/
│   ├── __init__.py
│   ├── run_saps.py                  # Main SAPS simulation entry point
│   ├── run_baseline.py              # Traditional stack baseline
│   └── run_comparison.py            # Side-by-side comparison + plots
├── tests/
│   └── __init__.py
├── results/                         # Auto-generated output directory
│   └── .gitkeep
├── README.md
└── requirements.txt
```

## Course Attribution

> **CSE 476/575 — Wireless & Mobile Networks, Fall 2026**
>
> This project was developed as part of the graduate course on Wireless and Mobile Networks. It explores the intersection of deep learning, semantic communication, and next-generation protocol design for AI-agent ecosystems.
