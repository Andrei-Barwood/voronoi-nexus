#!/bin/bash

echo "=== thirstmon Demo ==="
echo ""

cd "$(dirname "$0")/.."

echo "1. Installing dependencies..."
pip install -e . -q

echo ""
echo "2. Running basic usage example..."
python examples/basic_usage.py

echo ""
echo "3. Running tests..."
pytest tests/ -q

echo ""
echo "✓ Demo complete!"
