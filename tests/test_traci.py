
from backend.config import SUMO_BINARY
import traci

CONFIG_FILE = "simulation/intersection.sumocfg"

traci.start([
    SUMO_BINARY,
    "-c",
    CONFIG_FILE,
])

try:
    for _ in range(10):
        traci.simulationStep()

    vehicle_ids = traci.vehicle.getIDList()

    print("TraCI connection: successful")
    print("Simulation time:", traci.simulation.getTime())
    print("Active vehicles:", len(vehicle_ids))

    if vehicle_ids:
        vehicle_id = vehicle_ids[0]
        print("Sample vehicle:", vehicle_id)
        print("Position:", traci.vehicle.getPosition(vehicle_id))
        print("Speed (m/s):", traci.vehicle.getSpeed(vehicle_id))
finally:
    traci.close()
