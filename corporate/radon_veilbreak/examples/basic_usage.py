import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from radon_veilbreak.core import RadonVeilbreak


def main():
    module = RadonVeilbreak()
    data = {
    "lsb_irregularity_score": 0.81,
    "container_mismatch": True,
    "payload_signature_hits": 3,
    "metadata_anomaly": True,
}
    result = module.analyze(artifact_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
