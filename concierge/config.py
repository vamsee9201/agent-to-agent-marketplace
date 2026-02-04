"""Configuration for the Purchasing Concierge."""

import os
from dotenv import load_dotenv

load_dotenv()

# Vendor URLs
VENDOR_URLS = [
    "http://localhost:10001",  # Restaurant (LangGraph)
    "http://localhost:10002",  # Electronics (CrewAI)
    "http://localhost:10003",  # Travel (ADK)
]

# API configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Model configuration
MODEL_NAME = "gemini-2.0-flash"

# Timeouts (in seconds)
DISCOVERY_TIMEOUT = 10
REQUEST_TIMEOUT = 60
HEALTH_CHECK_TIMEOUT = 5
