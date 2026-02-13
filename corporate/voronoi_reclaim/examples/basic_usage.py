import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from voronoi_reclaim.core import VoronoiReclaim


def main():
    module = VoronoiReclaim()
    data = {
    "mass_file_changes": 180,
    "entropy_spike": True,
    "shadow_copy_deleted": True,
    "suspicious_extension_ratio": 0.62,
}
    result = module.analyze(event_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
