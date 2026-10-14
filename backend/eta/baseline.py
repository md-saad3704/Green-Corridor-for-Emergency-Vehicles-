
import math


def estimate_eta(distance_m, speed_mps, minimum_speed_mps=1.0):
    """
    Estimate time to the intersection using current speed.

    Returns ETA in seconds, or None if the distance or speed
    is invalid.
    """
    if distance_m is None or speed_mps is None:
        return None

    try:
        distance = float(distance_m)
        speed = float(speed_mps)
        minimum_speed = float(minimum_speed_mps)
    except (TypeError, ValueError, OverflowError):
        return None

    if not all(
        math.isfinite(value)
        for value in (distance, speed, minimum_speed)
    ):
        return None

    if distance < 0 or minimum_speed <= 0:
        return None

    if distance == 0:
        return 0.0

    effective_speed = max(speed, minimum_speed)
    return round(distance / effective_speed, 2)
