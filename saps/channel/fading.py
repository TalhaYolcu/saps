"""
Wireless Channel Fading Models
================================

Fully-working channel simulators for the SAPS physical-layer evaluation.

Models implemented:
  * **AWGNChannel**    – Additive White Gaussian Noise (baseline).
  * **RayleighChannel** – Flat/frequency-selective Rayleigh fading with
    Jakes Doppler spectrum for mobile (NLOS) scenarios.
  * **RicianChannel**  – Rician fading with a tuneable K-factor for
    scenarios that include a line-of-sight component.

All models operate on complex-baseband signals represented as
``np.ndarray`` with dtype ``complex128``.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class ChannelModel(ABC):
    """Abstract base class for wireless channel models.

    Subclasses must implement :meth:`forward` which takes a complex
    baseband signal and an SNR value (in dB) and returns the received
    signal after fading and noise.
    """

    @abstractmethod
    def forward(self, signal: np.ndarray, snr_db: float) -> np.ndarray:
        """Pass *signal* through the channel at the given *snr_db*.

        Parameters
        ----------
        signal : np.ndarray
            Transmitted complex baseband signal (1-D).
        snr_db : float
            Signal-to-noise ratio in decibels.

        Returns
        -------
        np.ndarray
            Received complex baseband signal (same length as *signal*).
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _add_awgn(signal: np.ndarray, snr_db: float) -> np.ndarray:
    """Add complex AWGN to *signal* so that the received SNR equals *snr_db*.

    The noise power is computed relative to the *actual* signal power:

    .. math::
        \\sigma_n^2 = P_{\\text{sig}} \\cdot 10^{-\\text{SNR}_{\\text{dB}} / 10}

    Each noise sample is drawn from
    :math:`\\mathcal{CN}(0,\\,\\sigma_n^2)`.

    Parameters
    ----------
    signal : np.ndarray
        Input complex signal.
    snr_db : float
        Desired SNR in dB.

    Returns
    -------
    np.ndarray
        Signal plus noise.
    """
    sig_power: float = float(np.mean(np.abs(signal) ** 2))
    if sig_power == 0.0:
        return signal.copy()
    snr_linear: float = 10.0 ** (snr_db / 10.0)
    noise_power: float = sig_power / snr_linear
    # Complex Gaussian: each of I/Q has variance noise_power / 2
    noise = np.sqrt(noise_power / 2.0) * (
        np.random.randn(*signal.shape) + 1j * np.random.randn(*signal.shape)
    )
    return signal + noise


# ---------------------------------------------------------------------------
# AWGN Channel
# ---------------------------------------------------------------------------

class AWGNChannel(ChannelModel):
    """Additive White Gaussian Noise channel (no fading).

    This is the simplest channel model: the received signal is

    .. math::
        y[n] = x[n] + w[n]

    where :math:`w[n] \\sim \\mathcal{CN}(0,\\,\\sigma_n^2)`.
    """

    def forward(self, signal: np.ndarray, snr_db: float) -> np.ndarray:
        """Add AWGN noise at the specified SNR.

        Parameters
        ----------
        signal : np.ndarray
            Transmitted complex baseband signal.
        snr_db : float
            Signal-to-noise ratio (dB).

        Returns
        -------
        np.ndarray
            Noisy received signal.
        """
        signal = np.asarray(signal, dtype=np.complex128)
        return _add_awgn(signal, snr_db)


# ---------------------------------------------------------------------------
# Rayleigh Fading Channel
# ---------------------------------------------------------------------------

