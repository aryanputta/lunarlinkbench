import pytest

from lunarlinkbench.geometry import (
    blackout_fraction,
    earth_visible,
    light_time_h,
    light_time_s,
)


def test_light_time_one_way():
    # 384,400 km / c ~= 1.28 s
    assert light_time_s() == pytest.approx(1.282, abs=0.01)
    assert light_time_h() == pytest.approx(light_time_s() / 3600.0, rel=1e-9)


def test_blackout_fraction_about_half():
    # 14 of 29.5 days ~= 0.475
    assert blackout_fraction() == pytest.approx(14.0 / 29.5, rel=1e-9)


def test_earth_visible_phase_split():
    # First 15.5 days visible, last 14 days blackout.
    assert earth_visible(0.0) is True
    assert earth_visible(15.0) is True
    assert earth_visible(16.0) is False
    assert earth_visible(29.0) is False


def test_earth_visible_is_periodic():
    assert earth_visible(1.0) == earth_visible(1.0 + 29.5)


def test_blackout_fraction_invalid():
    with pytest.raises(ValueError):
        blackout_fraction(14.0, 0.0)
