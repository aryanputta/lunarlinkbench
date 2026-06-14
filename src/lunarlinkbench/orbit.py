"""Relay orbital mechanics and contact-cadence model."""

from __future__ import annotations

import math

from .constants import MU_MOON, R_MOON_KM


def orbital_period_s(altitude_km: float) -> float:
    """Circular orbital period of a relay at the given altitude (Kepler III).

    T = 2*pi*sqrt(a^3 / mu), with a = R_moon + altitude.
    """
    if altitude_km <= 0:
        raise ValueError("altitude_km must be positive")
    a = R_MOON_KM + altitude_km
    return 2 * math.pi * math.sqrt(a**3 / MU_MOON)


def orbital_period_h(altitude_km: float) -> float:
    """Orbital period in hours."""
    return orbital_period_s(altitude_km) / 3600.0


def mean_contact_gap_h(altitude_km: float, contacts_per_orbit: float) -> float:
    """Mean time between usable relay contacts, hours.

    contacts_per_orbit >= 1 means at least one usable pass each orbit.
    """
    if contacts_per_orbit <= 0:
        raise ValueError("contacts_per_orbit must be positive")
    return orbital_period_h(altitude_km) / contacts_per_orbit
