"""Scenario sweep and human-readable reporting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .constants import (
    DEFAULT_DAILY_DATA_MB,
    DEFAULT_DOWNLINK_BPS,
    DEFAULT_RELAY_ALT_KM,
)
from .simulator import simulate_latency
from .types import LatencyResult, MissionConfig


@dataclass(frozen=True)
class Scenario:
    name: str
    config: MissionConfig


def default_scenarios() -> list[Scenario]:
    """The three architectures Team 15 compares for MR-06."""
    base = dict(
        daily_data_mb=DEFAULT_DAILY_DATA_MB,
        relay_alt_km=DEFAULT_RELAY_ALT_KM,
        downlink_bps=DEFAULT_DOWNLINK_BPS,
    )
    return [
        Scenario(
            "DTE only (no relay)",
            MissionConfig(**base, relay_coverage=0.0),
        ),
        Scenario(
            "Relay-assisted (nominal)",
            MissionConfig(**base, relay_coverage=1.0, contacts_per_orbit=1.0,
                          missed_contact_prob=0.1),
        ),
        Scenario(
            "Relay-assisted (degraded)",
            MissionConfig(**base, relay_coverage=0.7, contacts_per_orbit=1.0,
                          missed_contact_prob=0.25),
        ),
    ]


def run_scenarios(scenarios: Iterable[Scenario], n_samples: int = 20_000,
                  seed: int = 1234) -> list[tuple[str, LatencyResult]]:
    return [(s.name, simulate_latency(s.config, n_samples=n_samples, seed=seed))
            for s in scenarios]


def format_report(results: list[tuple[str, LatencyResult]]) -> str:
    lines = []
    lines.append("=" * 78)
    lines.append("LunarLinkBench - science-data latency under DTE + relay contact windows")
    lines.append("=" * 78)
    header = f"{'Scenario':<28}{'P50':>7}{'P90':>8}{'P99':>9}{'max':>9}{'<=req':>9}{'CI_low':>9}"
    lines.append(header)
    lines.append("-" * 78)
    for name, r in results:
        lines.append(
            f"{name:<28}"
            f"{r.p50_h:>6.1f}h"
            f"{r.p90_h:>7.1f}h"
            f"{r.p99_h:>8.1f}h"
            f"{r.max_h:>8.1f}h"
            f"{100*r.frac_meeting_requirement:>7.1f}%"
            f"{100*r.requirement_ci_low:>8.1f}%"
        )
    lines.append("-" * 78)
    req = results[0][1].requirement_h if results else 0.0
    lines.append(f"Requirement under test (MR-06): latency <= {req:.0f} h (TBR)")
    lines.append("Sources: NASA VIPER Lunar Operations; NASA SCaN LCRNS.")
    return "\n".join(lines)
