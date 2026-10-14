
import traci

from backend.config import SUMO_BINARY

CONFIG_FILE = "simulation/intersection.sumocfg"


def main():
    traci.start([
        SUMO_BINARY,
        "-c",
        CONFIG_FILE,
    ])

    try:
        # Advance the simulation until the ambulance is expected to depart.
        for _ in range(10):
            traci.simulationStep()

        vehicle_ids = traci.vehicle.getIDList()

        print("Simulation time:", traci.simulation.getTime())
        print("Ambulance present:", "ambulance_0" in vehicle_ids)

        if "ambulance_0" in vehicle_ids:
            print(
                "Ambulance type:",
                traci.vehicle.getTypeID("ambulance_0"),
            )
            print(
                "Ambulance position:",
                traci.vehicle.getPosition("ambulance_0"),
            )
            print(
                "Ambulance speed (m/s):",
                traci.vehicle.getSpeed("ambulance_0"),
            )

    finally:
        traci.close()


if __name__ == "__main__":
    main()
