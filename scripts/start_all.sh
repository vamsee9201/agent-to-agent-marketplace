#!/bin/bash

# Start all vendor servers for the A2A Marketplace

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "================================================"
echo "  A2A Marketplace - Starting All Services"
echo "================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to start a vendor in the background
start_vendor() {
    local name=$1
    local module=$2
    local port=$3

    echo -e "${YELLOW}Starting $name on port $port...${NC}"
    python -m $module &
    local pid=$!
    echo "  PID: $pid"
    sleep 1
}

# Start all vendors
echo "Starting vendor agents..."
echo ""

start_vendor "Restaurant (LangGraph)" "vendors.restaurant" "10001"
start_vendor "Electronics (CrewAI)" "vendors.electronics" "10002"
start_vendor "Travel (ADK)" "vendors.travel" "10003"

echo ""
echo -e "${GREEN}All vendors started!${NC}"
echo ""
echo "Vendor endpoints:"
echo "  Restaurant:  http://localhost:10001"
echo "  Electronics: http://localhost:10002"
echo "  Travel:      http://localhost:10003"
echo ""
echo "Waiting for services to be ready..."
sleep 3

# Check health of each vendor
echo ""
echo "Checking vendor health..."
for port in 10001 10002 10003; do
    if curl -s "http://localhost:$port/.well-known/agent.json" > /dev/null 2>&1; then
        echo -e "  Port $port: ${GREEN}OK${NC}"
    else
        echo -e "  Port $port: ${YELLOW}Not responding yet${NC}"
    fi
done

echo ""
echo "================================================"
echo "  Starting Purchasing Concierge"
echo "================================================"
echo ""

# Start the concierge (foreground)
python -m concierge
