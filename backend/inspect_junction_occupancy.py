
import xml.etree.ElementTree as ET

import traci

from backend.config import PROJECT_ROOT, SUMO_BINARY


def main():
    network_file = (
        PROJECT_ROOT
        / "simulation"
        / "network"
        / "intersection.net.xml"
    )
    config_file = (
        PROJECT_ROOT
        / "simulation"
        / "intersection.sumocfg"
    )

    tree = ET.parse(network_file)
    root = tree.getroot()

    junction = root.find("./junction[@id='C']")
    if junction is None:
        raise RuntimeError("Junction C was not found in the network.")

    internal_lanes = junction.get("intLanes", "").split()
    if not internal_lanes:
        raise RuntimeError("No internal junction lanes were found.")

    label = "junction_occupancy_inspection"
    traci.start(
        [SUMO_BINARY, "-c", str(config_file)],
        label=label,
    )
    connection = traci.getConnection(label)

    try:
        print(f"Junction: C")
        print(f"Internal lanes discovered: {len(internal_lanes)}")
        print(f"Internal lane IDs: {internal_lanes}")

        for _ in range(60):
            connection.simulationStep()

            occupied = []
            for lane_id in internal_lanes:
                vehicle_ids = (
                    connection.lane.getLastStepVehicleIDs(lane_id)
                )
                if vehicle_ids:
                    occupied.append(
                        (lane_id, list(vehicle_ids))
                    )

            if occupied:
                print(
                    f"Time {connection.simulation.getTime():.0f}s "
                    f"| Internal occupancy: {occupied}"
                )

        print("Occupancy inspection completed.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
