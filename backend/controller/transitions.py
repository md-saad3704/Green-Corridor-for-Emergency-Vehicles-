
from backend.controller.states import ControllerState
from backend.controller.config import PRIORITY_ETA_THRESHOLD_SECONDS


def determine_next_state(
    current_state,
    ambulance_available,
    eta_seconds,
    telemetry_valid=True,
    ambulance_passed=False,
    clearance_complete=False,
    emergency_green_timeout=False,
    passage_timeout=False,
    recovery_complete=False,
):
    """Determine the next state of the ambulance priority controller."""

    # Invalid or stale telemetry must never initiate priority.
    if not telemetry_valid:
        return ControllerState.SAFE_FAILURE

    if current_state == ControllerState.NORMAL_FIXED_TIME:
        if (
            ambulance_available
            and eta_seconds is not None
            and 0 <= eta_seconds <= PRIORITY_ETA_THRESHOLD_SECONDS
        ):
            return ControllerState.PRIORITY_REQUESTED

        return ControllerState.NORMAL_FIXED_TIME

    if current_state == ControllerState.PRIORITY_REQUESTED:
        if not ambulance_available:
            return ControllerState.SAFE_FAILURE

        return ControllerState.CLEARANCE

    if current_state == ControllerState.CLEARANCE:
        if clearance_complete:
            return ControllerState.EMERGENCY_GREEN

        return ControllerState.CLEARANCE

    if current_state == ControllerState.EMERGENCY_GREEN:
        if ambulance_passed:
            return ControllerState.RECOVERY

        if emergency_green_timeout:
            return ControllerState.PASSAGE_VERIFICATION

        return ControllerState.EMERGENCY_GREEN

    if current_state == ControllerState.PASSAGE_VERIFICATION:
        if ambulance_passed:
            return ControllerState.RECOVERY

        if passage_timeout:
            return ControllerState.SAFE_FAILURE

        return ControllerState.PASSAGE_VERIFICATION

    if current_state == ControllerState.RECOVERY:
        if recovery_complete:
            return ControllerState.NORMAL_FIXED_TIME

        return ControllerState.RECOVERY

    if current_state == ControllerState.SAFE_FAILURE:
        return ControllerState.SAFE_FAILURE

    return ControllerState.SAFE_FAILURE
