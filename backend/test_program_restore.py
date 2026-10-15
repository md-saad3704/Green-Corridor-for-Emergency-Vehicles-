
import traci

from backend.config import PROJECT_ROOT, SUMO_BINARY


def main():
    config_file = (
        PROJECT_ROOT
        / "simulation"
        / "intersection.sumocfg"
    )

    label = "program_restore_test"

    traci.start(
        [SUMO_BINARY, "-c", str(config_file)],
        label=label,
    )
    connection = traci.getConnection(label)

    try:
        connection.simulationStep()

        tls_id = "C"

        print(
            "Initial program:",
            connection.trafficlight.getProgram(tls_id),
        )
        print(
            "Initial phase:",
            connection.trafficlight.getPhase(tls_id),
        )
        print(
            "Initial signal:",
            connection.trafficlight.getRedYellowGreenState(tls_id),
        )

        # Apply a temporary signal override.
        connection.trafficlight.setRedYellowGreenState(
            tls_id,
            "r" * len(
                connection.trafficlight.getControlledLinks(tls_id)
            ),
        )

        print(
            "After override:",
            connection.trafficlight.getRedYellowGreenState(tls_id),
        )

        # Explicitly select the normal fixed-time program.
        connection.trafficlight.setProgram(tls_id, "0")

        print(
            "After restoring program:",
            connection.trafficlight.getProgram(tls_id),
        )
        print(
            "Phase after restoring:",
            connection.trafficlight.getPhase(tls_id),
        )
        print(
            "Signal after restoring:",
            connection.trafficlight.getRedYellowGreenState(tls_id),
        )

        connection.simulationStep()

        print(
            "Signal after next simulation step:",
            connection.trafficlight.getRedYellowGreenState(tls_id),
        )
        print(
            "Phase after next simulation step:",
            connection.trafficlight.getPhase(tls_id),
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()
