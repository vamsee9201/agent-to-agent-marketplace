"""UI configuration for A2A Marketplace."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class VendorConfig:
    """Configuration for a vendor display."""
    name: str
    emoji: str
    framework: str
    color: str


# Vendor configurations
VENDORS = {
    "restaurant": VendorConfig(
        name="Restaurant",
        emoji="🍕",
        framework="LangGraph",
        color="#FF6B6B",
    ),
    "electronics": VendorConfig(
        name="Electronics",
        emoji="📱",
        framework="CrewAI",
        color="#4ECDC4",
    ),
    "travel": VendorConfig(
        name="Travel",
        emoji="✈️",
        framework="ADK",
        color="#45B7D1",
    ),
}


def get_vendor_config(vendor_name: str) -> VendorConfig:
    """Get vendor config by name (case-insensitive partial match)."""
    vendor_name_lower = vendor_name.lower()
    for key, config in VENDORS.items():
        if key in vendor_name_lower or vendor_name_lower in key:
            return config
    # Return default config if not found
    return VendorConfig(
        name=vendor_name,
        emoji="📦",
        framework="Unknown",
        color="#888888",
    )


# UI Layout settings
LAYOUT = {
    "left_panel_ratio": 1,
    "right_panel_ratio": 1,
}

# Theme colors
COLORS = {
    "background": "#0E1117",
    "secondary": "#1E1E1E",
    "accent": "#FF6B6B",
    "success": "#00D26A",
    "error": "#FF4B4B",
    "text": "#FAFAFA",
    "text_muted": "#888888",
}

# A2A Protocol field descriptions for tooltips
A2A_FIELD_DESCRIPTIONS = {
    "jsonrpc": "JSON-RPC protocol version (always '2.0')",
    "method": "The A2A method being called (e.g., 'message/send')",
    "id": "Unique request identifier for matching responses",
    "params": "Method parameters containing the message and configuration",
    "params.message": "The message being sent to the vendor agent",
    "params.message.role": "Message role ('user' for client messages)",
    "params.message.parts": "Message content parts (text, data, etc.)",
    "params.configuration": "Request configuration options",
    "params.configuration.acceptedOutputModes": "Output formats the client accepts",
    "result": "The response from the vendor agent",
    "result.status": "Task status information",
    "result.status.state": "Current state (working, completed, failed)",
    "result.status.message": "Status message from the agent",
    "result.artifacts": "Output artifacts from the agent",
    "error": "Error information if the request failed",
}
