import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from helly_rules.core import HellyRules


def main():
    module = HellyRules()
    data = {
    "rules_compiled": 24,
    "syntax_errors": 0,
    "high_confidence_matches": 3,
    "suspicious_strings_detected": 11,
}
    result = module.analyze(rule_data=data)
    print(result.model_dump())


if __name__ == "__main__":
    main()
