"""Unit tests for Layer 3 — Vector-space Content-Centric Routing (V-CCR)."""

import numpy as np
import pytest
from saps.layers.network import VCCRRouter, NetworkLayer


def test_vccr_router_similarity_matching():
    router = VCCRRouter(similarity_threshold=0.5, top_k=2)

    vec_a = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    vec_b = np.array([0.0, 1.0, 0.0], dtype=np.float32)

    router.add_node("node_a", vec_a)
    router.add_node("node_b", vec_b)

    # Query close to node_a
    query = np.array([0.9, 0.1, 0.0], dtype=np.float32)
    routes = router.route(query)

    assert len(routes) > 0
    best_node, score = routes[0]
    assert best_node == "node_a"
    assert score > 0.8


def test_network_layer_wrapper():
    net = NetworkLayer({"network_layer": {"similarity_threshold": 0.4}})
    vec = np.array([0.5, 0.5, 0.0], dtype=np.float32)
    net.register_node("edge_01", vec)

    res = net.route_packet({"intent_vector": vec})
    assert res is not None
    node_id, score = res
    assert node_id == "edge_01"
    assert np.isclose(score, 1.0)
