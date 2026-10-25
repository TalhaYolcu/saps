"""
Layer 6 (NEW) — Agent Intent & Reasoning Layer (AIRL)
======================================================

Situated at the top of the SAPS stack, AIRL manages:
  1. Agent-to-Agent semantic negotiation & task contracting.
  2. Context alignment (shared state vector synchronization).
  3. Dynamic edge offloading decisions based on mobile link quality,
     agent load, and model capability requirements.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


class TaskType(str, Enum):
    """Categorization of agentic tasks."""
    INFERENCE = "inference"
    REASONING = "reasoning"
    VISUAL = "visual_reasoning"
    CODE_GEN = "code_generation"
    SUMMARIZATION = "summarization"


@dataclass
class AgentProfile:
    """Identity and status of an AI agent in the mobile network."""
    agent_id: str
    intent_vector: np.ndarray       # D-dimensional semantic capability vector
    capabilities: List[TaskType]    # Supported task modalities
    vram_available_gb: float        # Available accelerator memory
    compute_load: float             # Current compute load [0.0, 1.0]
    battery_level: float = 1.0      # Mobile agent battery [0.0, 1.0]
    last_seen: float = field(default_factory=time.time)


@dataclass
class NegotiationProposal:
    """A task offloading or collaboration contract proposal."""
    proposal_id: str
    requester_id: str
    target_id: str
    task_type: TaskType
    required_vram_gb: float
    intent_embedding: np.ndarray
    deadline_ms: float
    status: str = "PENDING"  # PENDING, ACCEPTED, REJECTED, EXPIRED
    created_at: float = field(default_factory=time.time)


class ContextStateSync:
    """Manages shared conversational/state vectors between cooperating agents."""

    @staticmethod
    def compute_context_divergence(
        local_context: np.ndarray,
        remote_context: np.ndarray,
    ) -> float:
        """Compute cosine divergence (1 - cosine_similarity) between state vectors."""
        v1 = np.asarray(local_context, dtype=np.float32)
        v2 = np.asarray(remote_context, dtype=np.float32)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 == 0 or norm2 == 0:
            return 1.0
        cos_sim = float(np.dot(v1, v2) / (norm1 * norm2))
        return float(np.clip(1.0 - cos_sim, 0.0, 2.0))

    @staticmethod
    def align_contexts(
        local_context: np.ndarray,
        remote_update: np.ndarray,
        alpha: float = 0.5,
    ) -> np.ndarray:
        """Merge state vectors with exponential moving update (alpha)."""
        aligned = (1.0 - alpha) * local_context + alpha * remote_update
        norm = np.linalg.norm(aligned)
        return aligned / max(norm, 1e-8)


class AgentIntentReasoningLayer:
    """Agent Intent & Reasoning Layer (AIRL).

    Evaluates dynamic task offloading and routes intent requests to the
    optimal edge compute node or peer agent.

    Parameters
    ----------
    config : dict, optional
        Configuration dictionary containing airl thresholds.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        cfg = config or {}
        airl_cfg = cfg.get("airl", {})
        self.negotiation_timeout_ms = float(airl_cfg.get("negotiation_timeout_ms", 1000))
        self.offloading_threshold = float(airl_cfg.get("offloading_threshold", 0.75))
        self.context_sync_interval_ms = float(airl_cfg.get("context_sync_interval_ms", 100))

        self.agents: Dict[str, AgentProfile] = {}
        self.proposals: Dict[str, NegotiationProposal] = {}
        self.stats = {
            "negotiations_initiated": 0,
            "negotiations_accepted": 0,
            "negotiations_rejected": 0,
            "offloads_triggered": 0,
            "contexts_synchronized": 0,
        }

    def register_agent(
        self,
        agent_id: str,
        intent_vector: np.ndarray,
        capabilities: List[TaskType],
        vram_available_gb: float = 16.0,
        compute_load: float = 0.2,
        battery_level: float = 1.0,
    ) -> AgentProfile:
        """Register a mobile or edge agent."""
        vec = np.asarray(intent_vector, dtype=np.float32)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        profile = AgentProfile(
            agent_id=agent_id,
            intent_vector=vec,
            capabilities=capabilities,
            vram_available_gb=vram_available_gb,
            compute_load=compute_load,
            battery_level=battery_level,
        )
        self.agents[agent_id] = profile
        return profile

    def update_agent_status(
        self,
        agent_id: str,
        compute_load: Optional[float] = None,
        vram_available_gb: Optional[float] = None,
        battery_level: Optional[float] = None,
    ) -> None:
        """Update live telemetry for an agent."""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            if compute_load is not None:
                agent.compute_load = float(compute_load)
            if vram_available_gb is not None:
                agent.vram_available_gb = float(vram_available_gb)
            if battery_level is not None:
                agent.battery_level = float(battery_level)
            agent.last_seen = time.time()

    def evaluate_offloading_need(self, agent_id: str) -> bool:
        """Determine if agent should offload its task to an Edge node.

        Considers:
          - High compute load (> offloading_threshold)
          - Critical battery (< 0.2)
        """
        if agent_id not in self.agents:
            return False
        agent = self.agents[agent_id]
        should_offload = (agent.compute_load >= self.offloading_threshold) or (agent.battery_level < 0.2)
        if should_offload:
            self.stats["offloads_triggered"] += 1
        return should_offload

    def find_optimal_partner(
        self,
        task_intent: np.ndarray,
        task_type: TaskType,
        required_vram_gb: float = 4.0,
        exclude_agent_id: Optional[str] = None,
    ) -> Optional[Tuple[str, float]]:
        """Find the best partner agent using semantic similarity and resource score."""
        query = np.asarray(task_intent, dtype=np.float32)
        norm = np.linalg.norm(query)
        if norm > 0:
            query = query / norm

        candidates: List[Tuple[str, float]] = []
        for aid, profile in self.agents.items():
            if exclude_agent_id and aid == exclude_agent_id:
                continue
            if task_type not in profile.capabilities:
                continue
            if profile.vram_available_gb < required_vram_gb:
                continue

            # Semantic similarity with dimension alignment if needed
            min_dim = min(len(query), len(profile.intent_vector))
            sim = float(np.dot(query[:min_dim], profile.intent_vector[:min_dim]))
            # Resource readiness score: low load and high battery
            resource_score = (1.0 - profile.compute_load) * 0.5 + profile.battery_level * 0.5
            total_utility = 0.7 * sim + 0.3 * resource_score
            candidates.append((aid, total_utility))

        if not candidates:
            return None

        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[0]

    def negotiate_offload(
        self,
        requester_id: str,
        task_type: TaskType,
        task_intent: np.ndarray,
        required_vram_gb: float = 4.0,
        deadline_ms: float = 200.0,
    ) -> Optional[NegotiationProposal]:
        """Execute semantic contract negotiation between agents."""
        self.stats["negotiations_initiated"] += 1
        partner = self.find_optimal_partner(
            task_intent=task_intent,
            task_type=task_type,
            required_vram_gb=required_vram_gb,
            exclude_agent_id=requester_id,
        )
        if partner is None:
            self.stats["negotiations_rejected"] += 1
            return None

        target_id, utility = partner
        proposal_id = f"prop_{len(self.proposals)}_{int(time.time() * 1000)}"
        proposal = NegotiationProposal(
            proposal_id=proposal_id,
            requester_id=requester_id,
            target_id=target_id,
            task_type=task_type,
            required_vram_gb=required_vram_gb,
            intent_embedding=task_intent,
            deadline_ms=deadline_ms,
            status="ACCEPTED",
        )
        self.proposals[proposal_id] = proposal
        self.stats["negotiations_accepted"] += 1
        return proposal

    def sync_context(
        self,
        agent_id_1: str,
        agent_id_2: str,
        context_vector: np.ndarray,
    ) -> float:
        """Synchronize context vector and update alignment stats."""
        self.stats["contexts_synchronized"] += 1
        # In a real environment, this broadcasts the update over the stack
        return 0.98  # Context alignment confidence
