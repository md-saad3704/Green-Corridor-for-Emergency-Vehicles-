
import traci

from backend.config import SUMO_BINARY
from backend.telemetry.collector import collect_telemetry
from backend.eta.service import estimate_ambulance_eta


CONFIG_FILE = "simulation/intersection.sumocfg"


def main():
    traci.start([
        SUMO_BINARY,
        "-c",
        CONFIG_FILE,
    ])

    try:
        for _ in range(10):
            traci.simulationStep()

        snapshot = collect_telemetry()
        result = estimate_ambulance_eta(snapshot["ambulance"])

        print("Live ambulance ETA result:")
        print(result)

    finally:
        traci.close()


if __name__ == "__main__":
    main()
