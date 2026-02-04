#!/bin/bash

# Start only vendor servers (without the concierge)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "Starting vendor servers..."

# Start vendors in background
python -m vendors.restaurant &
RESTAURANT_PID=$!
echo "Restaurant started (PID: $RESTAURANT_PID)"

python -m vendors.electronics &
ELECTRONICS_PID=$!
echo "Electronics started (PID: $ELECTRONICS_PID)"

python -m vendors.travel &
TRAVEL_PID=$!
echo "Travel started (PID: $TRAVEL_PID)"

echo ""
echo "All vendors started. PIDs:"
echo "  Restaurant: $RESTAURANT_PID"
echo "  Electronics: $ELECTRONICS_PID"
echo "  Travel: $TRAVEL_PID"
echo ""
echo "Press Ctrl+C to stop all vendors..."

# Wait for any process to exit
wait

# Cleanup on exit
trap "kill $RESTAURANT_PID $ELECTRONICS_PID $TRAVEL_PID 2>/dev/null" EXIT
