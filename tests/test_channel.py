"""Unit tests for wireless channel fading models."""

import numpy as np
import pytest
from saps.channel.fading import AWGNChannel, RayleighChannel, RicianChannel, calculate_ber, calculate_capacity


def test_awgn_channel_preserves_shape():
    chan = AWGNChannel()
    sig = np.ones(100, dtype=np.complex128)
    rx = chan.forward(sig, snr_db=20.0)
    assert rx.shape == sig.shape
    assert rx.dtype == np.complex128


def test_awgn_high_snr_low_distortion():
    chan = AWGNChannel()
    sig = np.ones(500, dtype=np.complex128)
    rx = chan.forward(sig, snr_db=40.0)
    mse = np.mean(np.abs(sig - rx) ** 2)
    assert mse < 1e-3


def test_rayleigh_fading_magnitudes():
    chan = RayleighChannel(num_taps=1, doppler_freq=10.0)
    sig = np.ones(2000, dtype=np.complex128)
    rx = chan.forward(sig, snr_db=20.0)
    # Magnitudes should exhibit Rayleigh-like variations
    mags = np.abs(rx)
    assert np.mean(mags) > 0.5
    assert np.std(mags) > 0.1


def test_rician_k_factor():
    chan = RicianChannel(k_factor=10.0, doppler_freq=10.0)
    sig = np.ones(1000, dtype=np.complex128)
    rx = chan.forward(sig, snr_db=25.0)
    assert rx.shape == sig.shape


def test_calculate_ber():
    tx = np.array([0, 1, 1, 0, 1, 0])
    rx = np.array([0, 1, 0, 0, 1, 1])
    ber = calculate_ber(tx, rx)
    assert np.isclose(ber, 2 / 6)


def test_calculate_capacity():
    c_low = calculate_capacity(snr_db=0.0, bandwidth=1.0)
    c_high = calculate_capacity(snr_db=20.0, bandwidth=1.0)
    assert c_high > c_low
