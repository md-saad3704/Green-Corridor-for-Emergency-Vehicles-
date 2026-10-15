
from backend.controller.signal_safety import validate_signal_state


AMBULANCE_SIGNAL_INDEX = 17


def build_emergency_signal_state(
    current_signal_state: str,
    ambulance_signal_index: int = AMBULANCE_SIGNAL_INDEX,
) -> str:
    """
    Build a candidate signal state for the ambulance movement.

    Only the ambulance movement receives green. All other controlled
    links are red. This function does not apply the state to SUMO or
    establish that the junction is safe to enter.
    """
    if not isinstance(current_signal_state, str):
        raise ValueError("Current signal state must be a string.")

    expected_length = len(current_signal_state)
    valid, message = validate_signal_state(
        current_signal_state,
        expected_length,
    )
    if not valid:
        raise ValueError(message)

    if (
        isinstance(ambulance_signal_index, bool)
        or not isinstance(ambulance_signal_index, int)
        or not 0 <= ambulance_signal_index < expected_length
    ):
        raise ValueError("Ambulance signal index is out of range.")

    state = ["r"] * expected_length
    state[ambulance_signal_index] = "G"
    return "".join(state)
