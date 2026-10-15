from backend.controller.config import (
    ALL_RED_DURATION_SECONDS,
    YELLOW_DURATION_SECONDS,
)
from backend.controller.signal_safety import validate_signal_state


def build_clearance_plan(current_signal_state, expected_length):
    """
    Build a yellow-to-all-red clearance plan without applying it to SUMO.

    Green indications become yellow while existing red and yellow
    indications are preserved. The second state sets every link to red.

    This function plans signal states only. It does not determine whether
    the resulting sequence is safe for a particular junction.
    """
    valid, message = validate_signal_state(
        current_signal_state,
        expected_length,
    )

    if not valid:
        raise ValueError(message)

    yellow_state = "".join(
        "Y" if character == "G" else "y" if character == "g" else character
        for character in current_signal_state
    )

    all_red_state = "r" * expected_length

    return {
        "yellow_state": yellow_state,
        "yellow_duration_seconds": YELLOW_DURATION_SECONDS,
        "all_red_state": all_red_state,
        "all_red_duration_seconds": ALL_RED_DURATION_SECONDS,
    }
