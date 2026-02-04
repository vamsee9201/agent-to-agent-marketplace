"""Entry point for the Purchasing Concierge."""

import asyncio
from dotenv import load_dotenv

from .agent import interactive_session
from .discovery import get_registry

load_dotenv()


async def main():
    """Main entry point."""
    print("Initializing Purchasing Concierge...")

    # Discover vendors
    print("Discovering available vendors...")
    registry = await get_registry()

    if not registry.vendors:
        print("\n⚠️  No vendors discovered. Make sure vendor servers are running:")
        print("   python -m vendors.restaurant  (port 10001)")
        print("   python -m vendors.electronics  (port 10002)")
        print("   python -m vendors.travel  (port 10003)")
        print("\nStarting anyway - vendors can be discovered later.\n")
    else:
        print(f"✓ Found {len(registry.vendors)} vendor(s)")
        for vendor in registry.vendors.values():
            print(f"  • {vendor.name}")

    # Start interactive session
    await interactive_session()


if __name__ == "__main__":
    asyncio.run(main())
