
def remaining_lane_distance(lane_length_m, lane_position_m):
    """Return the remaining distance to the end of the current lane."""
    if lane_length_m is None or lane_position_m is None:
        return None

    if lane_length_m < 0 or lane_position_m < 0:
        return None

    if lane_position_m > lane_length_m:
        return None

    return round(lane_length_m - lane_position_m, 2)
