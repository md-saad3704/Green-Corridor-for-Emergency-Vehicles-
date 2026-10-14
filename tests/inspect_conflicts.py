
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

    print("Junction:", junction.get("id"))
    print("Junction type:", junction.get("type"))

    requests = junction.findall("request")
    print("Request elements:", len(requests))

    for request in requests:
        print(
            "index =", request.get("index"),
            "foes =", request.get("foes"),
            "response =", request.get("response"),
            "cont =", request.get("cont"),
        )

    print("\nTraffic-light-controlled connections:")

    for connection in root.findall("connection"):
        if connection.get("tl") != "C":
            continue

        print(
            "index =", connection.get("linkIndex"),
            "from =", connection.get("from"),
            "fromLane =", connection.get("fromLane"),
            "to =", connection.get("to"),
            "toLane =", connection.get("toLane"),
            "via =", connection.get("via"),
        )


if __name__ == "__main__":
    main()
