
import traci

from backend.config import PROJECT_ROOT, SUMO_BINARY
from backend.controller.signal_adapter import apply_signal_state


def test_signal_adapter_applies_state_to_live_sumo():
    config_file = (
        PROJECT_ROOT / "simulation" / "intersection.sumocfg"
    )
    connection_label = "signal_adapter_live_test"

    traci.start(
        [
            SUMO_BINARY,
            "-c",
            str(config_file),
        ],
        label=connection_label,
    )
    connection = traci.getConnection(connection_label)

    try:
        connection.simulationStep()

        assert "C" in connection.trafficlight.getIDList()

        controlled_links = (
            connection.trafficlight.getControlledLinks("C")
        )
        expected_length = len(controlled_links)
        assert expected_length == 20

        # Isolated adapter test only; not the emergency-control sequence.
        requested_state = "r" * expected_length

        result = apply_signal_state(
            connection,
            "C",
            requested_state,
        )

        assert result == requested_state
        assert (
            connection.trafficlight.getRedYellowGreenState("C")
            == requested_state
        )
    finally:
        connection.close()
