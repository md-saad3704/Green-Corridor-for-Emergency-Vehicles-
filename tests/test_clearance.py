
import pytest

from backend.controller.clearance import build_clearance_plan
from backend.controller.config import (
    ALL_RED_DURATION_SECONDS,
    YELLOW_DURATION_SECONDS,
)


def test_clearance_plan_converts_green_to_yellow():
    plan = build_clearance_plan("GGggrrrr", 8)

    assert plan["yellow_state"] == "YYyyrrrr"
    assert plan["all_red_state"] == "rrrrrrrr"


def test_clearance_plan_preserves_existing_red_and_yellow():
    plan = build_clearance_plan("GyrR", 4)

    assert plan["yellow_state"] == "YyrR"
    assert plan["all_red_state"] == "rrrr"


def test_clearance_plan_uses_configured_durations():
    plan = build_clearance_plan("Ggrr", 4)

    assert plan["yellow_duration_seconds"] == YELLOW_DURATION_SECONDS
    assert plan["all_red_duration_seconds"] == ALL_RED_DURATION_SECONDS


@pytest.mark.parametrize(
    "signal_state, expected_length",
    [
        ("Ggr", 4),
        ("GGxr", 4),
        ("", 4),
    ],
)
def test_clearance_plan_rejects_invalid_signal_state(
    signal_state,
    expected_length,
):
    with pytest.raises(ValueError):
        build_clearance_plan(signal_state, expected_length)
