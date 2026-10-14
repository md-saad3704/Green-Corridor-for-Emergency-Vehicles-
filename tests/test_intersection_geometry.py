
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
        for _ in range(10):
            traci.simulationStep()

        vehicle_id = "ambulance_0"
        current_lane = traci.vehicle.getLaneID(vehicle_id)
        current_edge = traci.vehicle.getRoadID(vehicle_id)

        print("Simulation time:", traci.simulation.getTime())
        print("Ambulance edge:", current_edge)
        print("Ambulance lane:", current_lane)
        print(
            "Lane length (m):",
            traci.lane.getLength(current_lane),
        )
        print(
            "Position on current lane (m):",
            traci.vehicle.getLanePosition(vehicle_id),
        )
        print(
            "Distance to C_E start (m):",
            traci.vehicle.getDrivingDistance(
                vehicle_id, "C_E", 0.0
            ),
        )
        print(
            "Traffic-light state:",
            traci.trafficlight.getRedYellowGreenState("C"),
        )
        print(
            "Traffic-light program:",
            traci.trafficlight.getProgram("C"),
        )

    finally:
        traci.close()


if __name__ == "__main__":
    main()
