from backend.controller.controller_config import (
    AMBULANCE_CONFLICT_SIGNAL_INDICES,
    AMBULANCE_ID,
    AMBULANCE_INCOMING_LANE,
    AMBULANCE_INTERNAL_LANE,
    AMBULANCE_OUTGOING_LANE,
    AMBULANCE_SIGNAL_INDEX,
    NORMAL_PROGRAM_ID,
    TRAFFIC_LIGHT_ID,
)
from backend.controller.junction_occupancy import (
    get_internal_lane_occupancy,
)
from backend.controller.network_mapping import get_signal_link_mapping
from backend.inspect_conflicts import decode_foes, load_junction_requests


def assess_live_clearance(
    connection,
    *,
    internal_lane_ids,
    clearance_manager,
):
    """Assess live clearance conditions without actuating signals."""
    failures = []
    tls_id = TRAFFIC_LIGHT_ID

    try:
        trafficlight = connection.trafficlight

        if tls_id not in trafficlight.getIDList():
            return {
                "ready_for_further_review": False,
                "failures": ["Configured traffic light was not found."],
                "signal_actuation_performed": False,
            }

        program_id = trafficlight.getProgram(tls_id)
        signal_state = trafficlight.getRedYellowGreenState(tls_id)
        controlled_links = trafficlight.getControlledLinks(tls_id)
        expected_length = len(controlled_links)

        if program_id not in {NORMAL_PROGRAM_ID, "online"}:
            failures.append(
                f"Unexpected signal program during clearance: {program_id!r}."
            )

        if len(signal_state) != expected_length:
            failures.append("Live signal-state length is inconsistent.")

        if clearance_manager.stage != "complete":
            failures.append("Clearance sequence is not complete.")

        if signal_state != "r" * expected_length:
            failures.append("Live signal state is not all-red.")

        mapping = get_signal_link_mapping(tls_id, connection=connection)
        movement_indices = {movement["signal_index"] for movement in mapping}

        if movement_indices != set(range(expected_length)):
            failures.append(
                "Live controlled-movement indices are incomplete or invalid."
            )

        ambulance_matches = [
            movement
            for movement in mapping
            if movement["signal_index"] == AMBULANCE_SIGNAL_INDEX
            and movement["incoming_lane"] == AMBULANCE_INCOMING_LANE
            and movement["outgoing_lane"] == AMBULANCE_OUTGOING_LANE
            and movement["via_lane"] == AMBULANCE_INTERNAL_LANE
        ]

        if len(ambulance_matches) != 1:
            failures.append("Live ambulance movement does not match configuration.")

        requests = load_junction_requests()
        request_indices = set(requests)

        if request_indices != set(range(expected_length)):
            failures.append(
                "SUMO junction request indices do not match live signal indices."
            )

        observed_conflicts = set()

        if AMBULANCE_SIGNAL_INDEX not in requests:
            failures.append(
                "Ambulance signal index is missing from junction request data."
            )
        else:
            observed_conflicts = decode_foes(requests[AMBULANCE_SIGNAL_INDEX])

            if observed_conflicts != set(AMBULANCE_CONFLICT_SIGNAL_INDICES):
                failures.append(
                    "Configured conflict indices do not match SUMO network data."
                )

        asymmetric_pairs = []

        for index, foes_string in requests.items():
            for foe_index in decode_foes(foes_string):
                if foe_index not in requests:
                    failures.append(
                        f"Junction request {index} references missing foe "
                        f"index {foe_index}."
                    )
                    continue

                if index not in decode_foes(requests[foe_index]):
                    asymmetric_pairs.append((index, foe_index))

        if asymmetric_pairs:
            failures.append("SUMO junction foe relationships are asymmetric.")

        occupancy = get_internal_lane_occupancy(
            connection,
            internal_lane_ids,
        )

        if occupancy:
            failures.append("Internal junction lanes are occupied.")

        return {
            "ready_for_further_review": not failures,
            "failures": failures,
            "traffic_light_id": tls_id,
            "program_id": program_id,
            "signal_state": signal_state,
            "ambulance_id": AMBULANCE_ID,
            "ambulance_signal_index": AMBULANCE_SIGNAL_INDEX,
            "configured_conflict_indices": sorted(AMBULANCE_CONFLICT_SIGNAL_INDICES),
            "observed_conflict_indices": sorted(observed_conflicts),
            "occupied_internal_lanes": occupancy,
            "signal_actuation_performed": False,
        }

    except Exception as exc:
        return {
            "ready_for_further_review": False,
            "failures": [f"Live assessment failed: {type(exc).__name__}: {exc}"],
            "signal_actuation_performed": False,
        }
