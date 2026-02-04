#!/usr/bin/env python3
"""Demo script showcasing A2A Marketplace conversations."""

import asyncio
import httpx
import json
from typing import Optional


async def check_vendor_health(url: str) -> bool:
    """Check if a vendor is healthy."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{url}/.well-known/agent.json")
            return response.status_code == 200
    except Exception:
        return False


async def send_a2a_message(url: str, message: str) -> Optional[str]:
    """Send a message to a vendor via A2A protocol."""
    import uuid

    payload = {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": message}]
            },
            "configuration": {
                "acceptedOutputModes": ["text"]
            }
        },
        "id": str(uuid.uuid4())
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                # Extract response text
                if "result" in result:
                    task = result["result"]
                    if "status" in task and "message" in task["status"]:
                        parts = task["status"]["message"].get("parts", [])
                        texts = [p.get("text", "") for p in parts if "text" in p]
                        return " ".join(texts)
                return json.dumps(result, indent=2)
            else:
                return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"


async def demo_vendor_direct():
    """Demo direct communication with vendors."""
    print("\n" + "=" * 60)
    print("  Demo: Direct Vendor Communication")
    print("=" * 60)

    vendors = [
        ("Restaurant", "http://localhost:10001"),
        ("Electronics", "http://localhost:10002"),
        ("Travel", "http://localhost:10003"),
    ]

    # Check health
    print("\n1. Checking vendor health...")
    for name, url in vendors:
        healthy = await check_vendor_health(url)
        status = "✓ Online" if healthy else "✗ Offline"
        print(f"   {name}: {status}")

    # Demo queries
    demo_queries = [
        ("http://localhost:10001", "Show me your pizza options"),
        ("http://localhost:10002", "What laptops do you have?"),
        ("http://localhost:10003", "Tell me about Paris"),
    ]

    print("\n2. Sending demo queries...")
    for url, query in demo_queries:
        vendor = url.split(":")[2]
        print(f"\n   Query to port {vendor}: \"{query}\"")
        response = await send_a2a_message(url, query)
        if response:
            # Truncate long responses
            if len(response) > 500:
                response = response[:500] + "..."
            print(f"   Response: {response}")


async def demo_restaurant():
    """Demo restaurant vendor interactions."""
    print("\n" + "=" * 60)
    print("  Demo: Restaurant Vendor (LangGraph)")
    print("=" * 60)

    url = "http://localhost:10001"

    if not await check_vendor_health(url):
        print("\n⚠️  Restaurant vendor is not running. Start it with:")
        print("   python -m vendors.restaurant")
        return

    queries = [
        "What categories are on your menu?",
        "Show me your pasta dishes",
        "What vegetarian options do you have?",
        "Tell me about the Margherita pizza",
    ]

    for query in queries:
        print(f"\n> {query}")
        response = await send_a2a_message(url, query)
        print(f"< {response[:500]}..." if len(response) > 500 else f"< {response}")
        await asyncio.sleep(1)


async def demo_electronics():
    """Demo electronics vendor interactions."""
    print("\n" + "=" * 60)
    print("  Demo: Electronics Vendor (CrewAI)")
    print("=" * 60)

    url = "http://localhost:10002"

    if not await check_vendor_health(url):
        print("\n⚠️  Electronics vendor is not running. Start it with:")
        print("   python -m vendors.electronics")
        return

    queries = [
        "What product categories do you have?",
        "Show me your laptop options",
        "Compare the MacBook Pro and ThinkPad",
        "Is the Dell XPS 15 in stock?",
    ]

    for query in queries:
        print(f"\n> {query}")
        response = await send_a2a_message(url, query)
        print(f"< {response[:500]}..." if len(response) > 500 else f"< {response}")
        await asyncio.sleep(1)


async def demo_travel():
    """Demo travel vendor interactions."""
    print("\n" + "=" * 60)
    print("  Demo: Travel Vendor (ADK)")
    print("=" * 60)

    url = "http://localhost:10003"

    if not await check_vendor_health(url):
        print("\n⚠️  Travel vendor is not running. Start it with:")
        print("   python -m vendors.travel")
        return

    queries = [
        "What destinations are available?",
        "Tell me about Tokyo",
        "Show me flights to Paris",
        "What hotels are in Bali?",
        "Do you have any package deals?",
    ]

    for query in queries:
        print(f"\n> {query}")
        response = await send_a2a_message(url, query)
        print(f"< {response[:500]}..." if len(response) > 500 else f"< {response}")
        await asyncio.sleep(1)


async def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("  A2A Marketplace Demo")
    print("=" * 60)
    print("\nThis demo shows direct communication with vendor agents.")
    print("Make sure all vendors are running before proceeding.")

    # Quick health check
    all_healthy = True
    for url in ["http://localhost:10001", "http://localhost:10002", "http://localhost:10003"]:
        if not await check_vendor_health(url):
            all_healthy = False
            break

    if not all_healthy:
        print("\n⚠️  Not all vendors are running. Start them with:")
        print("   ./scripts/start_vendors.sh")
        print("\nOr start individually:")
        print("   python -m vendors.restaurant   # Port 10001")
        print("   python -m vendors.electronics  # Port 10002")
        print("   python -m vendors.travel       # Port 10003")
        return

    # Run demos
    await demo_vendor_direct()

    print("\n\nTo run individual vendor demos:")
    print("  demo_restaurant()")
    print("  demo_electronics()")
    print("  demo_travel()")

    print("\nTo start the interactive concierge:")
    print("  python -m concierge")


if __name__ == "__main__":
    asyncio.run(main())
