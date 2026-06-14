import math

import pytest

from lunarlinkbench.orbit import (
    mean_contact_gap_h,
    orbital_period_h,
    orbital_period_s,
)


def test_low_orbit_period_matches_hand_calc():
    # 100 km altitude -> ~1.96 h, matches the proof-of-concept derivation.
    assert orbital_period_h(100.0) == pytest.approx(1.96, abs=0.05)


def test_period_increases_with_altitude():
    assert orbital_period_s(50.0) < orbital_period_s(500.0)


def test_contact_gap_scales_with_contacts_per_orbit():
    one = mean_contact_gap_h(100.0, 1.0)
    two = mean_contact_gap_h(100.0, 2.0)
    assert two == pytest.approx(one / 2.0)


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        orbital_period_s(0.0)
    with pytest.raises(ValueError):
        mean_contact_gap_h(100.0, 0.0)
