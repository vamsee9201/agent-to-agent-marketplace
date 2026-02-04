# Agent-to-Agent (A2A) Marketplace

A demonstration project showcasing the A2A protocol for interoperability between AI agents built on different frameworks.

## Overview

This project demonstrates how a Purchasing Concierge agent (built with ADK) can orchestrate vendor agents built on different frameworks:

- **Restaurant Vendor** (LangGraph) - Italian restaurant with menu browsing and ordering
- **Electronics Vendor** (CrewAI) - Consumer electronics with product comparison
- **Travel Vendor** (ADK) - Travel booking with flights, hotels, and packages

All agents communicate using the A2A (Agent-to-Agent) protocol, enabling seamless interoperability regardless of the underlying framework.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User (CLI/API)                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              Purchasing Concierge Agent (ADK)                   │
│  - Discovers vendors via A2A agent cards                        │
│  - Routes requests, aggregates responses                        │
│  - Manages cart state and purchase flow                         │
└─────────────────────────────────────────────────────────────────┘
         │                      │                      │
         ▼                      ▼                      ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Restaurant    │  │   Electronics   │  │  Travel Booking │
│   (LangGraph)   │  │    (CrewAI)     │  │      (ADK)      │
│   Port: 10001   │  │   Port: 10002   │  │   Port: 10003   │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -e .
```

### 2. Set Up Environment

```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 3. Start All Services

```bash
./scripts/start_all.sh
```

Or start services individually:

```bash
# Terminal 1: Restaurant vendor
python -m vendors.restaurant

# Terminal 2: Electronics vendor
python -m vendors.electronics

# Terminal 3: Travel vendor
python -m vendors.travel

# Terminal 4: Concierge
python -m concierge
```

### 4. Run Demo

```bash
python scripts/demo.py
```

## Usage Examples

Once the concierge is running, try these conversations:

```
You: What vendors are available?
Concierge: [Lists all discovered vendors]

You: Show me the restaurant menu
Concierge: [Queries restaurant vendor and shows menu]

You: I'd like to order a Margherita pizza
Concierge: [Adds pizza to cart]

You: Also search for laptops
Concierge: [Queries electronics vendor]

You: Show my cart
Concierge: [Displays cart with items from multiple vendors]

You: Checkout
Concierge: [Completes orders with each vendor]
```

## Project Structure

```
agent-to-agent-marketplace/
├── common/                     # Shared utilities
│   ├── models.py              # Pydantic models
│   └── mcp_server.py          # Base MCP server
│
├── concierge/                  # Purchasing Concierge (ADK)
│   ├── agent.py               # Main concierge agent
│   ├── discovery.py           # Vendor discovery
│   ├── cart.py                # Cart management
│   └── config.py              # Configuration
│
├── vendors/
│   ├── restaurant/            # LangGraph vendor
│   │   ├── agent.py          # LangGraph agent
│   │   ├── data.py           # Mock menu data
│   │   └── mcp_server.py     # Menu data tools
│   │
│   ├── electronics/           # CrewAI vendor
│   │   ├── crew.py           # CrewAI crew
│   │   ├── agents.py         # CrewAI agents
│   │   └── data.py           # Mock product data
│   │
│   └── travel/                # ADK vendor
│       ├── agent.py          # ADK agent
│       ├── data.py           # Mock travel data
│       └── mcp_server.py     # Travel data tools
│
├── scripts/
│   ├── start_all.sh          # Start all services
│   └── demo.py               # Demo script
│
└── tests/                     # Test suite
```

## Vendor Capabilities

### Restaurant (Port 10001)
- Browse menu by category
- Search dishes
- Get recommendations (dietary preferences)
- Place orders

### Electronics (Port 10002)
- Browse products by category
- Compare products
- Check availability
- Purchase products

### Travel (Port 10003)
- Search destinations
- Search flights
- Search hotels
- Get package deals
- Get travel quotes

## A2A Protocol

Each vendor exposes an agent card at `/.well-known/agent.json`:

```json
{
  "name": "Vendor Name",
  "description": "Vendor description",
  "url": "http://localhost:10001",
  "skills": [
    {
      "id": "skill_id",
      "name": "Skill Name",
      "description": "What this skill does"
    }
  ],
  "capabilities": {
    "streaming": false,
    "pushNotifications": false
  }
}
```

## Testing

```bash
pytest tests/
```

## Dependencies

- `google-adk` - Google Agent Development Kit
- `a2a-sdk` - A2A Protocol SDK
- `langgraph` - LangGraph framework
- `crewai` - CrewAI framework
- `mcp` - Model Context Protocol
- `uvicorn` - ASGI server

## License

MIT
