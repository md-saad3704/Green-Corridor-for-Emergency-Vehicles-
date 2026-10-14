
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

    internal_lanes = junction.get("intLanes", "").split()
    
    requests = {}

    for item in junction.findall("request"):
        raw_index = item.get("index")

        if raw_index is None:
            continue

        try :
            request_index = int(raw_index)
        except ValueError:
            continue

        requests[request_index] = item


    connections_by_via = {}

    for connection in root.findall("connection"):
        via_lane = connection.get("via")

        if via_lane:
            connections_by_via[via_lane] = {
                "from": connection.get("from"),
                "fromLane": connection.get("fromLane"),
                "to": connection.get("to"),
                "toLane": connection.get("toLane"),
                "signal_index": connection.get("linkIndex"),
            }

    target_lane = ":C_16_1"

    if target_lane not in internal_lanes:
        raise RuntimeError(
            f"Ambulance internal lane {target_lane} was not found."
        )

    target_request_index = internal_lanes.index(target_lane)
    
    print("Target request index:", target_request_index)
    print("Available request indices:", sorted(requests.keys()))
    print("Number of request entries:", len(requests))

    if target_request_index not in requests:
        raise RuntimeError(
            "Target request index is missing from the request dictionary. "
            "Check how the request entries are parsed."
        )

    target_request = requests[target_request_index]

    foes = target_request.get("foes", "")

    print("Ambulance internal lane:", target_lane)
    print("Request index:", target_request_index)
    print("Controlled connection:", connections_by_via.get(target_lane))
    print("Foes bit string:", foes)
    print("\nCandidate foe connections:")

    for index, bit in enumerate(reversed(foes)):
        if bit != "1":
            continue

        foe_lane = (
            internal_lanes[index]
            if index < len(internal_lanes)
            else None
        )

        print(
            f"Request {index}: internal lane={foe_lane}, "
            f"connection={connections_by_via.get(foe_lane)}"
        )


if __name__ == "__main__":
    main()
