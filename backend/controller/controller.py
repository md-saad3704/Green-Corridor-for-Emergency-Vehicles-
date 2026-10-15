
import math

from backend.controller.controller_config import (
    PRIORITY_ETA_THRESHOLD,
)
from backend.controller.states import ControllerState
from backend.controller.transitions import determine_next_state


class EmergencyVehicleController:
    """Manage controller state and evaluate ambulance priority requests."""

    def __init__(self):
        self.state = ControllerState.NORMAL_FIXED_TIME

    def evaluate_priority_request(
        self,
        ambulance_available,
        eta_seconds,
        telemetry_valid=True,
    ):
        """
        Evaluate whether an ambulance priority request should be made.

        This method updates logical controller state only. It does not
        change traffic signals or authorize an ambulance green.
        """
        if self.state != ControllerState.NORMAL_FIXED_TIME:
            return self.state

        # Reject ambiguous availability or telemetry flags.
        if (
            not isinstance(ambulance_available, bool)
            or not isinstance(telemetry_valid, bool)
        ):
            self.state = ControllerState.SAFE_FAILURE
            return self.state

        if not telemetry_valid:
            self.state = determine_next_state(
                current_state=self.state,
                ambulance_available=ambulance_available,
                eta_seconds=eta_seconds,
                telemetry_valid=False,
            )
            return self.state

        if eta_seconds is not None:
            if (
                isinstance(eta_seconds, bool)
                or not isinstance(eta_seconds, (int, float))
                or not math.isfinite(eta_seconds)
                or eta_seconds < 0
            ):
                self.state = ControllerState.SAFE_FAILURE
                return self.state

        if (
            ambulance_available
            and eta_seconds is not None
            and eta_seconds <= PRIORITY_ETA_THRESHOLD
        ):
            self.state = determine_next_state(
                current_state=self.state,
                ambulance_available=True,
                eta_seconds=eta_seconds,
                telemetry_valid=True,
            )

        return self.state
