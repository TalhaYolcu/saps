"""
Layer 5 — Application Layer: Direct KV-Cache & Latent Vector Streaming
========================================================================

Replaces verbose serialization (JSON/Protobuf over REST/gRPC) with direct
KV-cache compression and latent feature vector streaming between AI agents.

Key components:
  * :class:`KVCacheSerializer` — Compresses & serializes transformer KV-cache
    tensors via dimension reduction and quantization.
  * :class:`LatentVectorStream` — Managed buffer for streaming latent vectors
    with flow control and semantic chunking.
  * :class:`ApplicationLayer` — Stack interface connecting agent models to
    the transport layer.
"""

from __future__ import annotations

import io
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import torch


@dataclass
class StreamChunk:
    """A chunk of latent vectors or serialized KV cache ready for transport."""
    chunk_id: int
    data: np.ndarray
    latent_dim: int
    num_tokens: int
    token_entropy: float
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


class KVCacheSerializer:
    """Serializes and compresses transformer Key-Value caches.

    Traditional approaches serialize KV caches into bulky JSON or uncompressed
    Protobuf messages. This serializer applies:
      1. SVD / PCA dimensionality projection or truncation
      2. 8-bit dynamic quantization
      3. Token-criticality masking

    Parameters
    ----------
    compression_ratio : float
        Target compression ratio (0.1 to 1.0).
    latent_dim : int
        Dimension of latent embeddings per token.
    quantize_bits : int
        Bit-width for quantization (e.g. 8).
    """

    def __init__(
        self,
        compression_ratio: float = 0.5,
        latent_dim: int = 256,
        quantize_bits: int = 8,
    ) -> None:
        self.compression_ratio = np.clip(compression_ratio, 0.1, 1.0)
        self.latent_dim = latent_dim
        self.quantize_bits = quantize_bits

    def compress_tensor(self, tensor: np.ndarray) -> Tuple[np.ndarray, Dict[str, float]]:
        """Quantize and compress an arbitrary float tensor.

        Returns
        -------
        quantized : np.ndarray (int8 or uint8)
        scale_dict : dict containing min and scale for dequantization
        """
        arr = np.asarray(tensor, dtype=np.float32)
        min_val = float(np.min(arr))
        max_val = float(np.max(arr))
        range_val = max(max_val - min_val, 1e-8)

        scale = (2 ** self.quantize_bits - 1) / range_val
        quantized = np.clip(np.round((arr - min_val) * scale), 0, 2 ** self.quantize_bits - 1).astype(np.uint8)

        return quantized, {"min_val": min_val, "scale": scale, "shape": list(arr.shape)}

    def decompress_tensor(self, quantized: np.ndarray, meta: Dict[str, Any]) -> np.ndarray:
        """Reconstruct float tensor from quantized representation."""
        arr = quantized.astype(np.float32)
        min_val = meta["min_val"]
        scale = meta["scale"]
        shape = tuple(meta["shape"])
        dequantized = (arr / scale) + min_val
        return dequantized.reshape(shape)

    def serialize_kv(self, k_cache: np.ndarray, v_cache: np.ndarray) -> Dict[str, Any]:
        """Compress both K and V caches into a compact transmission payload."""
        # Optional rank reduction based on compression_ratio
        k_shape = k_cache.shape
        v_shape = v_cache.shape

        keep_k = max(1, int(k_cache.shape[-1] * self.compression_ratio))
        k_reduced = k_cache[..., :keep_k]
        v_reduced = v_cache[..., :keep_k]

        k_quant, k_meta = self.compress_tensor(k_reduced)
        v_quant, v_meta = self.compress_tensor(v_reduced)

        original_bytes = (k_cache.nbytes + v_cache.nbytes)
        compressed_bytes = (k_quant.nbytes + v_quant.nbytes)
        actual_ratio = compressed_bytes / max(original_bytes, 1)

        return {
            "k_quant": k_quant,
            "k_meta": k_meta,
            "v_quant": v_quant,
            "v_meta": v_meta,
            "original_k_shape": k_shape,
            "original_v_shape": v_shape,
            "original_bytes": original_bytes,
            "compressed_bytes": compressed_bytes,
            "compression_ratio": actual_ratio,
        }

    def deserialize_kv(self, payload: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """Reconstruct K and V caches from received compressed payload."""
        k_rec = self.decompress_tensor(payload["k_quant"], payload["k_meta"])
        v_rec = self.decompress_tensor(payload["v_quant"], payload["v_meta"])

        orig_k_shape = payload["original_k_shape"]
        orig_v_shape = payload["original_v_shape"]

        # Zero-pad back to original dimension if truncated
        if k_rec.shape != orig_k_shape:
            k_full = np.zeros(orig_k_shape, dtype=np.float32)
            k_full[..., :k_rec.shape[-1]] = k_rec
            k_rec = k_full

        if v_rec.shape != orig_v_shape:
            v_full = np.zeros(orig_v_shape, dtype=np.float32)
            v_full[..., :v_rec.shape[-1]] = v_rec
            v_rec = v_full

        return k_rec, v_rec


class LatentVectorStream:
    """Managed FIFO buffer for streaming high-dimensional latent vectors."""

    def __init__(self, vector_dim: int = 256, buffer_capacity: int = 1024) -> None:
        self.vector_dim = vector_dim
        self.buffer_capacity = buffer_capacity
        self._buffer: List[StreamChunk] = []
        self._chunk_counter = 0

    def push(
        self,
        vectors: np.ndarray,
        entropy: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> StreamChunk:
        """Push a batch of latent vectors into the stream."""
        arr = np.asarray(vectors, dtype=np.float32)
        num_tokens = arr.shape[0] if arr.ndim > 1 else 1

        chunk = StreamChunk(
            chunk_id=self._chunk_counter,
            data=arr,
            latent_dim=self.vector_dim,
            num_tokens=num_tokens,
            token_entropy=entropy,
            metadata=metadata or {},
        )
        self._chunk_counter += 1
        self._buffer.append(chunk)

        if len(self._buffer) > self.buffer_capacity:
            self._buffer.pop(0)  # Drop oldest on overflow

        return chunk

    def pop(self) -> Optional[StreamChunk]:
        """Retrieve and remove the next chunk in FIFO order."""
        if not self._buffer:
            return None
        return self._buffer.pop(0)

    def is_empty(self) -> bool:
        return len(self._buffer) == 0

    @property
    def size(self) -> int:
        return len(self._buffer)


class ApplicationLayer:
    """Application Layer wrapper for the SAPS protocol stack.

    Provides direct model-to-stack serialization of latent vectors and KV cache.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        cfg = config or {}
        app_cfg = cfg.get("application_layer", {})
        self.compression_ratio = float(app_cfg.get("compression_ratio", 0.5))
        self.latent_dim = int(app_cfg.get("latent_vector_dim", 256))

        self.serializer = KVCacheSerializer(
            compression_ratio=self.compression_ratio,
            latent_dim=self.latent_dim,
        )
        self.stream = LatentVectorStream(vector_dim=self.latent_dim)

    def prepare_payload(
        self,
        latent_vectors: np.ndarray,
        token_entropy: float = 1.0,
        intent: Optional[str] = None,
    ) -> StreamChunk:
        """Prepare an application layer chunk ready to descend into IA-STP transport."""
        metadata = {"intent": intent or "inference"}
        return self.stream.push(latent_vectors, entropy=token_entropy, metadata=metadata)

    def process_incoming_chunk(self, chunk: StreamChunk) -> np.ndarray:
        """Receive a stream chunk reconstructed by the physical & transport layers."""
        return chunk.data
