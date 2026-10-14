
from enum import Enum


class ControllerState(str, Enum):
    NORMAL_FIXED_TIME = "normal_fixed_time"
    PRIORITY_REQUESTED = "priority_requested"
    CLEARANCE = "clearance"
    EMERGENCY_GREEN = "emergency_green"
    PASSAGE_VERIFICATION = "passage_verification"
    RECOVERY = "recovery"
    SAFE_FAILURE = "safe_failure"
