import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from hausdorff_match.core import HausdorffMatch


def main():
    module = HausdorffMatch()
    data = {
    "known_signature_hits": 6,
    "fuzzy_match_ratio": 0.84,
    "variant_clusters": 2,
    "collision_suspected": False,
}
    result = module.analyze(signature_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
