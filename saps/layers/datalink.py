"""
Semantic-Priority MAC (SP-MAC) Data Link Layer
=================================================

Implements a multi-queue MAC scheduler that prioritises frames based on
their **semantic criticality** — a tag derived from token entropy and
intent analysis higher up in the SAPS stack.

Key components:
  * :class:`CriticalityLevel` — priority enum (CRITICAL → LOW).
  * :class:`Frame` — data-link frame carrying a payload with metadata.
  * :class:`SPMACScheduler` — multi-level priority queue scheduler.
  * :class:`DataLinkLayer` — stack-level wrapper.
"""

from __future__ import annotations

import heapq
import itertools
import time
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Priority levels
# ---------------------------------------------------------------------------

class CriticalityLevel(IntEnum):
    """Semantic criticality levels (lower value = higher priority)."""

    CRITICAL = 0   # Safety / emergency — must be delivered first
    HIGH = 1       # High-value semantic content
    MEDIUM = 2     # Normal agent communication
    LOW = 3        # Best-effort background traffic


# ---------------------------------------------------------------------------
# Frame
# ---------------------------------------------------------------------------

@dataclass
class Frame:
    """A data-link layer frame with semantic-priority metadata.

    Attributes
    ----------
    frame_id : int
        Unique frame identifier.
    payload : Any
        Arbitrary payload (bytes, tensor, dict, …).
    criticality : CriticalityLevel
        Semantic criticality tag used for scheduling.
    token_entropy : float
        Average token entropy of the payload (bits).  Higher entropy
        ⟹ more information content.
    timestamp : float
        Creation timestamp (``time.time()``).
    size_bytes : int
        Logical payload size in bytes.
    """

    frame_id: int
    payload: Any
    criticality: CriticalityLevel
    token_entropy: float
    timestamp: float
    size_bytes: int


# ---------------------------------------------------------------------------
# Internal heap entry (comparable)
# ---------------------------------------------------------------------------

@dataclass(order=True)
class _HeapEntry:
    """Wrapper that makes :class:`Frame` heap-sortable.

    Sorting order: ``(criticality, sequence_number)``.
    The sequence number guarantees FIFO within the same priority level
    and avoids comparing ``Frame`` objects directly.
    """

    criticality: int
    seq: int
    frame: Frame = field(compare=False)


# ---------------------------------------------------------------------------
# SP-MAC Scheduler
# ---------------------------------------------------------------------------

class SPMACScheduler:
    """Semantic-Priority MAC scheduler.

    Maintains one logical priority queue per :class:`CriticalityLevel`.
    Internally uses a single min-heap keyed by
    ``(criticality, insertion_order)`` so that:

    1. Frames with a lower (= more critical) criticality are dequeued
       first.
    2. Within the same level, frames are served FIFO.

    Parameters
    ----------
    num_queues : int
        Number of distinct priority levels to support (default 4,
        matching the four :class:`CriticalityLevel` values).
    """

    def __init__(self, num_queues: int = 4) -> None:
        self.num_queues: int = num_queues
        self._heap: List[_HeapEntry] = []
        self._counter: itertools.count = itertools.count()  # monotonic seq
        # Per-level bookkeeping
        self._level_counts: Dict[int, int] = {i: 0 for i in range(num_queues)}
        self._level_enqueued_total: Dict[int, int] = {i: 0 for i in range(num_queues)}
        self._level_dequeued_total: Dict[int, int] = {i: 0 for i in range(num_queues)}
        self._level_wait_sum: Dict[int, float] = {i: 0.0 for i in range(num_queues)}

    # ---- Core API --------------------------------------------------------

    def enqueue(self, frame: Frame) -> None:
        """Add *frame* to the appropriate priority queue.

        Parameters
        ----------
        frame : Frame
            The frame to schedule.  Its ``criticality`` field determines
            the queue.
        """
        level: int = int(frame.criticality)
        entry = _HeapEntry(
            criticality=level,
            seq=next(self._counter),
            frame=frame,
        )
        heapq.heappush(self._heap, entry)
        self._level_counts[level] = self._level_counts.get(level, 0) + 1
        self._level_enqueued_total[level] = self._level_enqueued_total.get(level, 0) + 1

    def dequeue(self) -> Optional[Frame]:
        """Remove and return the highest-priority frame.

        Returns the frame with the **lowest** criticality number
        (highest priority).  Ties are broken by insertion order (FIFO).

        Returns
        -------
        Frame or None
            The next frame to transmit, or ``None`` if all queues are
            empty.
        """
        if not self._heap:
            return None
        entry: _HeapEntry = heapq.heappop(self._heap)
        frame: Frame = entry.frame
        level: int = int(frame.criticality)
        self._level_counts[level] = max(0, self._level_counts.get(level, 0) - 1)
        self._level_dequeued_total[level] = self._level_dequeued_total.get(level, 0) + 1

        wait_time: float = time.time() - frame.timestamp
        self._level_wait_sum[level] = self._level_wait_sum.get(level, 0.0) + wait_time

        return frame

    # ---- Inspection ------------------------------------------------------

    @property
    def total_pending(self) -> int:
        """Total number of frames waiting across all queues."""
        return len(self._heap)

    def is_empty(self) -> bool:
        """Return ``True`` if there are no pending frames."""
        return len(self._heap) == 0

    def peek(self) -> Optional[Frame]:
        """Return the highest-priority frame without removing it.

        Returns
        -------
        Frame or None
        """
        if not self._heap:
            return None
        return self._heap[0].frame

    def get_queue_stats(self) -> Dict[str, Any]:
        """Return per-queue statistics.

        Returns
        -------
        dict
            Keys are ``"total_pending"`` and ``"queues"`` (a list of
            dicts with ``level``, ``name``, ``pending``, ``enqueued``,
            ``dequeued``, and ``avg_wait_s`` for each level).
        """
        queues: List[Dict[str, Any]] = []
        for level in range(self.num_queues):
            dequeued: int = self._level_dequeued_total.get(level, 0)
            avg_wait: float = (
                self._level_wait_sum.get(level, 0.0) / dequeued
                if dequeued > 0
                else 0.0
            )
            try:
                name = CriticalityLevel(level).name
            except ValueError:
                name = f"LEVEL_{level}"
            queues.append(
                {
                    "level": level,
                    "name": name,
                    "pending": self._level_counts.get(level, 0),
                    "enqueued": self._level_enqueued_total.get(level, 0),
                    "dequeued": dequeued,
                    "avg_wait_s": round(avg_wait, 6),
                }
            )
        return {"total_pending": self.total_pending, "queues": queues}


