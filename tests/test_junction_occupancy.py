
from unittest.mock import Mock

from backend.controller.junction_occupancy import (
    get_internal_lane_occupancy,
    is_junction_clear,
)


def make_connection(lane_vehicles):
    connection = Mock()
    connection.lane.getLastStepVehicleIDs.side_effect = (
        lambda lane_id: lane_vehicles.get(lane_id, [])
    )
    return connection


def test_empty_internal_lanes_are_clear():
    connection = make_connection({})

    assert is_junction_clear(connection, [":C_1_0", ":C_6_0"])


def test_occupied_internal_lane_is_reported():
    connection = make_connection({
        ":C_1_0": ["north_traffic.0"],
        ":C_6_0": [],
    })

    assert get_internal_lane_occupancy(
        connection, [":C_1_0", ":C_6_0"]
    ) == {":C_1_0": ["north_traffic.0"]}

    assert not is_junction_clear(
        connection, [":C_1_0", ":C_6_0"]
    )


def test_excluded_ambulance_does_not_appear_in_occupancy():
    connection = make_connection({
        ":C_16_1": ["ambulance_0"],
    })

    assert get_internal_lane_occupancy(
        connection,
        [":C_16_1"],
        excluded_vehicle_ids={"ambulance_0"},
    ) == {}

    assert is_junction_clear(
        connection,
        [":C_16_1"],
        excluded_vehicle_ids={"ambulance_0"},
    )
