import math
from typing import Any

from backend.controller.clearance import build_clearance_plan


class ClearanceManager:
    """Track clearance stages using simulation time only."""

    def __init__(self) -> None:
        self._plan: dict[str, Any] | None = None
        self._stage = "idle"
        self._stage_started_at: float | None = None

    @property
    def stage(self) -> str:
        return self._stage

    @staticmethod
    def _validate_time(simulation_time: float) -> float:
        if (
            isinstance(simulation_time, bool)
            or not isinstance(simulation_time, (int, float))
            or not math.isfinite(simulation_time)
            or simulation_time < 0
        ):
            raise ValueError("Simulation time must be a finite, non-negative number.")

        return float(simulation_time)

    def start(
        self,
        current_signal_state: str,
        expected_length: int,
        simulation_time: float,
    ) -> str:
        """Start a new clearance sequence."""
        if self._stage not in {"idle", "complete"}:
            raise RuntimeError("A clearance sequence is already active.")

        start_time = self._validate_time(simulation_time)
        plan = build_clearance_plan(
            current_signal_state,
            expected_length,
        )

        self._plan = plan
        self._stage = "yellow"
        self._stage_started_at = start_time

        return plan["yellow_state"]

    @property
    def current_signal_state(self) -> str | None:
        if self._plan is None:
            return None

        if self._stage == "yellow":
            return self._plan["yellow_state"]

        if self._stage in {"all_red", "complete"}:
            return self._plan["all_red_state"]

        return None

    def update(self, simulation_time: float) -> str:
        """Advance clearance stages using simulation time."""
        now = self._validate_time(simulation_time)

        if self._stage in {"idle", "complete"}:
            return self._stage

        plan = self._plan
        stage_started_at = self._stage_started_at

        if plan is None or stage_started_at is None:
            raise RuntimeError("Clearance manager state is inconsistent.")

        if now < stage_started_at:
            raise ValueError("Simulation time cannot move backwards.")

        elapsed = now - stage_started_at

        if self._stage == "yellow":
            yellow_duration = plan["yellow_duration_seconds"]

            if elapsed >= yellow_duration:
                self._stage = "all_red"
                # Start the all-red duration when that stage is applied.
                self._stage_started_at = now
                return self._stage

        elif self._stage == "all_red":
            all_red_duration = plan["all_red_duration_seconds"]

            if elapsed >= all_red_duration:
                self._stage = "complete"

        return self._stage
