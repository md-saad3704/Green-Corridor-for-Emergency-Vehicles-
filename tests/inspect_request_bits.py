
import xml.etree.ElementTree as ET
from pathlib import Path

NETWORK_FILE = Path(
    "simulation/network/intersection.net.xml"
)


def main():
    root = ET.parse(NETWORK_FILE).getroot()
    junction = root.find("./junction[@id='C']")

    if junction is None:
        raise RuntimeError("Junction C was not found.")

    
    requests = {}

    for item in junction.findall("request"):
        raw_index = item.get("index")

        if raw_index is None:
            continue

        try:
            request_index = int(raw_index)
        except ValueError:
            continue

    requests[request_index] = item


    # SUMO's junction request order follows the junction's
    # internal connection ordering, not necessarily traffic-light
    # link indices.
    internal_lanes = junction.get("intLanes", "").split()

    connections = {}

    for connection in root.findall("connection"):
        if connection.get("tl") != "C":
            continue

        raw_index = connection.get("linkIndex")
        if raw_index is None:
            continue

        index = int(raw_index)
        
        connections[index] = {
            "from": connection.get("from"),
            "fromLane": connection.get("fromLane"),
            "to": connection.get("to"),
            "toLane": connection.get("toLane"),
            "via": connection.get("via"),
        }

    target_index = 17
    foes = requests[target_index].get("foes", "")

    print("Target traffic-light connection:")
    print(connections[target_index])

    print("\nJunction internal lanes:")
    for index, lane in enumerate(internal_lanes):
        print(f"  Request-order candidate {index}: {lane}")

    print("\nRequest indices with a set foe bit:")
    for position, bit in enumerate(reversed(foes)):
        if bit == "1":
            print(f"  Candidate request index: {position}")

    print(
        "\nNote: request indices and traffic-light link indices "
        "must be mapped separately and verified before use."
    )


if __name__ == "__main__":
    main()
