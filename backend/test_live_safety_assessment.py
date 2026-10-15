
import xml.etree.ElementTree as ET

import traci

from backend.config import SUMO_BINARY, PROJECT_ROOT
from backend.controller.clearance_manager import ClearanceManager
from backend.controller.controller_config import (
    ALL_RED_DURATION,
    NORMAL_PROGRAM_ID,
    TRAFFIC_LIGHT_ID,
    YELLOW_DURATION,
)
from backend.controller.live_safety import assess_live_clearance
from backend.controller.signal_adapter import apply_signal_state


CONFIG_FILE = PROJECT_ROOT / "simulation" / "intersection.sumocfg"
NET_FILE = PROJECT_ROOT / "simulation" / "network" / "intersection.net.xml"


def get_internal_lanes():
    """Read internal lane IDs from the generated SUMO network."""
    root = ET.parse(NET_FILE).getroot()

    for junction in root.findall("junction"):
        if junction.get("id") == TRAFFIC_LIGHT_ID:
            return junction.get("intLanes", "").split()

    raise RuntimeError(
        f"Junction {TRAFFIC_LIGHT_ID!r} was not found in the network."
    )


def main():
    traci.start([
        SUMO_BINARY,
        "-c",
        str(CONFIG_FILE),
        "--no-step-log",
        "true",
    ])

    original_program = None

    try:
        for _ in range(10):
            traci.simulationStep()

        tls_id = TRAFFIC_LIGHT_ID
        original_program = traci.trafficlight.getProgram(tls_id)
        initial_state = traci.trafficlight.getRedYellowGreenState(tls_id)
        expected_length = len(
            traci.trafficlight.getControlledLinks(tls_id)
        )

        print("Initial simulation time:", traci.simulation.getTime())
        print("Initial program:", original_program)
        print("Initial signal state:", initial_state)

        if original_program != NORMAL_PROGRAM_ID:
            raise RuntimeError(
                f"Expected program {NORMAL_PROGRAM_ID!r}, "
                f"got {original_program!r}."
            )

        manager = ClearanceManager()
        yellow_state = manager.start(
            current_signal_state=initial_state,
            expected_length=expected_length,
            simulation_time=traci.simulation.getTime(),
        )

        print("\nApplying yellow clearance...")
        apply_signal_state(traci, tls_id, yellow_state)
        yellow_started_at = traci.simulation.getTime()

        while (
            traci.simulation.getTime() - yellow_started_at
            < YELLOW_DURATION
        ):
            traci.simulationStep()

        stage = manager.update(traci.simulation.getTime())
        if stage != "all_red":
            raise RuntimeError(
                f"Expected all_red stage, got {stage!r}."
            )

        all_red_state = manager.current_signal_state
        if all_red_state is None:
            raise RuntimeError("No all-red state was produced.")

        print("Applying all-red clearance...")
        apply_signal_state(traci, tls_id, all_red_state)
        all_red_started_at = traci.simulation.getTime()

        while (
            traci.simulation.getTime() - all_red_started_at
            < ALL_RED_DURATION
        ):
            traci.simulationStep()

        stage = manager.update(traci.simulation.getTime())
        if stage != "complete":
            raise RuntimeError(
                f"Expected complete clearance stage, got {stage!r}."
            )

        internal_lanes = get_internal_lanes()

        print("\n=== LIVE CLEARANCE ASSESSMENT ===")
        print(
            "Program during override:",
            traci.trafficlight.getProgram(tls_id),
        )
        print(
            "Signal state:",
            traci.trafficlight.getRedYellowGreenState(tls_id),
        )
        print("Clearance stage:", manager.stage)

        result = assess_live_clearance(
            traci,
            internal_lane_ids=internal_lanes,
            clearance_manager=manager,
        )

        for key, value in result.items():
            print(f"{key}: {value}")

        if result.get("signal_actuation_performed") is not False:
            raise RuntimeError(
                "Assessment did not confirm that it remained read-only."
            )

        if result.get("ready_for_further_review"):
            print(
                "\nASSESSMENT: Preconditions passed for further review only. "
                "No emergency green was authorized."
            )
        else:
            print(
                "\nASSESSMENT: Blocked. Review the listed failures. "
                "No emergency green was authorized."
            )

    finally:
        # Restore the normal program for this diagnostic before closing SUMO.
        if original_program is not None:
            try:
                traci.trafficlight.setProgram(
                    TRAFFIC_LIGHT_ID,
                    NORMAL_PROGRAM_ID,
                )
                restored = traci.trafficlight.getProgram(
                    TRAFFIC_LIGHT_ID
                )
                print("\nRestored normal program:", restored)

                if restored != NORMAL_PROGRAM_ID:
                    print("WARNING: Normal program restoration was not verified.")
            finally:
                traci.close()
        else:
            traci.close()


if __name__ == "__main__":
    main()
