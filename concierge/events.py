"""Event types for UI integration with the Purchasing Concierge."""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Callable, Any


class EventType(Enum):
    """Types of events emitted during concierge processing."""
    PROCESSING_START = "processing_start"
    TOOL_CALL_START = "tool_call_start"
    TOOL_CALL_END = "tool_call_end"
    VENDOR_QUERY_START = "vendor_query_start"
    VENDOR_QUERY_END = "vendor_query_end"
    A2A_REQUEST = "a2a_request"
    A2A_RESPONSE = "a2a_response"
    RESPONSE_CHUNK = "response_chunk"
    RESPONSE_COMPLETE = "response_complete"
    ERROR = "error"


@dataclass
class UIEvent:
    """An event emitted for UI updates."""
    type: EventType
    timestamp: datetime = field(default_factory=datetime.now)
    data: dict = field(default_factory=dict)
    vendor_name: Optional[str] = None
    duration_ms: Optional[float] = None
    raw_json: Optional[str] = None
    message: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert event to dictionary for serialization."""
        return {
            "type": self.type.value,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "vendor_name": self.vendor_name,
            "duration_ms": self.duration_ms,
            "raw_json": self.raw_json,
            "message": self.message,
        }


# Type alias for event callback function
EventCallback = Callable[[UIEvent], Any]


def create_event(
    event_type: EventType,
    vendor_name: Optional[str] = None,
    duration_ms: Optional[float] = None,
    raw_json: Optional[str] = None,
    message: Optional[str] = None,
    **data
) -> UIEvent:
    """Create a new UI event with the given parameters."""
    return UIEvent(
        type=event_type,
        vendor_name=vendor_name,
        duration_ms=duration_ms,
        raw_json=raw_json,
        message=message,
        data=data,
    )
