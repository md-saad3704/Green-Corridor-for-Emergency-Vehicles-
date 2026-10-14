
import traci

from backend.config import SUMO_BINARY
from backend.telemetry.collector import collect_telemetry


CONFIG_FILE = "simulation/intersection.sumocfg"


def test_telemetry_snapshot_contains_required_fields():
    traci.start([SUMO_BINARY, "-c", CONFIG_FILE])

    try:
        for _ in range(10):
            traci.simulationStep()

        snapshot = collect_telemetry()

        assert "simulation_time" in snapshot
        assert "active_vehicle_count" in snapshot
        assert "vehicles" in snapshot
        assert "ambulance" in snapshot

        assert snapshot["simulation_time"] == 10.0
        assert snapshot["active_vehicle_count"] > 0

    finally:
        traci.close()


def test_vehicle_telemetry_contains_required_fields():
    traci.start([SUMO_BINARY, "-c", CONFIG_FILE])

    try:
        for _ in range(10):
            traci.simulationStep()

        snapshot = collect_telemetry()
        assert snapshot["vehicles"]

        vehicle = snapshot["vehicles"][0]

        required_fields = {
            "vehicle_id",
            "edge_id",
            "lane_id",
            "position_x",
            "position_y",
            "speed_mps",
            "waiting_time",
            "vehicle_type",
            "is_ambulance",
            "distance_to_intersection_m",
        }

        assert required_fields.issubset(vehicle.keys())

    finally:
        traci.close()
