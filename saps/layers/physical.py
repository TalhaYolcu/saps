"""
Deep Joint Source-Channel Coding (Deep-JSCC) Physical Layer
=============================================================

Implements a fully-differentiable neural transceiver that maps latent
feature vectors to IQ channel symbols, transmits them through a
(possibly fading) wireless channel, and reconstructs the original
representation at the receiver.

Key components:
  * :class:`DeepJSCCEncoder` — MLP encoder with power normalisation.
  * :class:`DeepJSCCDecoder` — MLP decoder.
  * :class:`DeepJSCCTransceiver` — End-to-end trainable transceiver.
  * :class:`PhysicalLayer` — High-level wrapper used by the SAPS stack.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from saps.channel.fading import AWGNChannel, ChannelModel


# ---------------------------------------------------------------------------
# Encoder
# ---------------------------------------------------------------------------

class DeepJSCCEncoder(nn.Module):
    """Neural encoder: maps a latent feature vector to power-normalised
    IQ channel symbols.

    Architecture::

        Linear(input_dim, hidden_dim) → ReLU
        Linear(hidden_dim, hidden_dim) → ReLU
        Linear(hidden_dim, iq_dim * 2)   # I and Q components
        PowerNorm                         # E[|x|^2] = 1

    Parameters
    ----------
    input_dim : int
        Dimensionality of the input latent vector.
    hidden_dim : int
        Width of the hidden layers.
    iq_dim : int
        Number of complex IQ symbols to produce (output has ``2 * iq_dim``
        real values which are then paired as complex samples).
    """

    def __init__(
        self,
        input_dim: int = 256,
        hidden_dim: int = 128,
        iq_dim: int = 64,
    ) -> None:
        super().__init__()
        self.input_dim: int = input_dim
        self.iq_dim: int = iq_dim

        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, iq_dim * 2),  # I and Q interleaved
        )

    def _power_normalise(self, x: torch.Tensor) -> torch.Tensor:
        """Normalise the batch so that the average symbol power is 1.

        .. math::
            \\hat{x} = \\frac{x}{\\sqrt{\\mathbb{E}[|x|^2]}}

        This is applied **per sample** (i.e. each row is independently
        normalised) to enforce the transmit power constraint.

        Parameters
        ----------
        x : torch.Tensor
            Tensor of shape ``(batch, 2 * iq_dim)`` with interleaved I/Q.

        Returns
        -------
        torch.Tensor
            Power-normalised tensor of the same shape.
        """
        # Reshape to (batch, iq_dim, 2) for convenience
        batch_size = x.shape[0]
        iq = x.view(batch_size, self.iq_dim, 2)
        # Per-sample average power: mean of I^2 + Q^2
        power = torch.mean(iq[:, :, 0] ** 2 + iq[:, :, 1] ** 2, dim=1, keepdim=True)  # (B, 1)
        # Avoid division by zero
        power = torch.clamp(power, min=1e-10)
        scale = torch.sqrt(power).unsqueeze(-1)  # (B, 1, 1)
        iq_normed = iq / scale
        return iq_normed.view(batch_size, self.iq_dim * 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Encode latent vector to power-normalised IQ symbols.

        Parameters
        ----------
        x : torch.Tensor
            Input tensor of shape ``(batch, input_dim)``.

        Returns
        -------
        torch.Tensor
            Complex IQ symbols of shape ``(batch, iq_dim)`` with
            ``dtype=torch.complex64``.
        """
        raw: torch.Tensor = self.net(x)                        # (B, 2*iq_dim)
        normed: torch.Tensor = self._power_normalise(raw)      # (B, 2*iq_dim)
        # Convert interleaved I/Q → complex
        iq = normed.view(-1, self.iq_dim, 2)
        complex_symbols = torch.complex(iq[:, :, 0], iq[:, :, 1])  # (B, iq_dim)
        return complex_symbols


# ---------------------------------------------------------------------------
# Decoder
# ---------------------------------------------------------------------------