class RayleighChannel(ChannelModel):
    """Rayleigh fading channel for mobile NLOS scenarios.

    Implements a tapped-delay-line model with ``num_taps`` independent
    Rayleigh fading taps.  Time-varying fading coefficients are
    generated using the **Jakes (sum-of-sinusoids)** Doppler model.

    Parameters
    ----------
    num_taps : int
        Number of channel taps (1 = flat fading).
    doppler_freq : float
        Maximum Doppler frequency :math:`f_d` in Hz.  Relates to mobile
        speed *v* by :math:`f_d = v \\cdot f_c / c`.
    sample_rate : float
        Signal sample rate in Hz.  Used together with *doppler_freq*
        to derive the normalised Doppler spread.
    num_sinusoids : int
        Number of sinusoids in the Jakes model (higher ⇒ more accurate).
    """

    def __init__(
        self,
        num_taps: int = 1,
        doppler_freq: float = 10.0,
        sample_rate: float = 1000.0,
        num_sinusoids: int = 16,
    ) -> None:
        self.num_taps: int = max(1, num_taps)
        self.doppler_freq: float = doppler_freq
        self.sample_rate: float = sample_rate
        self.num_sinusoids: int = num_sinusoids

    # -- Jakes model ----------------------------------------------------------

    def _jakes_fading(self, length: int) -> np.ndarray:
        """Generate a single time-varying Rayleigh fading process.

        Uses the Jakes / sum-of-sinusoids method.  The returned
        envelope has unit average power, i.e.
        :math:`\\mathbb{E}[|h|^2] = 1`.

        Parameters
        ----------
        length : int
            Number of fading samples to generate.

        Returns
        -------
        np.ndarray
            Complex fading coefficients of shape ``(length,)``.
        """
        N: int = self.num_sinusoids
        fd: float = self.doppler_freq
        ts: float = 1.0 / self.sample_rate

        t = np.arange(length) * ts  # time vector (seconds)

        # Random initial phases per sinusoid
        theta = np.random.uniform(0, 2 * np.pi, size=N)
        phi = np.random.uniform(0, 2 * np.pi, size=N)

        # Arrival angles uniformly spaced + random offset
        alpha = (2 * np.pi * np.arange(1, N + 1) + theta) / (4 * N)

        # Sum-of-sinusoids for in-phase and quadrature
        h_i = np.zeros(length, dtype=np.float64)
        h_q = np.zeros(length, dtype=np.float64)
        for k in range(N):
            cos_doppler = np.cos(2 * np.pi * fd * np.cos(alpha[k]) * t + phi[k])
            h_i += cos_doppler * np.cos(alpha[k])
            h_q += cos_doppler * np.sin(alpha[k])

        # Normalise so E[|h|^2] = 1
        h = (h_i + 1j * h_q) * np.sqrt(2.0 / N)
        return h

    # -- Forward pass ----------------------------------------------------------

    def forward(self, signal: np.ndarray, snr_db: float) -> np.ndarray:
        """Apply Rayleigh fading and AWGN to *signal*.

        For ``num_taps == 1`` (flat fading) the channel is simply:

        .. math::
            y[n] = h[n] \\cdot x[n] + w[n]

        For ``num_taps > 1`` (frequency-selective) a tapped-delay-line
        convolution is applied with independent fading per tap and an
        exponentially-decaying power-delay profile.

        Parameters
        ----------
        signal : np.ndarray
            Transmitted complex baseband signal.
        snr_db : float
            Signal-to-noise ratio (dB).

        Returns
        -------
        np.ndarray
            Received signal (same length as *signal*).
        """
        signal = np.asarray(signal, dtype=np.complex128)
        length: int = signal.shape[0]

        if self.num_taps == 1:
            # ---- Flat fading ----
            h = self._jakes_fading(length)
            faded = h * signal
        else:
            # ---- Frequency-selective fading ----
            # Exponential power-delay profile (normalised to unit total)
            tap_powers = np.exp(-np.arange(self.num_taps, dtype=np.float64))
            tap_powers /= tap_powers.sum()

            faded = np.zeros(length, dtype=np.complex128)
            for tap_idx in range(self.num_taps):
                h_tap = self._jakes_fading(length) * np.sqrt(tap_powers[tap_idx])
                delayed = np.roll(signal, tap_idx) * h_tap
                # Zero out the wrapped-around samples
                delayed[:tap_idx] = 0.0
                faded += delayed

        return _add_awgn(faded, snr_db)


# ---------------------------------------------------------------------------
# Rician Fading Channel
# ---------------------------------------------------------------------------

