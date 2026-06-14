import pytest

from lunarlinkbench.stats import clopper_pearson_low, percentile


def test_percentile_basic():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert percentile(data, 50) == pytest.approx(5.5)
    assert percentile(data, 0) == 1
    assert percentile(data, 100) == 10


def test_percentile_single_element():
    assert percentile([42.0], 90) == 42.0


def test_percentile_invalid():
    with pytest.raises(ValueError):
        percentile([], 50)
    with pytest.raises(ValueError):
        percentile([1, 2], 101)


def test_clopper_pearson_bounds():
    # All successes -> lower bound below 1 but high.
    low = clopper_pearson_low(100, 100)
    assert 0.95 < low < 1.0
    # Half successes -> lower bound below 0.5.
    low2 = clopper_pearson_low(50, 100)
    assert 0.35 < low2 < 0.5


def test_clopper_pearson_zero_successes():
    assert clopper_pearson_low(0, 100) == 0.0


def test_clopper_pearson_invalid():
    with pytest.raises(ValueError):
        clopper_pearson_low(5, 0)
    with pytest.raises(ValueError):
        clopper_pearson_low(101, 100)
