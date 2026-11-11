import math

import pytest

from week2_assignments.laser_utils import get_front_sector_min_distance


def test_only_front_sector_is_considered():
    result = get_front_sector_min_distance(
        [0.1, 0.8, 0.7, 0.2, 0.1],
        -math.pi / 2.0,
        math.pi / 4.0,
        0.4,
    )
    assert result == pytest.approx(0.7)


def test_no_usable_front_readings_returns_none():
    result = get_front_sector_min_distance(
        [math.nan, -math.inf, math.nan], -0.2, 0.2, 0.3
    )
    assert result is None


def test_positive_infinity_is_a_valid_no_return():
    result = get_front_sector_min_distance(
        [math.inf], 0.0, 0.0, 0.3
    )
    assert math.isinf(result)


def test_out_of_sensor_range_values_are_ignored():
    result = get_front_sector_min_distance(
        [0.05, 1.5, 6.0], -0.1, 0.1, 0.3, 0.1, 5.0
    )
    assert result == pytest.approx(1.5)


def test_invalid_sector_width_is_rejected():
    with pytest.raises(ValueError):
        get_front_sector_min_distance(
            [1.0], 0.0, 0.0, math.pi + 0.1
        )
