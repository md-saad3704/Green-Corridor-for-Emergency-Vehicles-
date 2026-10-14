
# Controller configuration
# All durations are measured in simulation seconds.

# Request priority when the ambulance is sufficiently close.
PRIORITY_ETA_THRESHOLD_SECONDS = 30.0

# Signal transition safety intervals.
YELLOW_DURATION_SECONDS = 3.0
ALL_RED_DURATION_SECONDS = 1.0

# Maximum time allowed to serve the emergency vehicle.
MAX_EMERGENCY_GREEN_SECONDS = 30.0

# Maximum time to wait for confirmation that the ambulance passed.
PASSAGE_VERIFICATION_TIMEOUT_SECONDS = 10.0

# Maximum age of telemetry before it is considered stale.
MAX_TELEMETRY_AGE_SECONDS = 3.0

# Minimum time to wait before returning to normal operation.
MIN_RECOVERY_SECONDS = 2.0
