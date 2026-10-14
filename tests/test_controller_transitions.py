
import pytest

from backend.controller.states import ControllerState as S
from backend.controller.transitions import determine_next_state


def test_ambulance_within_eta_threshold_requests_priority():
    result = determine_next_state(S.NORMAL_FIXED_TIME, True, 10)
    assert result == S.PRIORITY_REQUESTED


def test_ambulance_outside_eta_threshold_keeps_normal_state():
    result = determine_next_state(S.NORMAL_FIXED_TIME, True, 60)
    assert result == S.NORMAL_FIXED_TIME


def test_missing_ambulance_keeps_normal_state():
    result = determine_next_state(S.NORMAL_FIXED_TIME, False, None)
    assert result == S.NORMAL_FIXED_TIME


@pytest.mark.parametrize("eta", [None, -1, float("nan"), float("inf")])
def test_invalid_eta_does_not_request_priority(eta):
    result = determine_next_state(S.NORMAL_FIXED_TIME, True, eta)
    assert result == S.NORMAL_FIXED_TIME


def test_invalid_telemetry_enters_safe_failure():
    result = determine_next_state(
        S.NORMAL_FIXED_TIME, True, 5, telemetry_valid=False
    )
    assert result == S.SAFE_FAILURE


def test_priority_request_enters_clearance():
    result = determine_next_state(S.PRIORITY_REQUESTED, True, 5)
    assert result == S.CLEARANCE


def test_missing_ambulance_during_priority_request_fails_safely():
    result = determine_next_state(S.PRIORITY_REQUESTED, False, 5)
    assert result == S.SAFE_FAILURE


def test_clearance_waits_until_complete():
    result = determine_next_state(S.CLEARANCE, True, 5)
    assert result == S.CLEARANCE


def test_completed_clearance_enables_emergency_green():
    result = determine_next_state(
        S.CLEARANCE, True, 5, clearance_complete=True
    )
    assert result == S.EMERGENCY_GREEN


def test_emergency_green_continues_before_timeout_or_passage():
    result = determine_next_state(S.EMERGENCY_GREEN, True, 5)
    assert result == S.EMERGENCY_GREEN


def test_ambulance_passage_enters_recovery():
    result = determine_next_state(
        S.EMERGENCY_GREEN, True, 5, ambulance_passed=True
    )
    assert result == S.RECOVERY


def test_emergency_green_timeout_enters_passage_verification():
    result = determine_next_state(
        S.EMERGENCY_GREEN, True, 5, emergency_green_timeout=True
    )
    assert result == S.PASSAGE_VERIFICATION


def test_passage_timeout_enters_safe_failure():
    result = determine_next_state(
        S.PASSAGE_VERIFICATION, True, 5, passage_timeout=True
    )
    assert result == S.SAFE_FAILURE


def test_recovery_returns_to_normal_when_complete():
    result = determine_next_state(
        S.RECOVERY, False, None, recovery_complete=True
    )
    assert result == S.NORMAL_FIXED_TIME


def test_safe_failure_is_persistent():
    result = determine_next_state(S.SAFE_FAILURE, False, None)
    assert result == S.SAFE_FAILURE
