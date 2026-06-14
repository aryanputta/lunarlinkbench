# LunarLinkBench

Science-data latency characterization for a lunar south-pole / permanently
shadowed region (PSR) mission under direct-to-Earth (DTE) and relay-assisted
contact windows. Built for NASA L'SPACE Team 15 MCR to turn the **MR-06**
downlink-latency requirement from a guessed number into a measured, reproducible
benchmark.

## The problem

A PSR surface asset cannot rely on continuous DTE: from the lunar south pole,
Earth is out of view for ~14 days each ~29.5-day month due to libration
(NASA VIPER Lunar Operations), and a relay (NASA LCRNS) is required when there
is no line of sight to Earth. The science payload (dust, thermal at +/-2 K,
radiation dosimeter) is low-rate, so end-to-end latency is set by **contact
cadence, not bandwidth**. LunarLinkBench models this and reports percentile
latency so the 48 h requirement can be tested under different relay assumptions.

## Model

```
latency = wait_for_contact + downlink_time + light_time
```

- **light_time**: 384,400 km / c = 1.28 s one-way (fixed, negligible).
- **downlink_time**: buffered volume / link rate (minutes for a day of data).
- **wait_for_contact**: DTE (small wait when Earth visible) or, during blackout,
  relay revisit (orbital period via Kepler III) with a missed-contact model;
  if no relay coverage, the asset waits out the multi-day blackout.

Monte Carlo over randomly-timed acquisition events across the 29.5-day mission
yields P50/P90/P99/max plus a Clopper-Pearson lower bound on the fraction of
events meeting MR-06.

## Install

```bash
pip install -e .
```

## Run

```bash
# Default 3-scenario sweep (DTE-only vs relay nominal vs relay degraded)
lunarlinkbench bench --samples 20000

# Single custom scenario
lunarlinkbench run --relay-coverage 1.0 --downlink-bps 256000 --requirement-h 48
```

## Representative result (seed 1234)

| Scenario | P50 | P90 | P99 | max | meets <=48h |
|----------|-----|-----|-----|-----|-------------|
| DTE only (no relay) | 2.9 h | 270 h | 335 h | 342 h | 59.1% |
| Relay-assisted (nominal) | 1.3 h | 2.7 h | 3.8 h | 7.7 h | 100.0% |
| Relay-assisted (degraded) | 1.7 h | 98 h | 319 h | 341 h | 87.9% |

**Conclusion:** DTE-only fails MR-06 (the 14-day blackout dominates the tail);
a relay is required to meet the latency requirement. This is the quantitative
backing for the Section 1.6 relay/contact-window evaluation criterion and the
Section 1.8 selection of a relay-assisted architecture.

## What is sourced vs TBR

- **NASA-sourced:** 14-day blackout, DTE-via-DSN baseline, relay necessity,
  light time. See `docs/sources.md`.
- **TBR (Phase A link budget):** real LCRNS relay revisit cadence, daily data
  volume, and link rate. These are the tunable inputs; the benchmark shows the
  latency is robust to them only when relay coverage is high.

## Layout

```
src/lunarlinkbench/
  constants.py   NASA-sourced facts + mission assumptions (TBR tagged)
  geometry.py    Earth-visibility / libration blackout + light time
  orbit.py       relay orbital period + contact gap (Kepler III)
  payload.py     data volume + downlink transmission time
  stats.py       percentiles + Clopper-Pearson CI
  simulator.py   Monte Carlo latency
  analyzer.py    scenario sweep + report
  cli.py         command-line interface
tests/           26 tests mirroring each module
```

## Tests

```bash
python3 -m pytest -q   # 26 passing
```

## Sources

- NASA. "VIPER Lunar Operations." NASA Science. https://science.nasa.gov/mission/viper/lunar-operations/
- NASA. "Blazing a Trail to Lunar Relays." NASA SCaN. https://www.nasa.gov/technology/space-comms/space-communications/blazing-a-trail-to-lunar-relays/
