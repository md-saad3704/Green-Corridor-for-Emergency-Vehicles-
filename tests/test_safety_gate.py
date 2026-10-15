
import pytest

from backend.controller.controller_config import (
    AMBULANCE_CONFLICT_SIGNAL_INDICES,
    AMBULANCE_ID,
    AMBULANCE_SIGNAL_INDEX,
)
from backend.controller.safety_gate import (
    evaluate_emergency_green_readiness,
)


@pytest.fixture
def valid_inputs():
    return {
        "ambulance_id": AMBULANCE_ID,
        "ambulance_available": True,
        "telemetry_valid": True,
        "ambulance_signal_index": AMBULANCE_SIGNAL_INDEX,
        "conflict_signal_indices": AMBULANCE_CONFLICT_SIGNAL_INDICES,
        "occupied_internal_lanes": {},
        "signal_state": "r" * 20,
        "expected_signal_length": 20,
        "normal_program_active": True,
        "clearance_complete": True,
    }


def test_valid_configured_checks_pass(valid_inputs):
    result = evaluate_emergency_green_readiness(**valid_inputs)

    assert result["ready_for_further_review"] is True
    assert result["failures"] == []
    assert result["signal_actuation_performed"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("ambulance_available", False),
        ("telemetry_valid", False),
        ("normal_program_active", False),
        ("clearance_complete", False),
        ("ambulance_signal_index", 16),
        ("occupied_internal_lanes", {":C_16_1": ["car_1"]}),
    ],
)
def test_failed_precondition_blocks_readiness(valid_inputs, field, value):
    valid_inputs[field] = value

    result = evaluate_emergency_green_readiness(**valid_inputs)

    assert result["ready_for_further_review"] is False
    assert result["failures"]


def test_conflict_indices_must_match_configuration(valid_inputs):
    valid_inputs["conflict_signal_indices"] = {1, 2}

    result = evaluate_emergency_green_readiness(**valid_inputs)

    assert result["ready_for_further_review"] is False


def test_invalid_signal_state_length_blocks_readiness(valid_inputs):
    valid_inputs["signal_state"] = "rrrr"

    result = evaluate_emergency_green_readiness(**valid_inputs)

    assert result["ready_for_further_review"] is False
