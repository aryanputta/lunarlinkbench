# Sources and traceability

## NASA-sourced facts (citable)

| Fact | Value | Source |
|------|-------|--------|
| Earth invisible from south pole (libration) | ~14 days/month | NASA VIPER Lunar Operations |
| DTE baseline link | via Deep Space Network | NASA VIPER Lunar Operations |
| One-way light time | 1.28 s (6-10 s incl. processing) | NASA VIPER / geometry |
| Relay required when no Earth LOS | LCRNS enables comms "even when not in line of sight with Earth" | NASA SCaN LCRNS |
| Without relays, south-pole landing | "significantly limited by a lack of direct communication" | NASA SCaN LCRNS |

- NASA. "VIPER Lunar Operations." https://science.nasa.gov/mission/viper/lunar-operations/
- NASA. "Blazing a Trail to Lunar Relays." https://www.nasa.gov/technology/space-comms/space-communications/blazing-a-trail-to-lunar-relays/

## Standard physical constants

- c = 299,792.458 km/s
- Earth-Moon mean distance = 384,400 km
- Lunar mu = 4902.8 km^3/s^2, R_moon = 1737.4 km

## TBR (Phase A link budget)

- LCRNS relay revisit cadence (orbit period assumed via Kepler III for a low orbiter)
- Daily science-data volume (~50 MB/day estimate)
- Downlink rate (256 kbps conservative)
- MR-06 48 h latency value

## MCR traceability

- Backs Section 1.6 relay/contact-window evaluation criterion.
- Backs Section 1.8 selection of relay-assisted architecture over DTE-only.
- Companion analysis: Brain `misc/writing/nasa-mcr-team15/comms-latency-proof-of-concept.md`.