# ---------------------------------------------------------------------------
# Data Link Layer wrapper
# ---------------------------------------------------------------------------

class DataLinkLayer:
    """Data-Link Layer for the SAPS protocol stack.

    Provides ``send`` / ``receive`` semantics on top of the
    :class:`SPMACScheduler`.

    Parameters
    ----------
    config : dict
        Configuration dictionary.  Recognised keys:

        * ``num_queues`` (int, default 4)
        * ``max_frame_bytes`` (int, default 1500)
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config: Dict[str, Any] = config
        num_queues: int = config.get("num_queues", 4)
        self.max_frame_bytes: int = config.get("max_frame_bytes", 1500)

        self.scheduler = SPMACScheduler(num_queues=num_queues)
        self._frame_counter: itertools.count = itertools.count()
        self._rx_buffer: List[Frame] = []

    def send(
        self,
        data: Any = None,
        criticality: CriticalityLevel | int = CriticalityLevel.MEDIUM,
        token_entropy: float = 0.0,
        size_bytes: Optional[int] = None,
        payload: Any = None,
    ) -> Frame:
        """Create a frame and schedule it for transmission.

        Parameters
        ----------
        data : Any, optional
            Payload to encapsulate.
        criticality : CriticalityLevel or int
            Semantic criticality level.
        token_entropy : float
            Average token entropy of the payload (bits).
        size_bytes : int or None
            Payload size.  If ``None``, estimated via ``len(data)`` for
            bytes-like objects or defaults to 0.
        payload : Any, optional
            Alias for `data`.

        Returns
        -------
        Frame
            The created frame (already enqueued).
        """
        content = payload if payload is not None else data
        if isinstance(criticality, int) and not isinstance(criticality, CriticalityLevel):
            criticality = CriticalityLevel(criticality)

        if size_bytes is None:
            try:
                size_bytes = len(content)  # type: ignore[arg-type]
            except TypeError:
                size_bytes = 0

        frame = Frame(
            frame_id=next(self._frame_counter),
            payload=content,
            criticality=criticality,
            token_entropy=token_entropy,
            timestamp=time.time(),
            size_bytes=min(size_bytes, self.max_frame_bytes),
        )
        self.scheduler.enqueue(frame)
        return frame

    def receive(self) -> Optional[Frame]:
        """Dequeue and return the next scheduled frame.

        Returns
        -------
        Frame or None
            The highest-priority pending frame, or ``None`` if there
            are no frames to deliver.
        """
        frame = self.scheduler.dequeue()
        if frame is not None:
            self._rx_buffer.append(frame)
        return frame

    def receive_all(self) -> List[Frame]:
        """Drain the scheduler and return all pending frames in priority order.

        Returns
        -------
        list of Frame
        """
        frames: List[Frame] = []
        while not self.scheduler.is_empty():
            frame = self.receive()
            if frame is not None:
                frames.append(frame)
        return frames

    def get_stats(self) -> Dict[str, Any]:
        """Return scheduler statistics plus receive-buffer size.

        Returns
        -------
        dict
        """
        stats = self.scheduler.get_queue_stats()
        stats["rx_buffer_size"] = len(self._rx_buffer)
        return stats

    def get_queue_stats(self) -> Dict[str, Any]:
        """Alias for get_stats()."""
        return self.get_stats()
