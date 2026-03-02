"""
Binance WebSocket adapter for live cryptocurrency trade data.
Connects to the Binance streaming API and yields trade events.
"""

import json
import os
from typing import Any, Dict, Generator

from dotenv import load_dotenv

from .base_adapter import BaseAdapter

load_dotenv()


class BinanceAdapter(BaseAdapter):
    """Adapter for the Binance WebSocket trade stream."""

    def __init__(self):
        super().__init__(name="binance")
        self.url = os.getenv(
            "BINANCE_STREAM_URL",
            "wss://stream.binance.com:9443/ws/btcusdt@trade",
        )
        self._ws = None

    def connect(self) -> None:
        """Open a WebSocket connection to Binance."""
        import websocket

        self._ws = websocket.create_connection(self.url)
        self.is_connected = True
        print(f"[{self.name}] Connected to {self.url}")

    def disconnect(self) -> None:
        """Close the WebSocket connection."""
        if self._ws:
            self._ws.close()
        self.is_connected = False
        print(f"[{self.name}] Disconnected")

    def stream(self) -> Generator[Dict[str, Any], None, None]:
        """Yield trade events from the Binance stream."""
        if not self.is_connected:
            self.connect()
        while True:
            raw = self._ws.recv()
            data = json.loads(raw)
            yield {
                "source": self.name,
                "symbol": data.get("s"),
                "price": float(data.get("p", 0)),
                "quantity": float(data.get("q", 0)),
                "timestamp": data.get("T"),
            }
