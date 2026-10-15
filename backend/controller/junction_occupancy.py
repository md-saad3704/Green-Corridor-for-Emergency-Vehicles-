
def get_internal_lane_occupancy(
    connection,
    internal_lane_ids,
    excluded_vehicle_ids=(),
):
    """
    Return vehicles occupying internal junction lanes.

    Excluded vehicle IDs are omitted from the report, but this function
    does not determine whether it is safe to grant a signal green.
    """
    excluded = set(excluded_vehicle_ids)
    occupancy = {}

    for lane_id in internal_lane_ids:
        vehicle_ids = connection.lane.getLastStepVehicleIDs(lane_id)
        remaining = [
            vehicle_id
            for vehicle_id in vehicle_ids
            if vehicle_id not in excluded
        ]

        if remaining:
            occupancy[lane_id] = list(remaining)

    return occupancy


def is_junction_clear(
    connection,
    internal_lane_ids,
    excluded_vehicle_ids=(),
):
    """
    Return whether the queried internal lanes have no non-excluded vehicles.

    This is an occupancy observation, not a complete traffic-safety check.
    """
    occupancy = get_internal_lane_occupancy(
        connection,
        internal_lane_ids,
        excluded_vehicle_ids,
    )

    return not occupancy
