
from unittest.mock import Mock

from backend.controller.clearance_manager import ClearanceManager
from backend.controller.signal_adapter import apply_signal_state


TLS_ID = "C"
INITIAL_STATE = "GGGggrrrrrGGGggrrrrr"


def make_mock_connection(initial_state=INITIAL_STATE):
    connection = Mock()
    trafficlight = connection.trafficlight

    trafficlight.getIDList.return_value = [TLS_ID]
    trafficlight.getControlledLinks.return_value = [
        [("incoming", "outgoing", "internal")]
        for _ in range(len(initial_state))
    ]

    current_state = {"value": initial_state}

    def set_state(tls_id, state):
        current_state["value"] = state

    def get_state(tls_id):
        return current_state["value"]

    trafficlight.setRedYellowGreenState.side_effect = set_state
    trafficlight.getRedYellowGreenState.side_effect = get_state

    return connection


def test_clearance_starts_by_applying_yellow_state():
    connection = make_mock_connection()
    manager = ClearanceManager()

    yellow_state = manager.start(
        current_signal_state=INITIAL_STATE,
        expected_length=len(INITIAL_STATE),
        simulation_time=0,
    )

    applied_state = apply_signal_state(connection, TLS_ID, yellow_state)

    assert applied_state == yellow_state
    assert manager.stage == "yellow"
    assert connection.trafficlight.getRedYellowGreenState(TLS_ID) == yellow_state


def test_all_red_is_applied_after_yellow_duration():
    connection = make_mock_connection()
    manager = ClearanceManager()

    yellow_state = manager.start(
        current_signal_state=INITIAL_STATE,
        expected_length=len(INITIAL_STATE),
        simulation_time=0,
    )
    apply_signal_state(connection, TLS_ID, yellow_state)

    assert manager.update(2.9) == "yellow"

    assert manager.update(3.0) == "all_red"
    all_red_state = manager.current_signal_state

    assert all_red_state is not None

    assert all_red_state == "r" * len(INITIAL_STATE)

    applied_state = apply_signal_state(connection, TLS_ID, all_red_state)

    assert applied_state == all_red_state
    assert connection.trafficlight.getRedYellowGreenState(TLS_ID) == all_red_state


def test_all_red_duration_starts_when_all_red_is_applied():
    connection = make_mock_connection()
    manager = ClearanceManager()

    yellow_state = manager.start(
        current_signal_state=INITIAL_STATE,
        expected_length=len(INITIAL_STATE),
        simulation_time=0,
    )
    apply_signal_state(connection, TLS_ID, yellow_state)

    # The caller does not advance the manager until simulation time 5.
    assert manager.update(5.0) == "all_red"

    all_red_state = manager.current_signal_state

    assert all_red_state is not None

    apply_signal_state(connection, TLS_ID, all_red_state)

    # The all-red interval must not finish immediately after the transition.
    assert manager.update(5.5) == "all_red"
    assert manager.update(6.0) == "complete"
