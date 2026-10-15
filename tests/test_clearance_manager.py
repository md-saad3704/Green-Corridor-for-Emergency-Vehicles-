
import pytest

from backend.controller.clearance_manager import ClearanceManager
from backend.controller.config import (
    ALL_RED_DURATION_SECONDS,
    YELLOW_DURATION_SECONDS,
)


def test_start_begins_yellow_stage():
    manager = ClearanceManager()

    state = manager.start("GGrr", 4, 0)

    assert manager.stage == "yellow"
    assert state == "YYrr"


def test_yellow_stage_waits_for_configured_duration():
    manager = ClearanceManager()
    manager.start("GGrr", 4, 0)

    manager.update(YELLOW_DURATION_SECONDS - 0.1)
    assert manager.stage == "yellow"

    manager.update(YELLOW_DURATION_SECONDS)
    assert manager.stage == "all_red"


def test_all_red_stage_waits_for_configured_duration():
    manager = ClearanceManager()
    manager.start("GGrr", 4, 0)
    manager.update(YELLOW_DURATION_SECONDS)

    manager.update(
        YELLOW_DURATION_SECONDS + ALL_RED_DURATION_SECONDS - 0.1
    )
    assert manager.stage == "all_red"

    manager.update(
        YELLOW_DURATION_SECONDS + ALL_RED_DURATION_SECONDS
    )
    assert manager.stage == "complete"


def test_cannot_start_while_clearance_is_active():
    manager = ClearanceManager()
    manager.start("GGrr", 4, 0)

    with pytest.raises(RuntimeError):
        manager.start("rrrr", 4, 1)


@pytest.mark.parametrize("invalid_time", [-1, float("nan"), float("inf"), True])
def test_start_rejects_invalid_simulation_time(invalid_time):
    manager = ClearanceManager()

    with pytest.raises(ValueError):
        manager.start("GGrr", 4, invalid_time)


def test_update_rejects_backward_simulation_time():
    manager = ClearanceManager()
    manager.start("GGrr", 4, 10)

    with pytest.raises(ValueError):
        manager.update(9)


def test_delayed_update_preserves_full_all_red_duration():
    manager = ClearanceManager()
    manager.start("GGrr", 4, 0)

    # The update arrives late, at simulation time 5.
    manager.update(YELLOW_DURATION_SECONDS + 2)
    assert manager.stage == "all_red"

    # All-red must remain active for its full duration after transition.
    manager.update(5.9)
    assert manager.stage == "all_red"

    manager.update(6.0)
    assert manager.stage == "complete"
