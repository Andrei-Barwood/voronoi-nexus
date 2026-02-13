import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from kuratowski_forge.core import KuratowskiForge


def main():
    module = KuratowskiForge()
    data = {
    "indirect_jumps": 37,
    "opaque_predicates": 8,
    "control_flow_anomalies": 5,
    "anti_disassembly_tricks": True,
}
    result = module.analyze(binary_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
