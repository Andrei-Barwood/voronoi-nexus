import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from minkowski_unpack.core import MinkowskiUnpack


def main():
    module = MinkowskiUnpack()
    data = {
    "section_entropy": 7.9,
    "suspicious_stub_detected": True,
    "runtime_unpack_behavior": True,
    "overlay_size_kb": 620,
}
    result = module.analyze(binary_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
