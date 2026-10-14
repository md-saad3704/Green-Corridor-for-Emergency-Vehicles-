
import csv
from pathlib import Path

from backend.config import PROJECT_ROOT

RESULTS_DIR = PROJECT_ROOT / "results"
CSV_FILE = RESULTS_DIR / "traffic_telemetry.csv"

FIELDNAMES = [
    "simulation_time",
    "vehicle_id",
    "edge_id",
    "lane_id",
    "position_x",
    "position_y",
    "speed_mps",
    "waiting_time",
    "vehicle_type",
]


def initialize_log():
    """Create the results directory and start a fresh CSV log."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()


def log_snapshot(snapshot):
    """Append one telemetry snapshot to the CSV file."""
    with CSV_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        for vehicle in snapshot["vehicles"]:
            writer.writerow({
                "simulation_time": snapshot["simulation_time"],
                **vehicle,
            })

    return CSV_FILE
