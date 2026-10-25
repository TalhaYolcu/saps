"""
Traditional Protocol Stack Baseline
====================================

Simulates the standard Internet protocol stack:
  - Application: JSON serialization over HTTP/3 REST / gRPC
  - Transport: QUIC / TCP full reliability (retransmits EVERY lost packet, blind to token entropy)
  - Network: Static IP-based routing (blind to compute/VRAM readiness and semantic intent)
  - Data Link: Standard FIFO / round-robin scheduling (no token criticality weighting)
  - Physical: Digital QAM modulation with threshold detection (cliff effect under deep fading)
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


@dataclass
class BaselinePacket:
    packet_id: int
    payload_bytes: bytes
    size_bytes: int
    destination_ip: str
    retransmissions: int = 0
    acknowledged: bool = False


@dataclass
class BaselineStats:
    total_packets_sent: int = 0
    packets_retransmitted: int = 0
    packets_lost: int = 0
    total_bytes_sent: int = 0
    total_latency_ms: float = 0.0
    cliff_effect_errors: int = 0


class TraditionalStack:
    """Conventional HTTP/3 + QUIC + IP stack baseline for comparison against SAPS.

    Parameters
    ----------
    config : dict, optional
        Simulation configuration.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        cfg = config or {}
        base_cfg = cfg.get("baseline", {})
        self.retransmit_all: bool = bool(base_cfg.get("retransmit_all", True))
        self.mtu_bytes: int = int(base_cfg.get("mtu_bytes", 1400))
        self.rtt_base_ms: float = float(base_cfg.get("rtt_base_ms", 15.0))
        self.stats = BaselineStats()
        self._next_id = 0

    def serialize_json(self, data: Dict[str, Any]) -> bytes:
        """Convert data (e.g. KV cache or token vectors) to JSON bytes."""
        # Convert numpy arrays to lists for JSON serialization
        def _convert(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, (np.floating, np.float32, np.float64)):
                return float(obj)
            if isinstance(obj, (np.integer, np.int32, np.int64)):
                return int(obj)
            return str(obj)

        json_str = json.dumps(data, default=_convert)
        payload = json_str.encode("utf-8")
        return payload

    def chunk_payload(self, payload: bytes, dest_ip: str = "192.168.1.100") -> List[BaselinePacket]:
        """Fragment serialized payload into MTU-sized packets."""
        packets: List[BaselinePacket] = []
        for i in range(0, len(payload), self.mtu_bytes):
            chunk = payload[i : i + self.mtu_bytes]
            pkt = BaselinePacket(
                packet_id=self._next_id,
                payload_bytes=chunk,
                size_bytes=len(chunk),
                destination_ip=dest_ip,
            )
            self._next_id += 1
            packets.append(pkt)
        return packets

    def transmit_packets(
        self,
        packets: List[BaselinePacket],
        snr_db: float,
        packet_loss_rate: float,
        rng: Optional[np.random.Generator] = None,
    ) -> Tuple[List[BaselinePacket], float]:
        """Simulate QUIC reliable transmission over wireless channel.

        Retransmits ALL lost packets indiscriminately until delivery or max attempts.
        Calculates cumulative latency including retransmission delays.
        """
        if rng is None:
            rng = np.random.default_rng(seed=42)

        total_latency = 0.0
        delivered: List[BaselinePacket] = []

        # Traditional QAM cliff effect: if SNR falls below threshold, error rate spikes
        snr_threshold = 7.0  # dB for QPSK/16-QAM minimum decoding
        effective_loss = packet_loss_rate
        if snr_db < snr_threshold:
            cliff_penalty = float(np.clip((snr_threshold - snr_db) * 0.1, 0.0, 0.6))
            effective_loss = min(1.0, packet_loss_rate + cliff_penalty)
            self.stats.cliff_effect_errors += 1

        for pkt in packets:
            self.stats.total_packets_sent += 1
            self.stats.total_bytes_sent += pkt.size_bytes
            pkt_latency = self.rtt_base_ms / 2.0  # One-way

            lost = rng.random() < effective_loss
            attempts = 0
            max_retries = 5

            while lost and attempts < max_retries:
                attempts += 1
                pkt.retransmissions += 1
                self.stats.packets_retransmitted += 1
                self.stats.total_bytes_sent += pkt.size_bytes
                # Retransmission RTO (exponential backoff)
                rto = self.rtt_base_ms * (1.5 ** attempts)
                pkt_latency += rto
                lost = rng.random() < effective_loss

            if not lost:
                pkt.acknowledged = True
                delivered.append(pkt)
            else:
                self.stats.packets_lost += 1

            total_latency = max(total_latency, pkt_latency)

        self.stats.total_latency_ms += total_latency
        return delivered, total_latency

    def transmit(
        self,
        data: Dict[str, Any],
        snr_db: float,
        packet_loss_rate: float,
        dest_ip: str = "192.168.1.100",
        rng: Optional[np.random.Generator] = None,
    ) -> Dict[str, Any]:
        """Full end-to-end baseline pipeline: serialize -> packetize -> transmit."""
        t0 = time.perf_counter()
        raw_bytes = self.serialize_json(data)
        ser_time_ms = (time.perf_counter() - t0) * 1000.0

        packets = self.chunk_payload(raw_bytes, dest_ip=dest_ip)
        delivered, link_latency_ms = self.transmit_packets(
            packets=packets,
            snr_db=snr_db,
            packet_loss_rate=packet_loss_rate,
            rng=rng,
        )

        total_latency_ms = ser_time_ms + link_latency_ms
        delivery_ratio = len(delivered) / max(len(packets), 1)

        return {
            "total_latency_ms": total_latency_ms,
            "serialization_time_ms": ser_time_ms,
            "link_latency_ms": link_latency_ms,
            "payload_bytes": len(raw_bytes),
            "packets_sent": len(packets),
            "packets_delivered": len(delivered),
            "delivery_ratio": delivery_ratio,
            "retransmissions": sum(p.retransmissions for p in packets),
        }

    def reset_stats(self) -> None:
        self.stats = BaselineStats()
        self._next_id = 0
