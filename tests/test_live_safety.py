
from unittest.mock import Mock

import pytest

from backend.controller.controller_config import (
    AMBULANCE_CONFLICT_SIGNAL_INDICES,
    AMBULANCE_ID,
    AMBULANCE_INTERNAL_LANE,
    AMBULANCE_INCOMING_LANE,
    AMBULANCE_OUTGOING_LANE,
    AMBULANCE_SIGNAL_INDEX,
    TRAFFIC_LIGHT_ID,
)
from backend.controller.live_safety import assess_live_clearance


@pytest.fixture
def live_inputs(monkeypatch):
    connection = Mock()
    trafficlight = connection.trafficlight

    trafficlight.getIDList.return_value = [TRAFFIC_LIGHT_ID]
    trafficlight.getProgram.return_value = "online"
    trafficlight.getRedYellowGreenState.return_value = "r" * 20
    trafficlight.getControlledLinks.return_value = [
        [("incoming", "outgoing", "internal")]
        for _ in range(20)
    ]

    # Provide one movement for every controlled signal index.
    mapping = [
        {
            "signal_index": index,
            "incoming_lane": f"in_{index}",
            "outgoing_lane": f"out_{index}",
            "via_lane": f"via_{index}",
        }
        for index in range(20)
    ]

    # Use the actual configured ambulance movement at index 17.
    mapping[AMBULANCE_SIGNAL_INDEX] = {
        "signal_index": AMBULANCE_SIGNAL_INDEX,
        "incoming_lane": AMBULANCE_INCOMING_LANE,
        "outgoing_lane": AMBULANCE_OUTGOING_LANE,
        "via_lane": AMBULANCE_INTERNAL_LANE,
    }

    monkeypatch.setattr(
        "backend.controller.live_safety.get_signal_link_mapping",
        lambda tls_id, connection=None: mapping,
    )

    # Create symmetric foe relationships for the mock junction.
    foe_map = {index: set() for index in range(20)}
    foe_map[AMBULANCE_SIGNAL_INDEX] = set(
        AMBULANCE_CONFLICT_SIGNAL_INDICES
    )

    for index in AMBULANCE_CONFLICT_SIGNAL_INDICES:
        foe_map[index].add(AMBULANCE_SIGNAL_INDEX)

    requests = {
        index: f"request_{index}"
        for index in range(20)
    }

    monkeypatch.setattr(
        "backend.controller.live_safety.load_junction_requests",
        lambda: requests,
    )

    monkeypatch.setattr(
        "backend.controller.live_safety.decode_foes",
        lambda key: foe_map[int(key.removeprefix("request_"))],
    )

    monkeypatch.setattr(
        "backend.controller.live_safety.get_internal_lane_occupancy",
        lambda connection, internal_lane_ids: {},
    )

    manager = Mock()
    manager.stage = "complete"

    return {
        "connection": connection,
        "internal_lane_ids": [AMBULANCE_INTERNAL_LANE],
        "clearance_manager": manager,
    }


def assess(live_inputs):
    return assess_live_clearance(**live_inputs)


def test_valid_live_conditions_pass(live_inputs):
    result = assess(live_inputs)

    assert result["ready_for_further_review"] is True
    assert result["failures"] == []
    assert result["signal_actuation_performed"] is False


def test_missing_traffic_light_blocks_readiness(live_inputs):
    live_inputs["connection"].trafficlight.getIDList.return_value = []

    result = assess(live_inputs)

    assert result["ready_for_further_review"] is False
    assert result["signal_actuation_performed"] is False


@pytest.mark.parametrize(
    ("program", "state", "stage"),
    [
        ("unexpected", "r" * 20, "complete"),
        ("online", "G" + "r" * 19, "complete"),
        ("online", "r" * 20, "yellow"),
    ],
)
def test_invalid_program_state_or_clearance_blocks_readiness(
    live_inputs, program, state, stage
):
    trafficlight = live_inputs["connection"].trafficlight
    trafficlight.getProgram.return_value = program
    trafficlight.getRedYellowGreenState.return_value = state
    live_inputs["clearance_manager"].stage = stage

    result = assess(live_inputs)

    assert result["ready_for_further_review"] is False
    assert result["failures"]


def test_incorrect_ambulance_mapping_blocks_readiness(
    live_inputs, monkeypatch
):
    monkeypatch.setattr(
        "backend.controller.live_safety.get_signal_link_mapping",
        lambda tls_id, connection=None: [],
    )

    result = assess(live_inputs)

    assert result["ready_for_further_review"] is False
    assert any(
        "ambulance movement" in failure.lower()
        for failure in result["failures"]
    )


def test_conflict_mismatch_blocks_readiness(live_inputs, monkeypatch):
    monkeypatch.setattr(
        "backend.controller.live_safety.decode_foes",
        lambda key: {1, 2},
    )

    result = assess(live_inputs)

    assert result["ready_for_further_review"] is False
    assert any(
        "conflict indices" in failure.lower()
        for failure in result["failures"]
    )


def test_occupied_internal_lane_blocks_readiness(
    live_inputs, monkeypatch
):
    monkeypatch.setattr(
        "backend.controller.live_safety.get_internal_lane_occupancy",
        lambda connection, internal_lane_ids: {
            ":C_16_1": ["car_1"]
        },
    )

    result = assess(live_inputs)

    assert result["ready_for_further_review"] is False
    assert any(
        "occupied" in failure.lower()
        for failure in result["failures"]
    )


def test_assessment_exception_fails_closed(live_inputs, monkeypatch):
    monkeypatch.setattr(
        "backend.controller.live_safety.load_junction_requests",
        Mock(side_effect=RuntimeError("simulated test failure")),
    )

    result = assess(live_inputs)

    assert result["ready_for_further_review"] is False
    assert result["signal_actuation_performed"] is False
    assert any(
        "assessment failed" in failure.lower()
        for failure in result["failures"]
    )
