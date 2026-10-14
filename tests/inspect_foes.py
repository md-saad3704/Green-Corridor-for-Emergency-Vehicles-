
import traci

from backend.config import SUMO_BINARY

CONFIG_FILE = "simulation/intersection.sumocfg"


def main():
    traci.start([SUMO_BINARY, "-c", CONFIG_FILE])

    try:
        connections = []

        for lane_id in sorted(traci.lane.getIDList()):
            if not lane_id.startswith(":C_"):
                continue

            try:
                links = traci.lane.getLinks(lane_id)
            except traci.TraCIException:
                continue

            for link in links:
                if len(link) < 1:
                    continue

                outgoing_lane = link[0]
                if not outgoing_lane:
                    continue

                connections.append((lane_id, outgoing_lane))

        print("Internal-lane connections:", len(connections))

        for from_lane, to_lane in connections:
            print(f"\nConnection: {from_lane} -> {to_lane}")

            try:
                foes = traci.lane.getFoes(from_lane, to_lane)
                print("  Foes:", foes)
            except (traci.TraCIException, TypeError) as error:
                print("  Foes unavailable:", error)

    finally:
        traci.close()


if __name__ == "__main__":
    main()
