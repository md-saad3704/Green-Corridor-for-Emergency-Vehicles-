
import pytest

from backend.eta.baseline import estimate_eta


def test_moving_ambulance_eta():
    assert estimate_eta(150.96, 13.56) == 11.13


def test_slow_ambulance_eta():
    assert estimate_eta(150.96, 2.0) == 75.48


def test_stopped_ambulance_uses_minimum_speed():
    assert estimate_eta(150.96, 0.0) == 150.96


def test_ambulance_at_intersection():
    assert estimate_eta(0.0, 10.0) == 0.0


def test_missing_distance_returns_none():
    assert estimate_eta(None, 10.0) is None


@pytest.mark.parametrize(
    "distance",
    [-1.0, -100.0],
)
def test_negative_distance_returns_none(distance):
    assert estimate_eta(distance, 10.0) is None



@pytest.mark.parametrize(
    "speed",
    [-1.0, -10.0],
)
def test_negative_speed_uses_minimum_speed(speed):
    assert estimate_eta(150.96, speed) == 150.96


@pytest.mark.parametrize(
    "distance,speed",
    [
        (float("nan"), 10.0),
        (float("inf"), 10.0),
        (150.96, float("nan")),
        (150.96, float("inf")),
    ],
)
def test_non_finite_inputs_are_handled(distance, speed):
    result = estimate_eta(distance, speed)
    assert result is None
