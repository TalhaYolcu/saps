"""Unit tests for Layer 5 — KV-Cache & Latent Vector Application Layer."""

import numpy as np
import pytest
from saps.layers.application import KVCacheSerializer, LatentVectorStream, ApplicationLayer


def test_kv_cache_compression_and_reconstruction(sample_kv_cache):
    k, v = sample_kv_cache
    serializer = KVCacheSerializer(compression_ratio=0.5, quantize_bits=8)

    payload = serializer.serialize_kv(k, v)
    assert payload["compressed_bytes"] < payload["original_bytes"]

    k_rec, v_rec = serializer.deserialize_kv(payload)
    assert k_rec.shape == k.shape
    assert v_rec.shape == v.shape

    # Check reconstruction correlation
    corr = np.corrcoef(k.flatten()[:100], k_rec.flatten()[:100])[0, 1]
    assert corr > 0.70


def test_latent_vector_stream():
    stream = LatentVectorStream(vector_dim=128, buffer_capacity=10)
    data = np.random.randn(4, 128).astype(np.float32)

    chunk = stream.push(data, entropy=1.8, metadata={"layer": 5})
    assert chunk.num_tokens == 4
    assert stream.size == 1

    popped = stream.pop()
    assert popped.chunk_id == chunk.chunk_id
    assert stream.is_empty()


def test_application_layer_wrapper():
    app = ApplicationLayer({"application_layer": {"compression_ratio": 0.5, "latent_vector_dim": 64}})
    vec = np.random.randn(64).astype(np.float32)
    chunk = app.prepare_payload(vec, token_entropy=1.5)
    rec = app.process_incoming_chunk(chunk)
    assert np.allclose(vec, rec)
