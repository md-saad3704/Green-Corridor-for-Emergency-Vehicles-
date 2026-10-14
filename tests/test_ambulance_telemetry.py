
import traci

from backend.config import SUMO_BINARY
from backend.telemetry.collector import collect_telemetry


CONFIG_FILE = "simulation/intersection.sumocfg"


def test_ambulance_telemetry_is_collected():
    traci.start([SUMO_BINARY, "-c", CONFIG_FILE])

    try:
        for _ in range(10):
            traci.simulationStep()

        snapshot = collect_telemetry()
        ambulance = snapshot["ambulance"]

        assert ambulance is not None
        assert ambulance["vehicle_id"] == "ambulance_0"
        assert ambulance["is_ambulance"] is True
        assert ambulance["vehicle_type"] == "ambulance"
        assert ambulance["speed_mps"] >= 0

    finally:
        traci.close()



def test_ambulance_distance_matches_next_signal_measurement():
    traci.start([SUMO_BINARY, "-c", CONFIG_FILE])

    try:
        for _ in range(10):
            traci.simulationStep()

        ambulance = collect_telemetry()["ambulance"]
        next_tls = traci.vehicle.getNextTLS("ambulance_0")

        assert ambulance is not None
        assert next_tls, "Expected an upcoming traffic light"

        expected_distance = round(next_tls[0][2], 2)

        assert (
            ambulance["distance_to_intersection_m"]
            == expected_distance
        )

    finally:
        traci.close()
