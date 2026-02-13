import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from geodesic_pursuit.core import GeodesicPursuit


def main():
    module = GeodesicPursuit()
    data = {
    "lateral_movement_events": 7,
    "privilege_escalations": 2,
    "beaconing_detected": True,
    "dwell_time_days": 24,
}
    result = module.analyze(telemetry_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
