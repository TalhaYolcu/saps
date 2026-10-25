"""SAPS protocol stack layers.

Layer 1 (Physical):    Deep Joint Source-Channel Coding (Deep-JSCC)
Layer 2 (Data Link):   Semantic-Priority MAC (SP-MAC)
Layer 3 (Network):     Vector-space Content-Centric Routing (V-CCR)
Layer 4 (Transport):   Intent-Aware Selective Transport Protocol (IA-STP)
Layer 5 (Application): Direct KV-Cache & Latent Vector Streaming
Layer 6 (NEW):         Agent Intent & Reasoning Layer (AIRL)
"""

from saps.layers.physical import DeepJSCCEncoder, DeepJSCCDecoder, DeepJSCCTransceiver, PhysicalLayer
from saps.layers.datalink import CriticalityLevel, Frame, SPMACScheduler, DataLinkLayer
from saps.layers.network import RouterNode, VCCRRouter, NetworkLayer
from saps.layers.transport import TokenPacket, TransportStats, IASTP, TransportLayer
from saps.layers.application import StreamChunk, KVCacheSerializer, LatentVectorStream, ApplicationLayer
from saps.layers.airl import TaskType, AgentProfile, NegotiationProposal, AgentIntentReasoningLayer

__all__ = [
    # Layer 1
    "DeepJSCCEncoder",
    "DeepJSCCDecoder",
    "DeepJSCCTransceiver",
    "PhysicalLayer",
    # Layer 2
    "CriticalityLevel",
    "Frame",
    "SPMACScheduler",
    "DataLinkLayer",
    # Layer 3
    "RouterNode",
    "VCCRRouter",
    "NetworkLayer",
    # Layer 4
    "TokenPacket",
    "TransportStats",
    "IASTP",
    "TransportLayer",
    # Layer 5
    "StreamChunk",
    "KVCacheSerializer",
    "LatentVectorStream",
    "ApplicationLayer",
    # Layer 6
    "TaskType",
    "AgentProfile",
    "NegotiationProposal",
    "AgentIntentReasoningLayer",
]
