import pytest

from lunarlinkbench.payload import (
    buffered_volume_mb,
    downlink_time_h,
    downlink_time_s,
)


def test_downlink_50mb_256kbps_about_26min():
    t = downlink_time_s(50.0, 256_000)
    assert t == pytest.approx(1562.5, rel=1e-6)
    assert downlink_time_h(50.0, 256_000) == pytest.approx(1562.5 / 3600.0, rel=1e-9)


def test_downlink_faster_link_is_shorter():
    assert downlink_time_s(50.0, 1_000_000) < downlink_time_s(50.0, 256_000)


def test_buffer_accumulates_over_gap():
    # One full day gap buffers a full day's data.
    assert buffered_volume_mb(50.0, 24.0) == pytest.approx(50.0)
    assert buffered_volume_mb(50.0, 12.0) == pytest.approx(25.0)


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        downlink_time_s(50.0, 0.0)
    with pytest.raises(ValueError):
        buffered_volume_mb(-1.0, 5.0)
