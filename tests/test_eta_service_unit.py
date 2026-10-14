import pytest

from backend.eta.service import estimate_ambulance_eta


def test_ambulance_not_available():
    result = estimate_ambulance_eta(None)

    assert result["eta_seconds"] is None
    assert result["status"] == "ambulance_not_available"


def test_distance_unavailable():
    result = estimate_ambulance_eta({
        "distance_to_intersection_m": None,
        "speed_mps": 10.0,
    })

    assert result["eta_seconds"] is None
    assert result["status"] == "distance_unavailable"


def test_valid_ambulance_telemetry():
    result = estimate_ambulance_eta({
        "distance_to_intersection_m": 150.96,
        "speed_mps": 13.56,
    })

    assert result["eta_seconds"] == 11.13
    assert result["status"] == "estimated"
    assert result["distance_m"] == 150.96



import pytest


@pytest.mark.parametrize(
    "distance,speed",
    [
        (float("nan"), 10.0),
        (float("inf"), 10.0),
        (150.96, float("nan")),
        (150.96, float("inf")),
    ],
)
def test_invalid_numeric_telemetry(distance, speed):
    result = estimate_ambulance_eta({
        "distance_to_intersection_m": distance,
        "speed_mps": speed,
    })

    assert result["eta_seconds"] is None



@pytest.mark.parametrize(
    "speed",
    [
        None,
        "invalid",
        float("nan"),
        float("inf"),
    ],
)
def test_speed_unavailable(speed):
    result = estimate_ambulance_eta({
        "distance_to_intersection_m": 150.96,
        "speed_mps": speed,
    })

    assert result["eta_seconds"] is None
    assert result["status"] == "speed_unavailable"


@pytest.mark.parametrize(
    "distance",
    [
        "invalid",
        float("nan"),
        float("inf"),
        -1.0,
    ],
)
def test_invalid_distance_status(distance):
    result = estimate_ambulance_eta({
        "distance_to_intersection_m": distance,
        "speed_mps": 10.0,
    })

    assert result["eta_seconds"] is None
    assert result["status"] == "distance_unavailable"
