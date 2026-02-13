import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from polytope_detonate.core import PolytopeDetonate


def main():
    module = PolytopeDetonate()
    data = {
    "process_spawn_count": 18,
    "registry_modifications": 12,
    "network_callbacks": 4,
    "persistence_attempted": True,
}
    result = module.analyze(sample_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