class RicianChannel(ChannelModel):
    """Rician fading channel (LoS + scattered components).

    The fading coefficient is:

    .. math::
        h[n] = \\sqrt{\\frac{K}{K+1}}\\,e^{j2\\pi f_d t[n]}
             + \\sqrt{\\frac{1}{K+1}}\\,h_{\\text{Rayleigh}}[n]

    where *K* is the Rician K-factor (ratio of LoS power to scattered
    power in linear scale).

    Parameters
    ----------
    k_factor : float
        Rician K-factor in **linear** scale (not dB).  ``K = 0`` reduces
        to Rayleigh; ``K → ∞`` approaches AWGN.
    doppler_freq : float
        Maximum Doppler frequency (Hz).
    sample_rate : float
        Signal sample rate (Hz).
    num_sinusoids : int
        Number of sinusoids for the scattered (Rayleigh) component.
    """

    def __init__(
        self,
        k_factor: float = 3.0,
        doppler_freq: float = 10.0,
        sample_rate: float = 1000.0,
        num_sinusoids: int = 16,
    ) -> None:
        self.k_factor: float = max(0.0, k_factor)
        self.doppler_freq: float = doppler_freq
        self.sample_rate: float = sample_rate
        self.num_sinusoids: int = num_sinusoids

        # Internal Rayleigh generator for the scattered component
        self._rayleigh = RayleighChannel(
            num_taps=1,
            doppler_freq=doppler_freq,
            sample_rate=sample_rate,
            num_sinusoids=num_sinusoids,
        )

    def forward(self, signal: np.ndarray, snr_db: float) -> np.ndarray:
        """Apply Rician fading and AWGN to *signal*.

        Parameters
        ----------
        signal : np.ndarray
            Transmitted complex baseband signal.
        snr_db : float
            Signal-to-noise ratio (dB).

        Returns
        -------
        np.ndarray
            Received signal (same length as *signal*).
        """
        signal = np.asarray(signal, dtype=np.complex128)
        length: int = signal.shape[0]
        K: float = self.k_factor

        # --- LoS component ---
        ts: float = 1.0 / self.sample_rate
        t = np.arange(length) * ts
        # LoS arrives at angle 0 ⇒ Doppler shift = f_d
        los_phase = np.random.uniform(0, 2 * np.pi)
        h_los = np.exp(1j * (2 * np.pi * self.doppler_freq * t + los_phase))
        h_los *= np.sqrt(K / (K + 1.0))

        # --- Scattered (Rayleigh) component ---
        h_scatter = self._rayleigh._jakes_fading(length)
        h_scatter *= np.sqrt(1.0 / (K + 1.0))

        # --- Combined fading ---
        h = h_los + h_scatter
        faded = h * signal

        return _add_awgn(faded, snr_db)


# ---------------------------------------------------------------------------
# Performance metrics
# ---------------------------------------------------------------------------

def calculate_ber(tx_bits: np.ndarray, rx_bits: np.ndarray) -> float:
    """Calculate the Bit Error Rate (BER) between transmitted and received bits.

    Parameters
    ----------
    tx_bits : np.ndarray
        Transmitted bit sequence (0s and 1s).
    rx_bits : np.ndarray
        Received (detected) bit sequence (0s and 1s).  Must have the
        same length as *tx_bits*.

    Returns
    -------
    float
        BER in the range [0.0, 1.0].

    Raises
    ------
    ValueError
        If the two arrays differ in length.
    """
    tx_bits = np.asarray(tx_bits, dtype=np.int8)
    rx_bits = np.asarray(rx_bits, dtype=np.int8)
    if tx_bits.shape != rx_bits.shape:
        raise ValueError(
            f"Bit arrays must have the same shape, "
            f"got {tx_bits.shape} vs {rx_bits.shape}."
        )
    if tx_bits.size == 0:
        return 0.0
    return float(np.mean(tx_bits != rx_bits))


def calculate_capacity(snr_db: float, bandwidth: float = 1.0) -> float:
    """Compute the Shannon channel capacity.

    .. math::
        C = B \\log_2(1 + \\text{SNR}_{\\text{linear}})

    Parameters
    ----------
    snr_db : float
        Signal-to-noise ratio in decibels.
    bandwidth : float
        Channel bandwidth in Hz (default 1 Hz → result in bits/s/Hz).

    Returns
    -------
    float
        Channel capacity in bits/s.
    """
    snr_linear: float = 10.0 ** (snr_db / 10.0)
    return float(bandwidth * np.log2(1.0 + snr_linear))
