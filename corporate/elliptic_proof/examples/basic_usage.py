import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from elliptic_proof.core import EllipticProof


def main():
    module = EllipticProof()
    data = {
    "deprecated_ciphers": 2,
    "weak_key_detected": True,
    "tls_misconfigurations": 4,
    "signature_validation_issues": 1,
}
    result = module.analyze(crypto_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
