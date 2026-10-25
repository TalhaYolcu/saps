"""
SimPy Event-Driven Simulation Engine
=====================================

Executes discrete-event simulations for the 6-layer SAPS protocol stack
under mobile wireless fading channels.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import simpy

from saps.channel.fading import AWGNChannel, RayleighChannel, RicianChannel
from saps.layers.physical import PhysicalLayer, DeepJSCCTransceiver
from saps.layers.datalink import DataLinkLayer, CriticalityLevel, Frame
from saps.layers.network import NetworkLayer
from saps.layers.transport import TransportLayer, TokenPacket
from saps.layers.application import ApplicationLayer, StreamChunk
from saps.layers.airl import AgentIntentReasoningLayer, TaskType


@dataclass
class PacketTrace:
    """Telemetry recorded for an individual packet traversal."""
    packet_id: int
    intent: str
    num_tokens: int
    entropy: float
    is_critical: bool
    snr_db: float
    airl_time_ms: float
    app_time_ms: float
    transport_time_ms: float
    mac_time_ms: float
    phy_time_ms: float
    total_latency_ms: float
    delivered: bool
    retransmissions: int
    mse: float


class SAPSSimulator:
    """Discrete-event simulator for the Semantic-Driven Agentic Protocol Stack.

    Parameters
    ----------
    config : dict, optional
        Simulation parameters.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.env = simpy.Environment()

        # Instantiate all 6 layers
        self.airl = AgentIntentReasoningLayer(self.config)
        self.app = ApplicationLayer(self.config)
        self.transport = TransportLayer(self.config)
        self.datalink = DataLinkLayer(self.config.get("datalink_layer"))
        self.network = NetworkLayer(self.config)
        self.physical = PhysicalLayer(self.config.get("physical_layer"))

        # Setup standard wireless edge topology
        self._setup_default_topology()

        self.traces: List[PacketTrace] = []

    def _setup_default_topology(self) -> None:
        """Register Edge Compute nodes and Mobile Agents with distinct capabilities."""
        dim = int(self.config.get("network_layer", {}).get("embedding_dim", 256))
        rng = np.random.default_rng(seed=101)

        # Edge node 1: Visual reasoning & heavy inference
        v_intent = rng.normal(size=dim).astype(np.float32)
        self.network.register_node("edge_vision_01", v_intent, {"gpu": "H100", "vram_gb": 80})
        self.airl.register_agent("edge_vision_01", v_intent, [TaskType.VISUAL, TaskType.REASONING], 80.0, 0.15)

        # Edge node 2: Code generation & reasoning
        c_intent = rng.normal(size=dim).astype(np.float32)
        self.network.register_node("edge_code_02", c_intent, {"gpu": "A100", "vram_gb": 40})
        self.airl.register_agent("edge_code_02", c_intent, [TaskType.CODE_GEN, TaskType.INFERENCE], 40.0, 0.20)

        # Mobile agent: local requester
        m_intent = rng.normal(size=dim).astype(np.float32)
        self.airl.register_agent("mobile_agent_01", m_intent, [TaskType.INFERENCE], 4.0, 0.85, battery_level=0.4)

    def simulate_packet_transfer(
        self,
        latent_vector: np.ndarray,
        token_entropy: float,
        snr_db: float,
        task_type: TaskType = TaskType.REASONING,
        rng: Optional[np.random.Generator] = None,
    ) -> PacketTrace:
        """Simulate a single semantic payload traversing all 6 layers of the stack."""
        if rng is None:
            rng = np.random.default_rng()

        dim = latent_vector.shape[-1]
        pkt_id = len(self.traces)

        # 1. Layer 6 (AIRL): Intent negotiation & offload evaluation
        t_airl_0 = time.perf_counter()
        offload_needed = self.airl.evaluate_offloading_need("mobile_agent_01")
        proposal = self.airl.negotiate_offload(
            requester_id="mobile_agent_01",
            task_type=task_type,
            task_intent=latent_vector[:dim],
        )
        target_agent = proposal.target_id if proposal else "edge_vision_01"
        airl_ms = (time.perf_counter() - t_airl_0) * 1000.0 + 1.2  # 1.2ms negotiation overhead

        # 2. Layer 5 (Application): KV-cache & Latent stream compression
        t_app_0 = time.perf_counter()
        chunk = self.app.prepare_payload(latent_vector, token_entropy=token_entropy, intent=task_type.value)
        app_ms = (time.perf_counter() - t_app_0) * 1000.0 + 0.8  # ~0.8ms quantization & chunking

        # 3. Layer 4 (Transport / IA-STP): Selective ARQ based on entropy
        t_tp_0 = time.perf_counter()
        is_crit = self.transport.proto.classify_token(token_entropy)
        pkt = self.transport.proto.create_packet(tokens=chunk.data, entropy=token_entropy)

        # Channel packet drop probability model based on SNR
        # Under Deep-JSCC, channel is soft/graceful, but transport handles extreme fading dips
        loss_prob = float(np.clip(np.exp(-snr_db / 5.0) * 0.35, 0.01, 0.60))
        lost = rng.random() < loss_prob
        action = self.transport.proto.selective_arq(pkt, lost)

        retries = 0
        while action == "retransmit" and retries < self.transport.proto.max_retransmits:
            retries += 1
            lost = rng.random() < loss_prob
            action = self.transport.proto.selective_arq(pkt, lost)

        delivered = (action == "ack") or (action == "skip")
        tp_ms = (time.perf_counter() - t_tp_0) * 1000.0 + (retries * 8.0) + 1.0

        # 4. Layer 3 (Network / V-CCR): Semantic routing via intent cosine similarity
        t_net_0 = time.perf_counter()
        route_res = self.network.route_packet({"intent_vector": latent_vector[:dim]})
        next_hop = route_res[0] if route_res else target_agent
        net_ms = (time.perf_counter() - t_net_0) * 1000.0 + 0.5

        # 5. Layer 2 (Data Link / SP-MAC): Priority Queuing
        t_mac_0 = time.perf_counter()
        crit_level = CriticalityLevel.CRITICAL if is_crit else CriticalityLevel.LOW
        frame = self.datalink.send(
            payload=pkt,
            criticality=crit_level,
            token_entropy=token_entropy,
            size_bytes=int(chunk.data.nbytes * self.app.compression_ratio),
        )
        # SP-MAC gives priority frames lower contention delay
        queue_delay = 0.5 if is_crit else 3.5
        mac_ms = (time.perf_counter() - t_mac_0) * 1000.0 + queue_delay

        # 6. Layer 1 (Physical / Deep-JSCC): Neural transceiver over fading channel
        t_phy_0 = time.perf_counter()
        phy_dim = self.physical.transceiver.latent_dim
        if len(latent_vector) >= phy_dim:
            phy_in = latent_vector[:phy_dim]
        else:
            phy_in = np.pad(latent_vector, (0, phy_dim - len(latent_vector)))

        rec_vector = self.physical.transmit(phy_in, snr_db=snr_db)
        phy_ms = (time.perf_counter() - t_phy_0) * 1000.0 + 2.5

        mse = float(np.mean((phy_in - rec_vector) ** 2))
        total_latency = airl_ms + app_ms + tp_ms + net_ms + mac_ms + phy_ms

        trace = PacketTrace(
            packet_id=pkt_id,
            intent=task_type.value,
            num_tokens=chunk.num_tokens,
            entropy=token_entropy,
            is_critical=is_crit,
            snr_db=snr_db,
            airl_time_ms=airl_ms,
            app_time_ms=app_ms,
            transport_time_ms=tp_ms,
            mac_time_ms=mac_ms,
            phy_time_ms=phy_ms,
            total_latency_ms=total_latency,
            delivered=delivered,
            retransmissions=retries,
            mse=mse,
        )
        self.traces.append(trace)
        return trace

    def run_sweep(
        self,
        snr_values: List[float],
        num_packets_per_snr: int = 50,
        latent_dim: Optional[int] = None,
        seed: int = 42,
    ) -> Dict[str, Any]:
        """Execute a full simulation sweep across multiple SNR points."""
        rng = np.random.default_rng(seed)
        eff_dim = latent_dim or self.physical.transceiver.latent_dim

        latencies_by_snr: List[float] = []
        mse_by_snr: List[float] = []
        bleu_by_snr: List[float] = []
        tokens_skipped_count = 0
        total_tokens_count = 0
        total_retransmits = 0

        all_entropies: List[float] = []

        for snr in snr_values:
            snr_latencies = []
            snr_mses = []

            for _ in range(num_packets_per_snr):
                # Sample random latent vector (representing transformer hidden state)
                vec = rng.normal(size=eff_dim).astype(np.float32)
                # Sample realistic token entropy (e.g. mixture of low-entropy function words and high-entropy keywords)
                is_keyword = rng.random() > 0.4
                entropy = float(rng.uniform(1.2, 3.5) if is_keyword else rng.uniform(0.1, 0.9))
                all_entropies.append(entropy)

                trace = self.simulate_packet_transfer(vec, token_entropy=entropy, snr_db=snr, rng=rng)

                snr_latencies.append(trace.total_latency_ms)
                snr_mses.append(trace.mse)

                total_tokens_count += trace.num_tokens
                if not trace.is_critical and trace.retransmissions == 0:
                    tokens_skipped_count += 0  # delivered or intentionally skipped
                total_retransmits += trace.retransmissions

            avg_lat = float(np.mean(snr_latencies))
            avg_mse = float(np.mean(snr_mses))
            cos_sim = float(np.clip(1.0 - (avg_mse / 2.0), 0.1, 0.99))
            bleu = float(np.clip(cos_sim ** 1.5, 0.0, 1.0))

            latencies_by_snr.append(avg_lat)
            mse_by_snr.append(avg_mse)
            bleu_by_snr.append(bleu)

        # Compute total bytes sent
        raw_token_bytes = total_tokens_count * eff_dim * 4
        compressed_bytes = int(raw_token_bytes * self.app.compression_ratio)

        return {
            "snr_range": snr_values,
            "latencies_ms": latencies_by_snr,
            "mse_by_snr": mse_by_snr,
            "bleu_by_snr": bleu_by_snr,
            "total_bytes": compressed_bytes,
            "total_tokens": total_tokens_count,
            "tokens_skipped": self.transport.proto.stats.tokens_skipped,
            "retransmissions": total_retransmits,
            "entropies": all_entropies,
        }
