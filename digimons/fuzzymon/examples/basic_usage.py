"""
Basic usage example for fuzzymon
"""

import sys
sys.path.insert(0, '../src')

from fuzzymon.core import Fuzzymon
from fuzzymon.utils import setup_logging


def main():
    setup_logging(level="INFO")
    digimon = Fuzzymon()
    
    print("=== Digimon Info ===")
    info = digimon.get_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    print("\n=== Validation Test ===")
    is_valid = digimon.validate({"test": "data"})
    print(f"Data valid: {is_valid}")
    
    print("\n=== Running Analysis ===")
    result = digimon.analyze()
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
