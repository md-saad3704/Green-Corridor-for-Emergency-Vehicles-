
import xml.etree.ElementTree as ET
from pathlib import Path


NETWORK_FILE = Path(
    "simulation/network/intersection.net.xml"
)


def test_request_count_matches_internal_lane_count():
    root = ET.parse(NETWORK_FILE).getroot()
    junction = root.find("./junction[@id='C']")

    assert junction is not None

    requests = junction.findall("request")
    internal_lanes = junction.get("intLanes", "").split()

    assert len(requests) == len(internal_lanes) == 20


def test_request_indices_are_contiguous():
    root = ET.parse(NETWORK_FILE).getroot()
    junction = root.find("./junction[@id='C']")

    assert junction is not None

    request_indices = set()

    for request in junction.findall("request"):
        raw_index = request.get("index")
        assert raw_index is not None
        request_indices.add(int(raw_index))

    assert request_indices == set(range(20))


def test_ambulance_connection_has_expected_internal_lane():
    root = ET.parse(NETWORK_FILE).getroot()

    connection = None

    for item in root.findall("connection"):
        if (
            item.get("tl") == "C"
            and item.get("linkIndex") == "17"
        ):
            connection = item
            break

    assert connection is not None
    assert connection.get("via") == ":C_16_1"



def test_signal_link_indices_are_complete_and_unique():
    import xml.etree.ElementTree as ET
    from pathlib import Path

    network_file = Path(
        "simulation/network/intersection.net.xml"
    )
    root = ET.parse(network_file).getroot()

    indices = []

    for connection in root.findall("connection"):
        if connection.get("tl") != "C":
            continue

        raw_index = connection.get("linkIndex")
        assert raw_index is not None

        indices.append(int(raw_index))

    assert len(indices) == 20
    assert sorted(indices) == list(range(20))


def test_junction_foes_metadata_has_valid_bit_strings():
    import xml.etree.ElementTree as ET
    from pathlib import Path

    network_file = Path(
        "simulation/network/intersection.net.xml"
    )
    root = ET.parse(network_file).getroot()

    junction = root.find("./junction[@id='C']")
    assert junction is not None

    internal_lanes = junction.get("intLanes", "").split()
    requests = junction.findall("request")

    assert len(requests) == len(internal_lanes)

    for request in requests:
        foes = request.get("foes")

        assert foes is not None
        assert len(foes) == len(requests)
        assert set(foes) <= {"0", "1"}
