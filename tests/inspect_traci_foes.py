
import xml.etree.ElementTree as ET
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
NETWORK_FILE = (
    PROJECT_ROOT
    / "simulation"
    / "network"
    / "intersection.net.xml"
)


def main():
    root = ET.parse(NETWORK_FILE).getroot()
    junction = root.find("./junction[@id='C']")

    if junction is None:
        raise RuntimeError("Junction C was not found.")

    internal_lanes = junction.get("intLanes", "").split()
    
    requests = {}

    for request in junction.findall("request"):
        raw_index = request.get("index")

        if raw_index is None:
            continue

        try:
            request_index = int(raw_index)
        except ValueError:
            continue

        requests[request_index] = request


    signal_connections = {}

    for connection in root.findall("connection"):
        if connection.get("tl") != "C":
            continue

        raw_index = connection.get("linkIndex")
        if raw_index is None:
            continue

        signal_connections[int(raw_index)] = connection

    target_signal_index = 17
    target_connection = signal_connections[target_signal_index]
    target_via = target_connection.get("via")

    if target_via not in internal_lanes:
        raise RuntimeError(
            f"Target lane {target_via} is not in the request ordering."
        )

    target_request_index = internal_lanes.index(target_via)
    target_request = requests[target_request_index]
    foes = target_request.get("foes", "")

    print("Target signal index:", target_signal_index)
    print("Target movement: W_C lane 1 -> C_E lane 1")
    print("Target internal lane:", target_via)
    print("Target request index:", target_request_index)
    print("Foes bit string:", foes)
    print("\nFoe request entries:")

    for request_index, bit in enumerate(reversed(foes)):
        if bit != "1":
            continue

        foe_lane = internal_lanes[request_index]
        print(f"\nRequest {request_index}: {foe_lane}")

        matching_connections = [
            connection
            for connection in root.findall("connection")
            if connection.get("via") == foe_lane
        ]

        if not matching_connections:
            print("  No direct connection via this lane.")
            continue

        for connection in matching_connections:
            print(
                "  Movement:",
                f"{connection.get('from')}_{connection.get('fromLane')}",
                "->",
                f"{connection.get('to')}_{connection.get('toLane')}",
                "| signal index:",
                connection.get("linkIndex", "not directly controlled"),
            )


if __name__ == "__main__":
    main()
