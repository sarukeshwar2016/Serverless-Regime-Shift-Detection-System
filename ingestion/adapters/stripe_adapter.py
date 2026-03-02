"""
Stripe payment event adapter.
Polls Stripe for recent payment events and yields them.
"""

import os
from typing import Any, Dict, Generator

import stripe
from dotenv import load_dotenv

from .base_adapter import BaseAdapter

load_dotenv()


class StripeAdapter(BaseAdapter):
    """Adapter for Stripe payment events."""

    def __init__(self):
        super().__init__(name="stripe")
        stripe.api_key = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    def connect(self) -> None:
        """Validate the Stripe API key."""
        self.is_connected = True
        print(f"[{self.name}] Stripe adapter ready")

    def disconnect(self) -> None:
        """Mark the adapter as disconnected."""
        self.is_connected = False
        print(f"[{self.name}] Disconnected")

    def stream(self) -> Generator[Dict[str, Any], None, None]:
        """Yield recent Stripe payment events."""
        if not self.is_connected:
            self.connect()
        events = stripe.Event.list(limit=100)
        for event in events.auto_paging_iter():
            yield {
                "source": self.name,
                "event_type": event.type,
                "amount": event.data.object.get("amount", 0) if hasattr(event.data, "object") else 0,
                "currency": event.data.object.get("currency", "usd") if hasattr(event.data, "object") else "usd",
                "timestamp": event.created,
            }
