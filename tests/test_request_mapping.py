
import xml.etree.ElementTree as ET
from pathlib import Path


NETWORK_FILE = Path(
    "simulation/network/intersection.net.xml"
)


def test_junction_has_twenty_request_entries():
    root = ET.parse(NETWORK_FILE).getroot()
    junction = root.find("./junction[@id='C']")

    assert junction is not None

    requests = junction.findall("request")
    
    indices = set()

    for request in requests:
        raw_index = request.get("index")

        if raw_index is None:
            continue

        indices.add(int(raw_index))


    assert len(requests) == 20
    assert indices == set(range(20))


def test_ambulance_connection_is_signal_index_17():
    root = ET.parse(NETWORK_FILE).getroot()

    ambulance_connection = None

    for connection in root.findall("connection"):
        if (
            connection.get("tl") == "C"
            and connection.get("linkIndex") == "17"
        ):
            ambulance_connection = connection
            break

    assert ambulance_connection is not None
    assert ambulance_connection.get("from") == "W_C"
    assert ambulance_connection.get("fromLane") == "1"
    assert ambulance_connection.get("to") == "C_E"
    assert ambulance_connection.get("toLane") == "1"