class DeepJSCCDecoder(nn.Module):
    """Neural decoder: reconstructs latent features from received
    (noisy) IQ symbols.

    Architecture::

        Linear(iq_dim * 2, hidden_dim) → ReLU
        Linear(hidden_dim, hidden_dim) → ReLU
        Linear(hidden_dim, output_dim)

    Parameters
    ----------
    iq_dim : int
        Number of complex IQ symbols (input has ``2 * iq_dim`` reals).
    hidden_dim : int
        Width of the hidden layers.
    output_dim : int
        Dimensionality of the reconstructed latent vector.
    """

    def __init__(
        self,
        iq_dim: int = 64,
        hidden_dim: int = 128,
        output_dim: int = 256,
    ) -> None:
        super().__init__()
        self.iq_dim: int = iq_dim
        self.output_dim: int = output_dim

        self.net = nn.Sequential(
            nn.Linear(iq_dim * 2, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, y: torch.Tensor) -> torch.Tensor:
        """Decode received IQ symbols back to the latent space.

        Parameters
        ----------
        y : torch.Tensor
            Received complex IQ symbols, shape ``(batch, iq_dim)``
            (``complex64`` or ``complex128``), **or** real-valued tensor
            of shape ``(batch, 2 * iq_dim)`` with interleaved I/Q.

        Returns
        -------
        torch.Tensor
            Reconstructed latent vector of shape ``(batch, output_dim)``.
        """
        if torch.is_complex(y):
            # Split into real / imag and interleave → (B, 2*iq_dim)
            y_real = torch.stack([y.real, y.imag], dim=-1)  # (B, iq_dim, 2)
            y_flat = y_real.reshape(y.shape[0], -1)
        else:
            y_flat = y
        return self.net(y_flat)


# ---------------------------------------------------------------------------
# Transceiver (end-to-end)
# ---------------------------------------------------------------------------

class DeepJSCCTransceiver(nn.Module):
    """Complete Deep-JSCC transceiver for end-to-end learning over
    wireless channels.

    Combines :class:`DeepJSCCEncoder` and :class:`DeepJSCCDecoder` with
    a non-differentiable channel pass in between.  Gradients flow
    through the channel via the *straight-through estimator*: the
    channel is treated as an identity function during back-propagation,
    while the forward pass uses the actual noisy samples.

    Parameters
    ----------
    latent_dim : int
        Dimensionality of the latent vectors at encoder input / decoder
        output.
    hidden_dim : int
        Width of hidden layers in encoder and decoder MLPs.
    iq_dim : int
        Number of complex IQ symbols transmitted per latent vector.
    """

    def __init__(
        self,
        latent_dim: int = 256,
        hidden_dim: int = 128,
        iq_dim: int = 64,
    ) -> None:
        super().__init__()
        self.latent_dim: int = latent_dim
        self.iq_dim: int = iq_dim

        self.encoder = DeepJSCCEncoder(
            input_dim=latent_dim,
            hidden_dim=hidden_dim,
            iq_dim=iq_dim,
        )
        self.decoder = DeepJSCCDecoder(
            iq_dim=iq_dim,
            hidden_dim=hidden_dim,
            output_dim=latent_dim,
        )

    # --------------------------------------------------------------------- #
    #  Channel pass (numpy ↔ torch bridge)                                   #
    # --------------------------------------------------------------------- #

    @staticmethod
    def _torch_to_numpy(symbols: torch.Tensor) -> np.ndarray:
        """Convert a batch of complex torch symbols to a numpy array.

        Parameters
        ----------
        symbols : torch.Tensor
            Complex tensor of shape ``(batch, iq_dim)``.

        Returns
        -------
        np.ndarray
            Complex128 numpy array of the same shape.
        """
        return symbols.detach().cpu().numpy().astype(np.complex128)

    @staticmethod
    def _numpy_to_torch(
        arr: np.ndarray,
        device: torch.device,
    ) -> torch.Tensor:
        """Convert a numpy complex array back to a torch complex tensor.

        Parameters
        ----------
        arr : np.ndarray
            Complex numpy array.
        device : torch.device
            Target device for the returned tensor.

        Returns
        -------
        torch.Tensor
            Complex64 tensor on *device*.
        """
        return torch.from_numpy(arr.astype(np.complex64)).to(device)

    def _pass_through_channel(
        self,
        symbols: torch.Tensor,
        channel: ChannelModel,
        snr_db: float,
    ) -> torch.Tensor:
        """Send symbols through the channel (non-differentiable).

        Each sample in the batch is passed independently through the
        channel.  A straight-through estimator is used so that gradients
        from the decoder can flow back to the encoder.

        Parameters
        ----------
        symbols : torch.Tensor
            Encoded complex IQ symbols ``(batch, iq_dim)``.
        channel : ChannelModel
            A SAPS :class:`~saps.channel.fading.ChannelModel` instance.
        snr_db : float
            Operating SNR in dB.

        Returns
        -------
        torch.Tensor
            Received (noisy) complex symbols ``(batch, iq_dim)``.
        """
        device = symbols.device
        np_symbols = self._torch_to_numpy(symbols)

        # Process each sample in the batch through the channel
        rx_list: list[np.ndarray] = []
        for i in range(np_symbols.shape[0]):
            rx_sample = channel.forward(np_symbols[i], snr_db)
            rx_list.append(rx_sample)
        rx_np = np.stack(rx_list, axis=0)

        rx_torch = self._numpy_to_torch(rx_np, device)

        # Straight-through estimator: attach gradient graph via
        # ``symbols + (rx - symbols).detach()``  ⟹ forward value = rx,
        # backward gradient flows through symbols.
        rx_st = symbols + (rx_torch - symbols).detach()
        return rx_st

    # --------------------------------------------------------------------- #
    #  Forward / training                                                    #
    # --------------------------------------------------------------------- #

    def forward(
        self,
        x: torch.Tensor,
        channel: Optional[ChannelModel] = None,
        snr_db: float = 20.0,
    ) -> torch.Tensor:
        """End-to-end forward pass: encode → channel → decode.

        Parameters
        ----------
        x : torch.Tensor
            Input latent vectors ``(batch, latent_dim)``.
        channel : ChannelModel, optional
            Wireless channel model (defaults to AWGNChannel).
        snr_db : float
            Operating SNR (dB).

        Returns
        -------
        torch.Tensor
            Reconstructed latent vectors ``(batch, latent_dim)``.
        """
        if channel is None:
            channel = AWGNChannel()

        # 1. Encode to complex IQ symbols
        tx_symbols: torch.Tensor = self.encoder(x)         # (B, iq_dim) complex

        # 2. Transmit through the wireless channel
        rx_symbols: torch.Tensor = self._pass_through_channel(
            tx_symbols, channel, snr_db,
        )

        # 3. Decode back to latent space
        x_hat: torch.Tensor = self.decoder(rx_symbols)     # (B, latent_dim)
        return x_hat

    def train_step(
        self,
        x: torch.Tensor,
        channel: ChannelModel,
        snr_db: float,
        optimizer: optim.Optimizer,
    ) -> float:
        """Execute a single training step with MSE loss.

        Parameters
        ----------
        x : torch.Tensor
            Batch of latent vectors ``(batch, latent_dim)``.
        channel : ChannelModel
            Wireless channel model.
        snr_db : float
            Operating SNR (dB) — can be randomised per step for
            SNR-robust training.
        optimizer : torch.optim.Optimizer
            Optimiser instance (e.g. ``Adam``).

        Returns
        -------
        float
            Scalar MSE loss value for this step.
        """
        self.train()
        optimizer.zero_grad()

        x_hat = self.forward(x, channel, snr_db)
        loss: torch.Tensor = nn.functional.mse_loss(x_hat, x)

        loss.backward()
        optimizer.step()

        return float(loss.item())


# ---------------------------------------------------------------------------
# Physical layer wrapper
# ---------------------------------------------------------------------------

class PhysicalLayer:
    """High-level Physical Layer for the SAPS protocol stack.

    Wraps :class:`DeepJSCCTransceiver` and a channel model, exposing
    simple ``transmit`` / ``train`` methods.

    Parameters
    ----------
    config : dict
        Configuration dictionary.  Recognised keys:

        * ``latent_dim``  (int, default 256)
        * ``hidden_dim``  (int, default 128)
        * ``iq_dim``      (int, default 64)
        * ``channel_type`` (str, default ``"awgn"``):
          one of ``"awgn"``, ``"rayleigh"``, ``"rician"``
        * ``channel_params`` (dict, default ``{}``)
        * ``device``      (str, default ``"cpu"``)
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        self.config: Dict[str, Any] = config

        latent_dim: int = config.get("latent_dim", 256)
        hidden_dim: int = config.get("hidden_dim", 128)
        iq_dim: int = config.get("iq_dim", 64)
        device_str: str = config.get("device", "cpu")

        self.device: torch.device = torch.device(device_str)

        # --- Transceiver ---
        self.transceiver = DeepJSCCTransceiver(
            latent_dim=latent_dim,
            hidden_dim=hidden_dim,
            iq_dim=iq_dim,
        ).to(self.device)

        # --- Channel ---
        self.channel: ChannelModel = self._build_channel(
            config.get("channel_type", "awgn"),
            config.get("channel_params", {}),
        )

    @staticmethod
    def _build_channel(
        channel_type: str,
        params: Dict[str, Any],
    ) -> ChannelModel:
        """Instantiate a :class:`ChannelModel` from a string key.

        Parameters
        ----------
        channel_type : str
            ``"awgn"``, ``"rayleigh"``, or ``"rician"``.
        params : dict
            Keyword arguments forwarded to the channel constructor.

        Returns
        -------
        ChannelModel
        """
        from saps.channel.fading import RayleighChannel, RicianChannel

        channel_type = channel_type.lower().strip()
        if channel_type == "awgn":
            return AWGNChannel()
        elif channel_type == "rayleigh":
            return RayleighChannel(**params)
        elif channel_type == "rician":
            return RicianChannel(**params)
        else:
            raise ValueError(f"Unknown channel type: {channel_type!r}")

    def transmit(
        self,
        latent_vector: Union[torch.Tensor, np.ndarray],
        snr_db: float,
    ) -> Union[torch.Tensor, np.ndarray]:
        """Encode a latent vector, transmit through the channel, and decode.

        Parameters
        ----------
        latent_vector : torch.Tensor or np.ndarray
            Input latent vector/batch.
        snr_db : float
            Operating SNR (dB).

        Returns
        -------
        torch.Tensor or np.ndarray
            Reconstructed latent vector in the same type as input.
        """
        self.transceiver.eval()
        was_numpy = isinstance(latent_vector, np.ndarray)
        if was_numpy:
            t_vec = torch.from_numpy(latent_vector.astype(np.float32))
        else:
            t_vec = latent_vector

        if t_vec.dim() == 1:
            t_vec = t_vec.unsqueeze(0)
        t_vec = t_vec.to(self.device)

        with torch.no_grad():
            rec = self.transceiver(t_vec, self.channel, snr_db)

        if was_numpy:
            res = rec.cpu().numpy()
            if latent_vector.ndim == 1:
                res = res.squeeze(0)
            return res
        return rec

    def train(
        self,
        dataset: torch.Tensor,
        epochs: int = 10,
        lr: float = 1e-3,
        batch_size: int = 64,
        snr_range: Tuple[float, float] = (0.0, 20.0),
    ) -> List[float]:
        """Train the Deep-JSCC transceiver end-to-end.

        Parameters
        ----------
        dataset : torch.Tensor
            Training data of shape ``(N, latent_dim)``.
        epochs : int
            Number of training epochs.
        lr : float
            Learning rate.
        batch_size : int
            Mini-batch size.
        snr_range : tuple of float
            ``(min_snr_db, max_snr_db)`` — the SNR is uniformly sampled
            from this range at each step for robustness.

        Returns
        -------
        list of float
            Per-step MSE losses.
        """
        optimizer = optim.Adam(self.transceiver.parameters(), lr=lr)
        dataset = dataset.to(self.device)
        n_samples: int = dataset.shape[0]
        losses: List[float] = []

        for epoch in range(epochs):
            # Shuffle
            perm = torch.randperm(n_samples, device=self.device)
            for start in range(0, n_samples, batch_size):
                end = min(start + batch_size, n_samples)
                batch = dataset[perm[start:end]]
                snr_db = float(
                    np.random.uniform(snr_range[0], snr_range[1])
                )
                loss = self.transceiver.train_step(
                    batch, self.channel, snr_db, optimizer,
                )
                losses.append(loss)

        return losses
