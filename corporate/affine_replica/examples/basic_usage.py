import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from affine_replica.core import AffineReplica


def main():
    module = AffineReplica()
    data = {
    "api_sequence_similarity": 0.88,
    "syscall_profile_risk": 0.73,
    "evasion_signals": 3,
    "payload_stage_count": 2,
}
    result = module.analyze(execution_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
