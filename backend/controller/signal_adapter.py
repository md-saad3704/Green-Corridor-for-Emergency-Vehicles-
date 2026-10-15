
from backend.controller.signal_safety import validate_signal_state


def apply_signal_state(
    connection,
    tls_id: str,
    signal_state: str,
) -> str:
    """
    Apply and verify a structurally valid state through a TraCI connection.

    This function does not establish junction-level traffic safety
    or manage yellow/all-red clearance timing.
    """
    if not isinstance(tls_id, str) or not tls_id.strip():
        raise ValueError("Traffic light ID must be a non-empty string.")

    trafficlight = connection.trafficlight

    if tls_id not in trafficlight.getIDList():
        raise ValueError(f"Traffic light {tls_id!r} was not found.")

    expected_length = len(trafficlight.getControlledLinks(tls_id))

    valid, message = validate_signal_state(signal_state, expected_length)
    if not valid:
        raise ValueError(message)

    trafficlight.setRedYellowGreenState(tls_id, signal_state)
    actual_state = trafficlight.getRedYellowGreenState(tls_id)

    if actual_state != signal_state:
        raise RuntimeError(
            f"Signal-state verification failed for {tls_id!r}: "
            f"requested {signal_state!r}, received {actual_state!r}."
        )

    return actual_state
