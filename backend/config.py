
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SUMO_HOME = Path(
    os.environ.get(
        "SUMO_HOME",
        r"C:\Program Files (x86)\SUMO",
    )
)

SUMO_BIN = SUMO_HOME / "bin"
SUMO_TOOLS = SUMO_HOME / "tools"

if not SUMO_TOOLS.is_dir():
    raise RuntimeError(
        f"SUMO tools directory not found: {SUMO_TOOLS}"
    )

if str(SUMO_TOOLS) not in sys.path:
    sys.path.insert(0, str(SUMO_TOOLS))

SUMO_BINARY = str(SUMO_BIN / "sumo")
SUMO_GUI_BINARY = str(SUMO_BIN / "sumo-gui")

print(f"Project root: {PROJECT_ROOT}")
print(f"SUMO home: {SUMO_HOME}")
