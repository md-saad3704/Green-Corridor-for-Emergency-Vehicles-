
from backend.controller.controller_config import (
    AMBULANCE_CONFLICT_SIGNAL_INDICES,
    AMBULANCE_ID,
    AMBULANCE_SIGNAL_INDEX,
)


def evaluate_emergency_green_readiness(
    *,
    ambulance_id,
    ambulance_available,
    telemetry_valid,
    ambulance_signal_index,
    conflict_signal_indices,
    occupied_internal_lanes,
    signal_state,
    expected_signal_length,
    normal_program_active,
    clearance_complete,
):
    """
    Evaluate configured preconditions for further emergency-green review.

    A ready result means only that these configured checks passed.
    It is not a complete proof of junction safety and does not actuate
    traffic signals.
    """
    failures = []

    if ambulance_id != AMBULANCE_ID:
        failures.append("Unexpected ambulance ID.")

    if ambulance_available is not True:
        failures.append("Ambulance is not confirmed available.")

    if telemetry_valid is not True:
        failures.append("Telemetry is not valid.")

    if ambulance_signal_index != AMBULANCE_SIGNAL_INDEX:
        failures.append("Ambulance signal index does not match configuration.")

    if set(conflict_signal_indices) != set(
        AMBULANCE_CONFLICT_SIGNAL_INDICES
    ):
        failures.append("Conflict indices do not match configuration.")

    if occupied_internal_lanes:
        failures.append("Internal junction lanes are occupied.")

    if (
        not isinstance(signal_state, str)
        or len(signal_state) != expected_signal_length
    ):
        failures.append("Signal state is missing or has an invalid length.")

    if normal_program_active is not True:
        failures.append("Normal signal program is not confirmed active.")

    if clearance_complete is not True:
        failures.append("Clearance sequence is not complete.")

    return {
        "ready_for_further_review": not failures,
        "failures": failures,
        "signal_actuation_performed": False,
    }
