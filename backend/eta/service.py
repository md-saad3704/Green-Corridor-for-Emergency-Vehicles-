
import math

from backend.eta.baseline import estimate_eta


def estimate_ambulance_eta(ambulance_telemetry):
    """Calculate a validated baseline ETA from ambulance telemetry."""
    if ambulance_telemetry is None:
        return {
            "eta_seconds": None,
            "status": "ambulance_not_available",
        }

    distance = ambulance_telemetry.get(
        "distance_to_intersection_m"
    )
    speed = ambulance_telemetry.get("speed_mps")

    try:
        distance = float(distance)
    except (TypeError, ValueError, OverflowError):
        return {
            "eta_seconds": None,
            "status": "distance_unavailable",
        }

    if not math.isfinite(distance) or distance < 0:
        return {
            "eta_seconds": None,
            "status": "distance_unavailable",
        }

    try:
        speed_value = float(speed)
    except (TypeError, ValueError, OverflowError):
        return {
            "eta_seconds": None,
            "status": "speed_unavailable",
        }

    if not math.isfinite(speed_value):
        return {
            "eta_seconds": None,
            "status": "speed_unavailable",
        }

    eta_seconds = estimate_eta(distance, speed_value)

    if eta_seconds is None:
        return {
            "eta_seconds": None,
            "status": "invalid_telemetry",
        }

    return {
        "eta_seconds": eta_seconds,
        "status": "estimated",
        "distance_m": round(distance, 2),
        "speed_mps": round(max(speed_value, 0.0), 2),
    }
