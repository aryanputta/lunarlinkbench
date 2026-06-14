import pytest

from lunarlinkbench.analyzer import default_scenarios, run_scenarios
from lunarlinkbench.simulator import simulate_latency
from lunarlinkbench.types import MissionConfig


def _cfg(**kw):
    base = dict(daily_data_mb=50.0, relay_alt_km=100.0, downlink_bps=256_000)
    base.update(kw)
    return MissionConfig(**base)


def test_relay_beats_dte_only_at_tail():
    dte = simulate_latency(_cfg(relay_coverage=0.0), n_samples=5000, seed=7)
    relay = simulate_latency(_cfg(relay_coverage=1.0), n_samples=5000, seed=7)
    # Relay dramatically reduces the P99 tail vs no-relay blackout waits.
    assert relay.p99_h < dte.p99_h
    assert relay.frac_meeting_requirement > dte.frac_meeting_requirement


def test_percentiles_are_ordered():
    r = simulate_latency(_cfg(), n_samples=5000, seed=1)
    assert r.p50_h <= r.p90_h <= r.p99_h <= r.max_h


def test_reproducible_with_seed():
    a = simulate_latency(_cfg(), n_samples=3000, seed=99)
    b = simulate_latency(_cfg(), n_samples=3000, seed=99)
    assert a.p90_h == b.p90_h
    assert a.frac_meeting_requirement == b.frac_meeting_requirement


def test_dte_only_can_exceed_requirement_in_blackout():
    # No relay: worst-case waits run into multi-day blackout, exceeding 48 h.
    r = simulate_latency(_cfg(relay_coverage=0.0), n_samples=5000, seed=3)
    assert r.max_h > 48.0


def test_requirement_fraction_in_unit_interval():
    r = simulate_latency(_cfg(), n_samples=2000, seed=5)
    assert 0.0 <= r.frac_meeting_requirement <= 1.0
    assert r.requirement_ci_low <= r.frac_meeting_requirement


def test_invalid_config_rejected():
    with pytest.raises(ValueError):
        MissionConfig(daily_data_mb=50.0, relay_alt_km=100.0,
                      downlink_bps=256_000, relay_coverage=1.5)


def test_default_scenarios_run():
    results = run_scenarios(default_scenarios(), n_samples=1500, seed=2)
    assert len(results) == 3
    names = [n for n, _ in results]
    assert "DTE only (no relay)" in names
