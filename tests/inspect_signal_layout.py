
import traci

from backend.config import SUMO_BINARY

CONFIG_FILE = "simulation/intersection.sumocfg"
AMBULANCE_ID = "ambulance_0"


def main():
    traci.start([SUMO_BINARY, "-c", CONFIG_FILE])

    try:
        for _ in range(10):
            traci.simulationStep()

        print("Simulation time:", traci.simulation.getTime())

        if AMBULANCE_ID not in traci.vehicle.getIDList():
            print("Ambulance is not currently active.")
            return

        print("Ambulance ID:", AMBULANCE_ID)
        print("Route:", traci.vehicle.getRoute(AMBULANCE_ID))
        print("Current edge:", traci.vehicle.getRoadID(AMBULANCE_ID))
        print("Current lane:", traci.vehicle.getLaneID(AMBULANCE_ID))
        print("Position:", traci.vehicle.getPosition(AMBULANCE_ID))
        print("Speed (m/s):", traci.vehicle.getSpeed(AMBULANCE_ID))

        next_tls = traci.vehicle.getNextTLS(AMBULANCE_ID)
        print("Next traffic light:", next_tls)

        if next_tls:
            tls_id, link_index, distance, signal_state = next_tls[0]
            print("Traffic-light ID:", tls_id)
            print("Signal link index:", link_index)
            print("Distance to traffic light (m):", round(distance, 2))
            print("Signal state at that link:", signal_state)

    finally:
        traci.close()


if __name__ == "__main__":
    main()
