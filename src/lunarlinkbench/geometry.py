"""Earth-visibility geometry from the lunar south pole.

NASA fact: from the lunar south pole, Earth is invisible for ~14 days each
~29.5-day month due to libration (NASA VIPER Lunar Operations). We model the
month as two phases: an Earth-visible phase (DTE available) and a blackout
phase (DTE unavailable; relay required).
"""

from __future__ import annotations

from .constants import BLACKOUT_DAYS, EARTH_MOON_KM, C_KM_S, LUNAR_CYCLE_DAYS


def light_time_s(distance_km: float = EARTH_MOON_KM) -> float:
    """One-way Earth-Moon light time, seconds."""
    return distance_km / C_KM_S


def light_time_h(distance_km: float = EARTH_MOON_KM) -> float:
    return light_time_s(distance_km) / 3600.0


def blackout_fraction(blackout_days: float = BLACKOUT_DAYS,
                      cycle_days: float = LUNAR_CYCLE_DAYS) -> float:
    """Fraction of the lunar cycle with no direct Earth line of sight."""
    if cycle_days <= 0:
        raise ValueError("cycle_days must be positive")
    return blackout_days / cycle_days


def earth_visible(t_days: float, cycle_days: float = LUNAR_CYCLE_DAYS,
                  blackout_days: float = BLACKOUT_DAYS) -> bool:
    """Whether Earth is in view at mission time t_days.

    Phase convention: the first (cycle - blackout) days are Earth-visible, the
    final `blackout_days` of each cycle are blackout.
    """
    phase = t_days % cycle_days
    visible_days = cycle_days - blackout_days
    return phase < visible_days
