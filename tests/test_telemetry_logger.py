
import traci

from backend.config import SUMO_BINARY
from backend.telemetry.collector import collect_telemetry
from backend.telemetry.logger import initialize_log, log_snapshot

CONFIG_FILE = "simulation/intersection.sumocfg"


def main():
    initialize_log()

    traci.start([SUMO_BINARY, "-c", CONFIG_FILE])

    try:
        for _ in range(20):
            traci.simulationStep()
            snapshot = collect_telemetry()
            log_snapshot(snapshot)

        print("Telemetry logging: successful")
        print("Simulation time:", traci.simulation.getTime())
    finally:
        traci.close()


if __name__ == "__main__":
    main()
