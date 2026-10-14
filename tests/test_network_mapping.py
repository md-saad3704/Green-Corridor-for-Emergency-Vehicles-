
import traci

from backend.config import SUMO_BINARY
from backend.controller.network_mapping import get_signal_link_mapping


CONFIG_FILE = "simulation/intersection.sumocfg"


def test_ambulance_movement_is_present_in_signal_mapping():
    traci.start([SUMO_BINARY, "-c", CONFIG_FILE])

    try:
        mapping = get_signal_link_mapping("C")

        ambulance_movement = [
            item
            for item in mapping
            if item["signal_index"] == 17
            and item["incoming_lane"] == "W_C_1"
            and item["outgoing_lane"] == "C_E_1"
        ]

        assert ambulance_movement
    finally:
        traci.close()


def test_mapping_contains_all_controlled_links():
    traci.start([SUMO_BINARY, "-c", CONFIG_FILE])

    try:
        mapping = get_signal_link_mapping("C")
        indices = {item["signal_index"] for item in mapping}

        assert indices == set(range(20))
    finally:
        traci.close()
