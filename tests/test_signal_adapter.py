
from unittest.mock import Mock

import pytest

from backend.controller.signal_adapter import apply_signal_state


@pytest.fixture
def mock_connection():
    connection = Mock()
    connection.trafficlight.getIDList.return_value = ["C"]
    connection.trafficlight.getControlledLinks.return_value = [
        [("lane_in", "lane_out", ":via")]
        for _ in range(20)
    ]
    connection.trafficlight.getRedYellowGreenState.return_value = "r" * 20
    return connection


def test_valid_signal_state_is_applied_and_verified(mock_connection):
    requested_state = "r" * 17 + "G" + "r" * 2
    mock_connection.trafficlight.getRedYellowGreenState.return_value = (
        requested_state
    )

    result = apply_signal_state(
        mock_connection, "C", requested_state
    )

    mock_connection.trafficlight.setRedYellowGreenState.assert_called_once_with(
        "C", requested_state
    )
    assert result == requested_state


def test_unknown_traffic_light_is_rejected(mock_connection):
    with pytest.raises(ValueError, match="was not found"):
        apply_signal_state(mock_connection, "UNKNOWN", "r" * 20)

    mock_connection.trafficlight.setRedYellowGreenState.assert_not_called()


def test_invalid_signal_state_is_rejected_before_application(mock_connection):
    with pytest.raises(ValueError):
        apply_signal_state(mock_connection, "C", "r" * 19 + "x")

    mock_connection.trafficlight.setRedYellowGreenState.assert_not_called()


def test_wrong_signal_state_length_is_rejected(mock_connection):
    with pytest.raises(ValueError, match="length"):
        apply_signal_state(mock_connection, "C", "r" * 19)

    mock_connection.trafficlight.setRedYellowGreenState.assert_not_called()


def test_state_mismatch_after_application_raises_error(mock_connection):
    mock_connection.trafficlight.getRedYellowGreenState.return_value = (
        "r" * 20
    )
    requested_state = "r" * 17 + "G" + "r" * 2

    with pytest.raises(RuntimeError, match="verification failed"):
        apply_signal_state(mock_connection, "C", requested_state)
