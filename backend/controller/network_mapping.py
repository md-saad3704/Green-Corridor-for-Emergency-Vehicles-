
import traci


def get_signal_link_mapping(tls_id="C", connection=None):
    """Return controlled movements for a SUMO traffic light."""
    if connection is None:
        connection = traci

    trafficlight = connection.trafficlight

    if tls_id not in trafficlight.getIDList():
        raise ValueError(
            f"Traffic light {tls_id!r} was not found."
        )

    controlled_links = trafficlight.getControlledLinks(tls_id)
    mapping = []

    for signal_index, link_group in enumerate(controlled_links):
        for incoming_lane, outgoing_lane, via_lane in link_group:
            mapping.append(
                {
                    "signal_index": signal_index,
                    "incoming_lane": incoming_lane,
                    "outgoing_lane": outgoing_lane,
                    "via_lane": via_lane,
                }
            )

    return mapping
