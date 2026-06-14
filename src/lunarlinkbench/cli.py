"""Command-line interface."""

from __future__ import annotations

import argparse

from .analyzer import default_scenarios, format_report, run_scenarios
from .constants import (
    DEFAULT_DAILY_DATA_MB,
    DEFAULT_DOWNLINK_BPS,
    DEFAULT_RELAY_ALT_KM,
    MR06_LATENCY_HOURS,
)
from .orbit import orbital_period_h
from .simulator import simulate_latency
from .types import MissionConfig


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="lunarlinkbench",
        description="Latency benchmark for lunar south-pole DTE + relay links.",
    )
    sub = parser.add_subparsers(dest="cmd")

    p_bench = sub.add_parser("bench", help="Run the default 3-scenario sweep.")
    p_bench.add_argument("--samples", type=int, default=20_000)
    p_bench.add_argument("--seed", type=int, default=1234)

    p_one = sub.add_parser("run", help="Run a single custom scenario.")
    p_one.add_argument("--daily-mb", type=float, default=DEFAULT_DAILY_DATA_MB)
    p_one.add_argument("--relay-alt-km", type=float, default=DEFAULT_RELAY_ALT_KM)
    p_one.add_argument("--downlink-bps", type=float, default=DEFAULT_DOWNLINK_BPS)
    p_one.add_argument("--relay-coverage", type=float, default=1.0)
    p_one.add_argument("--samples", type=int, default=20_000)
    p_one.add_argument("--seed", type=int, default=1234)
    p_one.add_argument("--requirement-h", type=float, default=MR06_LATENCY_HOURS)

    args = parser.parse_args(argv)

    if args.cmd == "run":
        cfg = MissionConfig(
            daily_data_mb=args.daily_mb,
            relay_alt_km=args.relay_alt_km,
            downlink_bps=args.downlink_bps,
            relay_coverage=args.relay_coverage,
        )
        r = simulate_latency(cfg, n_samples=args.samples, seed=args.seed,
                             requirement_h=args.requirement_h)
        print(f"relay orbital period : {orbital_period_h(args.relay_alt_km):.2f} h")
        print(f"P50 / P90 / P99      : {r.p50_h:.1f} / {r.p90_h:.1f} / {r.p99_h:.1f} h")
        print(f"max latency          : {r.max_h:.1f} h")
        print(f"meets <= {r.requirement_h:.0f} h     : {100*r.frac_meeting_requirement:.1f}% "
              f"(CI low {100*r.requirement_ci_low:.1f}%)")
        return 0

    # default: bench
    samples = getattr(args, "samples", 20_000)
    seed = getattr(args, "seed", 1234)
    results = run_scenarios(default_scenarios(), n_samples=samples, seed=seed)
    print(format_report(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
