"""Monte Carlo latency simulator.

For each randomly-timed data-acquisition event over the mission, compute the
end-to-end latency to Earth:

    latency = wait_for_contact + downlink_time + light_time

wait_for_contact depends on whether Earth is visible (DTE) or in blackout
(relay, possibly missed). This turns the proof-of-concept bounding math into a
distribution so we can report P50/P90/P99 and test MR-06.
"""

from __future__ import annotations

import random
from typing import Optional

from .constants import BLACKOUT_DAYS, LUNAR_CYCLE_DAYS, MR06_LATENCY_HOURS
from .geometry import earth_visible, light_time_h
from .orbit import mean_contact_gap_h
from .payload import buffered_volume_mb, downlink_time_h
from .stats import clopper_pearson_low, percentile
from .types import LatencyResult, MissionConfig

# DTE wait when Earth is visible: continuous-to-hourly contact at the pole.
# Modelled as a small uniform wait (terrain/scheduling), hours.
_DTE_MAX_WAIT_H = 3.0


def _blackout_wait_h(cfg: MissionConfig, rng: random.Random) -> float:
    """Wait time for a contact during the libration blackout."""
    if cfg.relay_coverage <= 0.0 or rng.random() > cfg.relay_coverage:
        # No relay coverage for this event: must wait out the blackout.
        # Uniform remaining-blackout assumption.
        return rng.uniform(0.0, BLACKOUT_DAYS * 24.0)
    gap = mean_contact_gap_h(cfg.relay_alt_km, cfg.contacts_per_orbit)
    wait = rng.uniform(0.0, gap)
    # Each scheduled contact can be missed, adding another gap.
    while rng.random() < cfg.missed_contact_prob:
        wait += gap
    return wait


def simulate_latency(
    cfg: MissionConfig,
    n_samples: int = 20_000,
    seed: Optional[int] = 1234,
    requirement_h: float = MR06_LATENCY_HOURS,
) -> LatencyResult:
    """Run the latency Monte Carlo and return a percentile summary."""
    if n_samples <= 0:
        raise ValueError("n_samples must be positive")
    rng = random.Random(seed)
    lt = light_time_h()
    samples: list[float] = []
    meeting = 0

    for _ in range(n_samples):
        t_days = rng.uniform(0.0, cfg.mission_days)
        if earth_visible(t_days, LUNAR_CYCLE_DAYS, BLACKOUT_DAYS):
            wait = rng.uniform(0.0, _DTE_MAX_WAIT_H)
        else:
            wait = _blackout_wait_h(cfg, rng)
        vol = buffered_volume_mb(cfg.daily_data_mb, wait)
        dl = downlink_time_h(vol, cfg.downlink_bps)
        latency = wait + dl + lt
        samples.append(latency)
        if latency <= requirement_h:
            meeting += 1

    frac = meeting / n_samples
    return LatencyResult(
        n_samples=n_samples,
        p50_h=percentile(samples, 50),
        p90_h=percentile(samples, 90),
        p99_h=percentile(samples, 99),
        mean_h=sum(samples) / n_samples,
        max_h=max(samples),
        requirement_h=requirement_h,
        frac_meeting_requirement=frac,
        requirement_ci_low=clopper_pearson_low(meeting, n_samples),
    )
