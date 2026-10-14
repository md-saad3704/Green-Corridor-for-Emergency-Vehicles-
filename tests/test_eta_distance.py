
from backend.eta.distance import remaining_lane_distance


def test_remaining_lane_distance():
    assert remaining_lane_distance(189.6, 59.4383327433) == 130.16


def test_vehicle_at_lane_end():
    assert remaining_lane_distance(189.6, 189.6) == 0.0


def test_missing_lane_measurement():
    assert remaining_lane_distance(None, 50.0) is None


def test_invalid_lane_position():
    assert remaining_lane_distance(189.6, 200.0) is None
