import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from persistent_nerve.core import PersistentNerve


def main():
    module = PersistentNerve()
    data = {
    "anomalous_process_tree": True,
    "credential_access_attempts": 4,
    "living_off_the_land_score": 0.79,
    "data_staging_events": 3,
}
    result = module.analyze(behavior_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
