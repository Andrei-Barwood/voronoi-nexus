import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from delaunay_sentinel.core import DelaunaySentinel


def main():
    module = DelaunaySentinel()
    data = {
    "suspicious_imports": 9,
    "packed_binary": True,
    "network_callbacks": 5,
    "anti_vm_checks": True,
}
    result = module.analyze(sample_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
