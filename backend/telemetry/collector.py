import traci

AMBULANCE_ID = "ambulance_0"


def collect_telemetry():
    """Collect a snapshot of all active vehicles in SUMO."""
    vehicles = []

    for vehicle_id in traci.vehicle.getIDList():
        position_x, position_y = traci.vehicle.getPosition(vehicle_id)

        vehicle_type = traci.vehicle.getTypeID(vehicle_id)
        is_ambulance = vehicle_id == AMBULANCE_ID

        vehicle_data = {
            "vehicle_id": vehicle_id,
            "edge_id": traci.vehicle.getRoadID(vehicle_id),
            "lane_id": traci.vehicle.getLaneID(vehicle_id),
            "position_x": position_x,
            "position_y": position_y,
            "speed_mps": traci.vehicle.getSpeed(vehicle_id),
            "waiting_time": traci.vehicle.getWaitingTime(vehicle_id),
            "vehicle_type": vehicle_type,
            "is_ambulance": is_ambulance,
            "distance_to_intersection_m": None,
        }


        if is_ambulance:
            next_tls = traci.vehicle.getNextTLS(vehicle_id)

            if next_tls:
                vehicle_data["distance_to_intersection_m"] = round(
                next_tls[0][2],
                2,
            )

        vehicles.append(vehicle_data)

    return {
        "simulation_time": traci.simulation.getTime(),
        "active_vehicle_count": len(vehicles),
        "vehicles": vehicles,
        "ambulance": next(
            (vehicle for vehicle in vehicles if vehicle["is_ambulance"]),
            None,
        ),
    }
