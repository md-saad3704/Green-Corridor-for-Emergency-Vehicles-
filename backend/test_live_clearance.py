
import traci

from backend.config import SUMO_BINARY, PROJECT_ROOT
from backend.controller.clearance_manager import ClearanceManager
from backend.controller.controller_config import (
    ALL_RED_DURATION,
    NORMAL_PROGRAM_ID,
    TRAFFIC_LIGHT_ID,
    YELLOW_DURATION,
)
from backend.controller.signal_adapter import apply_signal_state


CONFIG_FILE = PROJECT_ROOT / "simulation" / "intersection.sumocfg"


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
        # Start the simulation and allow the normal program to run.
        for _ in range(10):
            traci.simulationStep()

        tls_id = TRAFFIC_LIGHT_ID
        original_program = traci.trafficlight.getProgram(tls_id)
        initial_state = traci.trafficlight.getRedYellowGreenState(tls_id)
        controlled_links = traci.trafficlight.getControlledLinks(tls_id)
        expected_length = len(controlled_links)

        print("Initial simulation time:", traci.simulation.getTime())
        print("Initial program:", original_program)
        print("Initial signal state:", initial_state)

        if original_program != NORMAL_PROGRAM_ID:
            raise RuntimeError(
                f"Expected normal program {NORMAL_PROGRAM_ID!r}, "
                f"got {original_program!r}."
            )

        manager = ClearanceManager()
        yellow_state = manager.start(
            current_signal_state=initial_state,
            expected_length=expected_length,
            simulation_time=traci.simulation.getTime(),
        )

        # Apply and verify yellow before counting its duration.
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
                f"Expected all_red stage after yellow; got {stage!r}."
            )

        all_red_state = manager.current_signal_state
        if all_red_state is None:
            raise RuntimeError("Clearance manager returned no all-red state.")

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
                f"Expected complete clearance stage; got {stage!r}."
            )

        current_state = traci.trafficlight.getRedYellowGreenState(tls_id)
        if current_state != all_red_state:
            raise RuntimeError(
                "All-red state changed unexpectedly during clearance."
            )

        print("Yellow clearance verified.")
        print("All-red clearance verified.")
        print("No emergency green was requested.")

    finally:
        # Restore the normal program before closing SUMO.
        if original_program is not None:
            try:
                traci.trafficlight.setProgram(
                    TRAFFIC_LIGHT_ID,
                    NORMAL_PROGRAM_ID,
                )
                restored_program = traci.trafficlight.getProgram(
                    TRAFFIC_LIGHT_ID
                )
                if restored_program != NORMAL_PROGRAM_ID:
                    raise RuntimeError(
                        "Normal signal program restoration failed: "
                        f"{restored_program!r}."
                    )
                print("Restored normal program:", restored_program)
                print(
                    "Restored signal state:",
                    traci.trafficlight.getRedYellowGreenState(
                        TRAFFIC_LIGHT_ID
                    ),
                )
            finally:
                traci.close()
        else:
            traci.close()


if __name__ == "__main__":
    main()
