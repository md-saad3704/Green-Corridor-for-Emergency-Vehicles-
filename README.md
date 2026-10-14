# AI-Powered Predictive Green Corridor System for Emergency Vehicles

A simulation-based system designed to explore how traffic conditions, ambulance ETA prediction, and intelligent traffic-signal prioritization can help emergency vehicles cross intersections more efficiently.

The project uses **SUMO** for traffic simulation, **Python and TraCI** for simulation interaction, and a test-driven backend architecture. A React dashboard, machine-learning ETA prediction, and computer-vision-based traffic analysis are planned development components.

> **Current status:** The SUMO intersection network and traffic scenarios are configured. Backend modules for ETA estimation, telemetry, controller state transitions, and signal-safety checks are under development. The current system is a research and simulation prototype, not a deployment-ready traffic-control system.

## Table of Contents

- [Project Objectives](#project-objectives)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation on Windows](#installation-on-windows)
- [Configure SUMO](#configure-sumo)
- [Run the Traffic Simulation](#run-the-traffic-simulation)
- [Run the Test Suite](#run-the-test-suite)
- [Project Structure](#project-structure)
- [Git and GitHub Commands](#git-and-github-commands)
- [Planned Development](#planned-development)
- [Safety Notice](#safety-notice)

## Project Objectives

- Simulate a four-way intersection with traffic approaching from four directions.
- Track a simulated ambulance and collect its position, speed, and route information.
- Estimate the ambulance's arrival time at the intersection.
- Investigate machine-learning methods for traffic-density and ETA prediction.
- Develop a rule-based traffic-signal priority controller with explicit clearance and recovery states.
- Evaluate traffic and emergency-vehicle performance using repeatable simulation experiments.
- Build a dashboard for visualizing traffic conditions and emergency-vehicle movement.
- Evaluate computer-vision methods for traffic-density estimation using recorded video.

## Technology Stack

| Component | Technology |
|---|---|
| Traffic simulation | SUMO |
| Simulation integration | Python, TraCI, sumolib |
| Backend | Python |
| ETA estimation | Python |
| Testing | pytest |
| Traffic data and analytics | Planned: Pandas, NumPy, scikit-learn |
| Computer vision | Planned: OpenCV and YOLO |
| Frontend dashboard | Planned: React, Vite, JavaScript |
| Data storage | Planned: SQLite and CSV |

## Prerequisites

Install the following before setting up the project:

1. **Python 3.12** — the current development environment uses Python 3.12.10.
2. **SUMO** — the current installation uses SUMO 1.28.0.
3. **Git** — for version control and GitHub synchronization.
4. **Visual Studio Code** — recommended for development.

The following instructions use Windows Command Prompt (CMD).

## Installation on Windows

### 1. Clone the repository

Open CMD and navigate to the directory where you want to store the project.

```bat
cd /d C:\Users\%USERNAME%\Desktop\Projects
git clone https://github.com/md-saad3704/Green-Corridor-for-Emergency-Vehicles-.git Traffic
cd Traffic
```

If you already have the project locally, skip cloning.

### 2. Create and activate a virtual environment

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
```

Confirm that Python is using the virtual environment:

```bat
python --version
where python
```

The first Python path returned by `where python` should point to the project's `.venv\Scripts\python.exe`.

### 3. Install the current development dependencies

```bat
python -m pip install --upgrade pip
python -m pip install traci==1.28.0 sumolib==1.28.0 pytest
```

TraCI and sumolib versions should match the installed SUMO version.

Additional libraries will be documented here when their use becomes part of the implemented project.

## Configure SUMO

The current Windows development setup uses this SUMO installation directory:

```text
C:\Program Files (x86)\SUMO
```

Set `SUMO_HOME` and add SUMO's executables to the current CMD session's `PATH`:

```bat
set "SUMO_HOME=C:\Program Files (x86)\SUMO"
set "PATH=%SUMO_HOME%\bin;%PATH%"
```

Verify the installation:

```bat
sumo --version
sumo-gui --version
```

These commands configure the current terminal session. Repeat them in a new CMD session when needed, or configure the environment variables permanently in Windows.

The backend configuration currently expects SUMO's `bin` and `tools` directories beneath `SUMO_HOME`.

## Run the Traffic Simulation

From the project root, with the virtual environment activated and SUMO configured, run the simulation in the terminal:

```bat
sumo -c simulation\intersection.sumocfg
```

To open the graphical simulation:

```bat
sumo-gui -c simulation\intersection.sumocfg
```

The current configuration runs a four-way intersection simulation with normal traffic flows and a simulated ambulance named `ambulance_0`.

The simulation is configured to run for 300 simulation seconds with a one-second simulation step.

## Run the Test Suite

Run all automated tests from the project root:

```bat
python -m pytest -q
```

For verbose test output:

```bat
python -m pytest -v
```

To run a particular test file:

```bat
python -m pytest tests\test_controller_transitions.py -v
```

To run the ETA tests:

```bat
python -m pytest tests\test_eta_baseline.py tests\test_eta_distance.py tests\test_eta_service.py tests\test_eta_service_unit.py -v
```

To run the signal-safety tests:

```bat
python -m pytest tests\test_signal_safety.py -v
```

The test suite previously passed **78 tests** in the development environment. Run the commands above to verify the current checkout; test results may change as the project evolves.

## Project Structure

```text
Traffic/
├── backend/
│   ├── config.py
│   ├── controller/
│   │   ├── config.py
│   │   ├── network_mapping.py
│   │   ├── signal_safety.py
│   │   ├── states.py
│   │   └── transitions.py
│   ├── eta/
│   │   ├── baseline.py
│   │   ├── distance.py
│   │   └── service.py
│   └── telemetry/
│       ├── collector.py
│       └── logger.py
├── simulation/
│   ├── intersection.sumocfg
│   ├── network/
│   │   ├── nodes.nod.xml
│   │   ├── edges.edg.xml
│   │   └── intersection.net.xml
│   └── routes/
│       └── vehicles.rou.xml
├── tests/
│   ├── test_ambulance.py
│   ├── test_ambulance_telemetry.py
│   ├── test_controller_transitions.py
│   ├── test_eta_baseline.py
│   ├── test_eta_distance.py
│   ├── test_eta_service.py
│   ├── test_intersection_geometry.py
│   ├── test_junction_request_consistency.py
│   ├── test_network_mapping.py
│   ├── test_signal_safety.py
│   └── ...
├── .gitignore
└── README.md
```

## Git and GitHub Commands

Check the working tree:

```bat
git status
```

Review changed files:

```bat
git diff
```

Stage the README:

```bat
git add README.md
```

Commit the change:

```bat
git commit -m "docs: add project README and setup instructions"
```

Push the commit to GitHub:

```bat
git push
```

Because the local `main` branch already tracks `origin/main`, `git push` is sufficient.

After making further changes, the usual workflow is:

```bat
git status
git add <file-or-folder>
git commit -m "Describe the change"
git push
```

Replace `<file-or-folder>` with the files or folders you intend to stage. Review the staged changes before committing.

## Planned Development

The next development milestones are:

1. Validate SUMO network geometry and vehicle routes.
2. Integrate TraCI telemetry for the ambulance and surrounding traffic.
3. Improve route-aware ambulance ETA estimation and test edge cases.
4. Develop and evaluate traffic-density and ETA prediction models.
5. Implement and test safe signal-priority transitions, including yellow and all-red clearance.
6. Integrate the simulation, telemetry, prediction, and controller.
7. Develop a React dashboard for monitoring and visualization.
8. Evaluate the system using repeatable baseline and priority-control scenarios.

## Safety Notice

This project is intended for academic research and simulation. It does not control real traffic infrastructure. Any future real-world application would require traffic-engineering validation, formal safety analysis, regulatory approval, and appropriate hardware and operational safeguards.
