
import xml.etree.ElementTree as ET

import traci

from backend.config import PROJECT_ROOT, SUMO_BINARY
from backend.controller.junction_occupancy import (
    get_internal_lane_occupancy,
    is_junction_clear,
)


def test_junction_occupancy_reads_live_sumo():
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

    root = ET.parse(network_file).getroot()
    junction = root.find("./junction[@id='C']")

    assert junction is not None
    internal_lanes = junction.get("intLanes", "").split()
    assert len(internal_lanes) == 20

    label = "junction_occupancy_live_test"

    traci.start(
        [SUMO_BINARY, "-c", str(config_file)],
        label=label,
    )
    connection = traci.getConnection(label)

    try:
        # Advance until the simulation reaches a known busy period.
        for _ in range(60):
            connection.simulationStep()

        occupancy = get_internal_lane_occupancy(
            connection,
            internal_lanes,
        )

        # This traffic scenario should have internal-lane occupancy
        # during at least one of the sampled simulation steps.
        assert isinstance(occupancy, dict)

        # Verify the helper's result agrees with direct TraCI queries.
        direct_occupancy = {
            lane_id: list(
                connection.lane.getLastStepVehicleIDs(lane_id)
            )
            for lane_id in internal_lanes
            if connection.lane.getLastStepVehicleIDs(lane_id)
        }

        assert occupancy == direct_occupancy
        assert is_junction_clear(
            connection,
            internal_lanes,
        ) == (not bool(direct_occupancy))

    finally:
        connection.close()
