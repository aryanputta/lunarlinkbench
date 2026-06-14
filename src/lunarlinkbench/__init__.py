"""LunarLinkBench - science-data latency characterization for a lunar south-pole
/ PSR mission under direct-to-Earth and relay-assisted contact windows."""

from .types import LatencyResult, MissionConfig
from .simulator import simulate_latency
from .analyzer import Scenario, default_scenarios, run_scenarios, format_report

__version__ = "0.1.0"

__all__ = [
    "LatencyResult",
    "MissionConfig",
    "simulate_latency",
    "Scenario",
    "default_scenarios",
    "run_scenarios",
    "format_report",
]
