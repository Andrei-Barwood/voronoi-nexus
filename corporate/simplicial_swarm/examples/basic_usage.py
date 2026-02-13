import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from simplicial_swarm.core import SimplicialSwarm


def main():
    module = SimplicialSwarm()
    data = {
    "c2_contact_attempts": 15,
    "peer_fanout": 22,
    "domain_flux_detected": True,
    "synchronized_beacons": True,
}
    result = module.analyze(traffic_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
