
import traci

from backend.config import SUMO_BINARY, PROJECT_ROOT

CONFIG_FILE = PROJECT_ROOT / "simulation" / "intersection.sumocfg"


def main():
    traci.start([
        SUMO_BINARY,
        "-c",
        str(CONFIG_FILE),
        "--no-step-log",
        "true",
    ])

    try:
        # Advance the simulation so vehicles and the signal are active.
        for _ in range(10):
            traci.simulationStep()

        tls_id = "C"

        print("\n=== TRAFFIC LIGHT ===")
        print("Traffic light IDs:", traci.trafficlight.getIDList())
        print("Signal ID:", tls_id)
        print("Current state:", traci.trafficlight.getRedYellowGreenState(tls_id))
        print("Active program:", traci.trafficlight.getProgram(tls_id))

        print("\n=== CONTROLLED MOVEMENTS ===")
        controlled_links = traci.trafficlight.getControlledLinks(tls_id)

        for signal_index, link_group in enumerate(controlled_links):
            print(f"\nSignal index {signal_index}:")
            for incoming_lane, outgoing_lane, via_lane in link_group:
                print(
                    f"  {incoming_lane} -> {outgoing_lane}"
                    f" | internal lane: {via_lane}"
                )

        print("\n=== CURRENT PHASE ===")
        print("Phase index:", traci.trafficlight.getPhase(tls_id))
        print("Phase duration remaining:", traci.trafficlight.getNextSwitch(tls_id) - traci.simulation.getTime())

        
        print("\n=== ALL SIGNAL PROGRAM PHASES ===")
        programs = traci.trafficlight.getAllProgramLogics(tls_id)

        for program in programs:
            print(f"\nProgram ID: {program.programID}")
            print(f"Program type: {program.type}")

            for phase_index, phase in enumerate(program.phases):
                print(
                    f"Phase {phase_index}: "
                    f"duration={phase.duration}s, "
                    f"state={phase.state}"
                )

    finally:
        traci.close()


if __name__ == "__main__":
    main()
