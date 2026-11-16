"""Unit tests for NVIDIA Sionna channel integration."""

import numpy as np
import pytest

from saps.channel.sionna_channel import (
    SIONNA_AVAILABLE,
    SionnaAWGNChannel,
    SionnaFlatFadingChannel,
    Sionna3GPPChannel,
)


@pytest.mark.skipif(not SIONNA_AVAILABLE, reason="NVIDIA Sionna is not installed")
def test_sionna_awgn_channel():
    chan = SionnaAWGNChannel()
    sig = np.ones(64, dtype=np.complex128)
    rx = chan.forward(sig, snr_db=30.0)

    assert rx.shape == sig.shape
    assert rx.dtype == np.complex64 or rx.dtype == np.complex128
    # At 30 dB SNR, error should be tiny
    mse = np.mean(np.abs(sig - rx) ** 2)
    assert mse < 0.05


@pytest.mark.skipif(not SIONNA_AVAILABLE, reason="NVIDIA Sionna is not installed")
def test_sionna_flat_fading_channel():
    chan = SionnaFlatFadingChannel(num_tx_ant=1, num_rx_ant=1)
    sig = np.ones(32, dtype=np.complex128)
    rx = chan.forward(sig, snr_db=20.0)

    assert rx.shape == sig.shape
    # Output should not be all zeros or all NaNs
    assert not np.any(np.isnan(rx))
    assert np.mean(np.abs(rx)) > 0.0


@pytest.mark.skipif(not SIONNA_AVAILABLE, reason="NVIDIA Sionna is not installed")
def test_sionna_3gpp_channel():
    chan = Sionna3GPPChannel(scenario="UMi", doppler_freq_hz=50.0)
    sig = np.ones(32, dtype=np.complex128)
    rx = chan.forward(sig, snr_db=15.0)

    assert rx.shape == sig.shape
    assert not np.any(np.isnan(rx))
