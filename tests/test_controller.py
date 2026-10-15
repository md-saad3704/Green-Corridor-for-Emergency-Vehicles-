
import pytest

from backend.controller.controller import EmergencyVehicleController
from backend.controller.controller_config import PRIORITY_ETA_THRESHOLD
from backend.controller.states import ControllerState


def test_controller_initializes_in_normal_state():
    controller = EmergencyVehicleController()

    assert controller.state == ControllerState.NORMAL_FIXED_TIME


def test_ambulance_within_eta_threshold_requests_priority():
    controller = EmergencyVehicleController()

    result = controller.evaluate_priority_request(
        ambulance_available=True,
        eta_seconds=PRIORITY_ETA_THRESHOLD,
    )

    assert result == ControllerState.PRIORITY_REQUESTED


def test_ambulance_outside_eta_threshold_does_not_request_priority():
    controller = EmergencyVehicleController()

    result = controller.evaluate_priority_request(
        ambulance_available=True,
        eta_seconds=PRIORITY_ETA_THRESHOLD + 1,
    )

    assert result == ControllerState.NORMAL_FIXED_TIME


def test_missing_ambulance_does_not_request_priority():
    controller = EmergencyVehicleController()

    result = controller.evaluate_priority_request(
        ambulance_available=False,
        eta_seconds=5.0,
    )

    assert result == ControllerState.NORMAL_FIXED_TIME


def test_invalid_telemetry_enters_safe_failure():
    controller = EmergencyVehicleController()

    result = controller.evaluate_priority_request(
        ambulance_available=True,
        eta_seconds=5.0,
        telemetry_valid=False,
    )

    assert result == ControllerState.SAFE_FAILURE


@pytest.mark.parametrize("eta", [-1, float("nan"), float("inf"), True, "5"])
def test_invalid_eta_enters_safe_failure(eta):
    controller = EmergencyVehicleController()

    result = controller.evaluate_priority_request(
        ambulance_available=True,
        eta_seconds=eta,
    )

    assert result == ControllerState.SAFE_FAILURE


def test_priority_request_does_not_overwrite_existing_state():
    controller = EmergencyVehicleController()
    controller.state = ControllerState.CLEARANCE

    result = controller.evaluate_priority_request(
        ambulance_available=True,
        eta_seconds=5.0,
    )

    assert result == ControllerState.CLEARANCE



@pytest.mark.parametrize("value", [1, 0, "true", "false", None])
def test_invalid_ambulance_availability_enters_safe_failure(value):
    controller = EmergencyVehicleController()

    result = controller.evaluate_priority_request(
        ambulance_available=value,
        eta_seconds=5.0,
    )

    assert result == ControllerState.SAFE_FAILURE


@pytest.mark.parametrize("value", [1, 0, "true", "false", None])
def test_invalid_telemetry_flag_enters_safe_failure(value):
    controller = EmergencyVehicleController()

    result = controller.evaluate_priority_request(
        ambulance_available=True,
        eta_seconds=5.0,
        telemetry_valid=value,
    )

    assert result == ControllerState.SAFE_FAILURE
