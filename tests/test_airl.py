"""Unit tests for Layer 6 (NEW) — Agent Intent & Reasoning Layer (AIRL)."""

import numpy as np
import pytest
from saps.layers.airl import AgentIntentReasoningLayer, TaskType, ContextStateSync


def test_airl_agent_registration():
    airl = AgentIntentReasoningLayer()
    intent = np.array([1.0, 0.0, 0.0])
    profile = airl.register_agent("edge_01", intent, [TaskType.REASONING], vram_available_gb=40.0)
    assert profile.agent_id == "edge_01"
    assert "edge_01" in airl.agents


def test_airl_offload_trigger_on_high_load():
    airl = AgentIntentReasoningLayer({"airl": {"offloading_threshold": 0.8}})
    intent = np.array([0.5, 0.5, 0.0])
    airl.register_agent("mobile_agent", intent, [TaskType.INFERENCE], compute_load=0.85)

    assert airl.evaluate_offloading_need("mobile_agent") is True


def test_airl_negotiation_partner_matching():
    airl = AgentIntentReasoningLayer()
    dim = 4
    vec_vis = np.array([1.0, 0.0, 0.0, 0.0])
    vec_code = np.array([0.0, 1.0, 0.0, 0.0])

    airl.register_agent("edge_vision", vec_vis, [TaskType.VISUAL], vram_available_gb=80.0, compute_load=0.1)
    airl.register_agent("edge_code", vec_code, [TaskType.CODE_GEN], vram_available_gb=40.0, compute_load=0.1)

    proposal = airl.negotiate_offload(
        requester_id="mobile_agent",
        task_type=TaskType.VISUAL,
        task_intent=vec_vis,
        required_vram_gb=16.0,
    )

    assert proposal is not None
    assert proposal.target_id == "edge_vision"
    assert proposal.status == "ACCEPTED"


def test_context_state_sync_alignment():
    c1 = np.array([1.0, 0.0, 0.0])
    c2 = np.array([0.8, 0.6, 0.0])

    divergence = ContextStateSync.compute_context_divergence(c1, c2)
    assert 0.0 < divergence < 1.0

    merged = ContextStateSync.align_contexts(c1, c2, alpha=0.5)
    assert np.isclose(np.linalg.norm(merged), 1.0)
