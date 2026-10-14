
import pytest

from backend.controller.signal_safety import (
    validate_signal_state,
    validate_no_conflicting_greens,
)


@pytest.mark.parametrize(
    "signal_state",
    ["rrrr", "GGrr", "yyrr", "RRRR", "gGrr"],
)
def test_valid_signal_state_is_accepted(signal_state):
    result, message = validate_signal_state(
        signal_state, len(signal_state)
    )
    assert result is True


def test_signal_state_length_mismatch_is_rejected():
    result, message = validate_signal_state("rrrr", 5)
    assert result is False


@pytest.mark.parametrize(
    "signal_state",
    [None, "", "rrxg", "1234", "rr r"],
)
def test_invalid_signal_state_is_rejected(signal_state):
    result, message = validate_signal_state(signal_state, 4)
    assert result is False


def test_conflicting_green_indices_are_rejected():
    # Indices 0 and 1 are configured as mutually conflicting.
    result, message = validate_no_conflicting_greens(
        "GGrr",
        conflict_groups=[{0, 1}],
    )
    assert result is False
    assert "Conflicting green" in message


def test_non_conflicting_green_indices_are_accepted():
    result, message = validate_no_conflicting_greens(
        "GrrG",
        conflict_groups=[{0, 1}, {2, 3}],
    )
    assert result is True


def test_red_and_yellow_are_not_counted_as_green_conflicts():
    result, message = validate_no_conflicting_greens(
        "yRrr",
        conflict_groups=[{0, 1}],
    )
    assert result is True


def test_invalid_character_is_rejected_by_conflict_validator():
    result, message = validate_no_conflicting_greens(
        "Gxrr",
        conflict_groups=[{0, 1}],
    )
    assert result is False
