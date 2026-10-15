from pathlib import Path

import traci

from backend.config import PROJECT_ROOT, SUMO_BINARY


CONFIG_FILE = PROJECT_ROOT / "simulation" / "intersection.sumocfg"


def test_traci_starts_and_advances_sumo():
    """Verify that TraCI starts SUMO and advances simulation time."""
    traci.start([
        SUMO_BINARY,
        "-c",
        str(CONFIG_FILE),
        "--no-step-log",
        "true",
    ])

    try:
        for _ in range(10):
            traci.simulationStep()

        assert traci.simulation.getTime() == 10.0
        assert len(traci.vehicle.getIDList()) > 0
    finally:
        traci.close()


def test_traci_reports_ambulance_telemetry():
    """Verify that the ambulance appears and exposes telemetry."""
    traci.start([
        SUMO_BINARY,
        "-c",
        str(CONFIG_FILE),
        "--no-step-log",
        "true",
    ])

    try:
        for _ in range(10):
            traci.simulationStep()

        assert "ambulance_0" in traci.vehicle.getIDList()

        ambulance_id = "ambulance_0"
        position = traci.vehicle.getPosition(ambulance_id)
        speed = traci.vehicle.getSpeed(ambulance_id)

        assert len(position) == 2
        assert all(isinstance(value, (int, float)) for value in position)
        assert isinstance(speed, (int, float))
        assert speed >= 0
    finally:
        traci.close()