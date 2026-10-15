
import pytest

from backend.controller.emergency_signal import (
    AMBULANCE_SIGNAL_INDEX,
    build_emergency_signal_state,
)


def test_only_ambulance_movement_receives_green():
    current_state = "GGGggrrrrrGGGggrrrrr"

    result = build_emergency_signal_state(current_state)

    assert len(result) == len(current_state)
    assert result[AMBULANCE_SIGNAL_INDEX] == "G"
    assert result.count("G") == 1
    assert result.count("g") == 0
    assert all(
        character == "r"
        for index, character in enumerate(result)
        if index != AMBULANCE_SIGNAL_INDEX
    )


@pytest.mark.parametrize("index", [-1, 20, True, 1.5])
def test_invalid_ambulance_signal_index_is_rejected(index):
    with pytest.raises(ValueError):
        build_emergency_signal_state("r" * 20, index)


@pytest.mark.parametrize("state", ["", "rrxr", None, 123])
def test_invalid_current_signal_state_is_rejected(state):
    with pytest.raises(ValueError):
        build_emergency_signal_state(state)
