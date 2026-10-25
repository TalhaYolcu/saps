"""Unit tests for Layer 1 — Deep-JSCC Neural Transceiver."""

import numpy as np
import torch
import pytest
from saps.layers.physical import DeepJSCCEncoder, DeepJSCCDecoder, DeepJSCCTransceiver, PhysicalLayer


def test_encoder_output_dimensions():
    encoder = DeepJSCCEncoder(input_dim=256, hidden_dim=128, iq_dim=64)
    x = torch.randn(8, 256)
    out = encoder(x)
    assert out.shape == (8, 64)
    assert out.is_complex()


def test_encoder_power_normalization():
    encoder = DeepJSCCEncoder(input_dim=256, hidden_dim=128, iq_dim=64)
    x = torch.randn(16, 256)
    out = encoder(x)
    power = torch.mean(out.abs() ** 2, dim=1)
    # Each sample's mean symbol power should be approximately 1.0
    assert torch.allclose(power, torch.ones_like(power), atol=1e-2)


def test_decoder_output_dimensions():
    decoder = DeepJSCCDecoder(iq_dim=64, hidden_dim=128, output_dim=256)
    noisy_iq = torch.randn(8, 64, dtype=torch.complex64)
    out = decoder(noisy_iq)
    assert out.shape == (8, 256)


def test_transceiver_end_to_end_forward():
    transceiver = DeepJSCCTransceiver(latent_dim=256, hidden_dim=128, iq_dim=64)
    x = torch.randn(4, 256)
    rec = transceiver(x, snr_db=20.0)
    assert rec.shape == x.shape


def test_physical_layer_wrapper():
    phy = PhysicalLayer({"latent_dim": 256, "hidden_dim": 128, "iq_dim": 64})
    vec = np.random.randn(256).astype(np.float32)
    rec = phy.transmit(vec, snr_db=25.0)
    assert rec.shape == vec.shape
    assert isinstance(rec, np.ndarray)
