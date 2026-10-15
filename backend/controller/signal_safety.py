
VALID_SIGNAL_CHARACTERS = {"r", "R", "y", "Y", "g", "G"}


def validate_signal_state(signal_state, expected_length):
    """Validate basic structure of a SUMO signal-state string."""

    if not isinstance(signal_state, str):
        return False, "Signal state must be a string."

    if len(signal_state) != expected_length:
        return False, "Signal-state length does not match controlled links."

    if any(character not in VALID_SIGNAL_CHARACTERS
           for character in signal_state):
        return False, "Signal state contains an unsupported character."

    return True, "Signal-state structure is valid."



def validate_no_conflicting_greens(signal_state, conflict_groups):
    """
    Reject signal states that activate conflicting green signal groups.

    Each conflict group contains signal-state indices that must not
    display green simultaneously. Every index must be an integer
    within the signal-state string.
    """
    if not isinstance(signal_state, str):
        return False, "Signal state must be a string."

    if any(
        character not in VALID_SIGNAL_CHARACTERS
        for character in signal_state
    ):
        return False, "Signal state contains an unsupported character."

    for group in conflict_groups:
        for index in group:
            if (
                not isinstance(index, int)
                or isinstance(index, bool)
                or index < 0
                or index >= len(signal_state)
            ):
                return False, (
                    f"Invalid conflict index {index!r}; "
                    f"valid indices are 0 to {len(signal_state) - 1}."
                )

        green_indices = [
            index
            for index in group
            if signal_state[index] in {"g", "G"}
        ]

        if len(green_indices) > 1:
            return False, (
                f"Conflicting green indications at indices {green_indices}."
            )

    return True, "No configured green conflicts detected."
