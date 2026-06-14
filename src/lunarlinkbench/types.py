"""Typed configuration and result records."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MissionConfig:
    """Parameters defining a single mission/link scenario."""

    daily_data_mb: float
    relay_alt_km: float
    downlink_bps: float
    # Relay availability: fraction of the libration blackout covered by a relay.
    # 1.0 = fully relay-covered; 0.0 = DTE only (no relay).
    relay_coverage: float = 1.0
    # Mean number of usable contacts per relay orbital period (>= 1 typical).
    contacts_per_orbit: float = 1.0
    # Probability a scheduled contact is missed (weather, attitude, occlusion).
    missed_contact_prob: float = 0.1
    mission_days: float = 29.5

    def __post_init__(self) -> None:
        if not 0.0 <= self.relay_coverage <= 1.0:
            raise ValueError("relay_coverage must be in [0, 1]")
        if not 0.0 <= self.missed_contact_prob < 1.0:
            raise ValueError("missed_contact_prob must be in [0, 1)")
        if self.daily_data_mb <= 0 or self.downlink_bps <= 0:
            raise ValueError("data volume and link rate must be positive")
        if self.relay_alt_km <= 0:
            raise ValueError("relay_alt_km must be positive")


@dataclass(frozen=True)
class LatencyResult:
    """Percentile summary of a latency Monte Carlo run (hours)."""

    n_samples: int
    p50_h: float
    p90_h: float
    p99_h: float
    mean_h: float
    max_h: float
    requirement_h: float
    frac_meeting_requirement: float
    # Clopper-Pearson style lower bound on the meeting-requirement fraction.
    requirement_ci_low: float = field(default=0.0)
