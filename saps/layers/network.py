"""Layer 3 — Network Layer: Vector-space Content-Centric Routing (V-CCR).

Routes data based on semantic intent vectors (cosine similarity)
instead of traditional IP addresses.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class RouterNode:
    """A node in the semantic routing network."""
    node_id: str
    intent_vector: np.ndarray           # semantic embedding of the node's capability
    metadata: Dict = field(default_factory=dict)


class VCCRRouter:
    """Vector-space Content-Centric Router.

    Maintains a registry of nodes, each described by a semantic intent
    vector.  Incoming requests carry an intent vector and are routed to
    the node(s) whose intent is most similar (cosine similarity).
    """

    def __init__(self, similarity_threshold: float = 0.5, top_k: int = 3) -> None:
        self.similarity_threshold = similarity_threshold
        self.top_k = top_k
        self.nodes: Dict[str, RouterNode] = {}

    # ------------------------------------------------------------------ #
    #  Node Management
    # ------------------------------------------------------------------ #

    def add_node(self, node_id: str, intent_vector: np.ndarray,
                 metadata: Optional[Dict] = None) -> None:
        """Register a node with its intent vector.

        Parameters
        ----------
        node_id : str
            Unique identifier for the node.
        intent_vector : np.ndarray
            Semantic embedding describing the node's capability.
        metadata : dict, optional
            Extra attributes (e.g. capacity, location).
        """
        vec = np.asarray(intent_vector, dtype=np.float64)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm  # store unit vector
        self.nodes[node_id] = RouterNode(
            node_id=node_id,
            intent_vector=vec,
            metadata=metadata or {},
        )

    def remove_node(self, node_id: str) -> bool:
        """Remove a node from the routing table."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            return True
        return False

    # ------------------------------------------------------------------ #
    #  Similarity & Routing
    # ------------------------------------------------------------------ #

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        min_d = min(len(a), len(b))
        a_sub = a[:min_d]
        b_sub = b[:min_d]
        norm_a = np.linalg.norm(a_sub)
        norm_b = np.linalg.norm(b_sub)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a_sub, b_sub) / (norm_a * norm_b))

    def route(
        self,
        intent_vector: np.ndarray,
        top_k: Optional[int] = None,
    ) -> List[Tuple[str, float]]:
        """Route a request to the best-matching node(s).

        Parameters
        ----------
        intent_vector : np.ndarray
            Semantic intent of the request.
        top_k : int, optional
            Override the default ``top_k``.

        Returns
        -------
        list of (node_id, similarity)
            Nodes whose similarity exceeds the threshold, sorted descending,
            limited to *top_k* entries.
        """
        k = top_k if top_k is not None else self.top_k
        query = np.asarray(intent_vector, dtype=np.float64)
        norm = np.linalg.norm(query)
        if norm > 0:
            query = query / norm

        scores: List[Tuple[str, float]] = []
        for node in self.nodes.values():
            sim = self.cosine_similarity(query, node.intent_vector)
            if sim >= self.similarity_threshold:
                scores.append((node.node_id, sim))

        scores.sort(key=lambda t: t[1], reverse=True)
        return scores[:k]

    def best_route(self, intent_vector: np.ndarray) -> Optional[Tuple[str, float]]:
        """Return the single best matching node, or ``None``."""
        results = self.route(intent_vector, top_k=1)
        return results[0] if results else None


class NetworkLayer:
    """Network Layer wrapper for the SAPS protocol stack.

    Provides high-level routing and topology configuration.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        cfg = config or {}
        net_cfg = cfg.get("network_layer", {})
        similarity_threshold = float(net_cfg.get("similarity_threshold", 0.5))
        self.router = VCCRRouter(similarity_threshold=similarity_threshold)

    def register_node(
        self,
        node_id: str,
        intent_vector: np.ndarray,
        metadata: Optional[Dict] = None,
    ) -> None:
        """Register an edge node or agent with its capability vector."""
        self.router.add_node(node_id, intent_vector, metadata)

    def route_packet(self, packet: Dict[str, Any]) -> Optional[Tuple[str, float]]:
        """Route packet to the best node matching the packet's intent embedding."""
        intent = packet.get("intent_vector")
        if intent is None:
            return None
        return self.router.best_route(intent)

