"""Science-data volume and downlink transmission time."""

from __future__ import annotations


def downlink_time_s(data_mb: float, rate_bps: float) -> float:
    """Time to transmit a data volume (MB) at a link rate (bits/s)."""
    if data_mb < 0:
        raise ValueError("data_mb must be non-negative")
    if rate_bps <= 0:
        raise ValueError("rate_bps must be positive")
    data_bits = data_mb * 8e6
    return data_bits / rate_bps


def downlink_time_h(data_mb: float, rate_bps: float) -> float:
    return downlink_time_s(data_mb, rate_bps) / 3600.0


def buffered_volume_mb(daily_data_mb: float, gap_h: float) -> float:
    """Data accumulated in the buffer over a contact gap of `gap_h` hours."""
    if daily_data_mb < 0 or gap_h < 0:
        raise ValueError("inputs must be non-negative")
    return daily_data_mb * (gap_h / 24.0)
