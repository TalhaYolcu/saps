"""Unit tests for Layer 2 — Semantic-Priority MAC (SP-MAC)."""

import pytest
from saps.layers.datalink import CriticalityLevel, Frame, SPMACScheduler, DataLinkLayer


def test_spmac_scheduler_priority_order():
    sched = SPMACScheduler(num_queues=4)

    f_low = Frame(frame_id=1, payload="low_data", criticality=CriticalityLevel.LOW, token_entropy=0.2, timestamp=1.0, size_bytes=100)
    f_crit = Frame(frame_id=2, payload="crit_data", criticality=CriticalityLevel.CRITICAL, token_entropy=3.1, timestamp=2.0, size_bytes=100)
    f_med = Frame(frame_id=3, payload="med_data", criticality=CriticalityLevel.MEDIUM, token_entropy=1.2, timestamp=3.0, size_bytes=100)

    # Enqueue in reverse order
    sched.enqueue(f_low)
    sched.enqueue(f_crit)
    sched.enqueue(f_med)

    # Dequeue must return CRITICAL first, then MEDIUM, then LOW
    out1 = sched.dequeue()
    out2 = sched.dequeue()
    out3 = sched.dequeue()

    assert out1.frame_id == 2  # CRITICAL
    assert out2.frame_id == 3  # MEDIUM
    assert out3.frame_id == 1  # LOW


def test_datalink_layer_wrapper():
    dl = DataLinkLayer({"num_priority_queues": 4})
    frame = dl.send(payload="test", criticality=CriticalityLevel.CRITICAL, token_entropy=2.5, size_bytes=50)
    assert frame.criticality == CriticalityLevel.CRITICAL
    rec = dl.receive()
    assert rec.frame_id == frame.frame_id
