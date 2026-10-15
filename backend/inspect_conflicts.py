
import xml.etree.ElementTree as ET

import traci

from backend.config import PROJECT_ROOT, SUMO_BINARY
from backend.controller.network_mapping import get_signal_link_mapping


NETWORK_FILE = (
    PROJECT_ROOT
    / "simulation"
    / "network"
    / "intersection.net.xml"
)
CONFIG_FILE = PROJECT_ROOT / "simulation" / "intersection.sumocfg"
TLS_ID = "C"
AMBULANCE_SIGNAL_INDEX = 17


def load_junction_requests():
    """Read junction request and foe data from the generated SUMO network."""
    tree = ET.parse(NETWORK_FILE)
    junction = tree.find(f".//junction[@id='{TLS_ID}']")

    if junction is None:
        raise ValueError(f"Junction {TLS_ID!r} was not found.")

    requests = {}

    for element in junction.findall("request"):
        index = int(element.attrib["index"])
        foes = element.attrib["foes"]

        if index in requests:
            raise ValueError(f"Duplicate junction request index: {index}")

        if len(foes) != len(junction.findall("request")):
            raise ValueError(
                f"Unexpected foes-string length for request {index}."
            )

        requests[index] = foes

    return requests


def decode_foes(foes):
    """Decode SUMO's foes bit string, with request index 0 at the right."""
    return {
        index
        for index, bit in enumerate(reversed(foes))
        if bit == "1"
    }


def main():
    requests = load_junction_requests()

    traci.start([
        SUMO_BINARY,
        "-c",
        str(CONFIG_FILE),
        "--no-step-log",
        "true",
    ])

    try:
        mapping = get_signal_link_mapping(TLS_ID)

        movement_by_index = {
            item["signal_index"]: item
            for item in mapping
        }

        if set(requests) != set(movement_by_index):
            raise ValueError(
                "Junction request indices do not match traffic-light "
                "signal indices. Do not use this mapping for control."
            )

        ambulance_index = AMBULANCE_SIGNAL_INDEX

        if ambulance_index not in requests:
            raise ValueError(
                f"Ambulance signal index {ambulance_index} is missing."
            )

        foes = decode_foes(requests[ambulance_index])

        print("\n=== AMBULANCE MOVEMENT ===")
        print("Signal index:", ambulance_index)
        print("Movement:", movement_by_index[ambulance_index])

        print("\n=== FOE MOVEMENTS FROM SUMO NETWORK ===")
        print("Foe indices:", sorted(foes))

        for index in sorted(foes):
            print(f"{index}: {movement_by_index.get(index)}")

        print("\n=== FOE RELATIONSHIP CHECK ===")
        asymmetric_pairs = []

        for index, foes_string in requests.items():
            for foe_index in decode_foes(foes_string):
                if foe_index not in requests:
                    raise ValueError(
                        f"Request {index} references missing foe "
                        f"index {foe_index}."
                    )

                reverse_foes = decode_foes(requests[foe_index])

                if index not in reverse_foes:
                    asymmetric_pairs.append((index, foe_index))

        if asymmetric_pairs:
            print("Asymmetric foe pairs:", asymmetric_pairs)
        else:
            print("All decoded foe relationships are symmetric.")

        print(
            "\nNote: this is a diagnostic of SUMO's junction conflict data, "
            "not yet an approved signal-control configuration."
        )

    finally:
        traci.close()


if __name__ == "__main__":
    main()
