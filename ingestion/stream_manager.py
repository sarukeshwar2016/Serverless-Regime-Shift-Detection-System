"""
Stream manager — orchestrates multiple adapters and feeds data
into the window builder for regime-shift detection.
"""

import threading
from typing import Dict, List

from .adapters.base_adapter import BaseAdapter
from .window_builder import WindowBuilder


class StreamManager:
    """Manages multiple data-source adapters and feeds a shared WindowBuilder."""

    def __init__(self, window_builder: WindowBuilder):
        self.window_builder = window_builder
        self._adapters: Dict[str, BaseAdapter] = {}
        self._threads: List[threading.Thread] = []
        self._running = False

    def register(self, adapter: BaseAdapter) -> None:
        """Register a data-source adapter."""
        self._adapters[adapter.name] = adapter
        print(f"[StreamManager] Registered adapter: {adapter.name}")

    def _run_adapter(self, adapter: BaseAdapter) -> None:
        """Internal: run a single adapter's stream loop."""
        try:
            for record in adapter.stream():
                if not self._running:
                    break
                self.window_builder.add(record)
        except Exception as exc:
            print(f"[StreamManager] Error in {adapter.name}: {exc}")

    def start(self) -> None:
        """Start streaming from all registered adapters in background threads."""
        self._running = True
        for adapter in self._adapters.values():
            t = threading.Thread(target=self._run_adapter, args=(adapter,), daemon=True)
            t.start()
            self._threads.append(t)
        print(f"[StreamManager] Started {len(self._threads)} stream(s)")

    def stop(self) -> None:
        """Stop all streams and disconnect adapters."""
        self._running = False
        for adapter in self._adapters.values():
            adapter.disconnect()
        for t in self._threads:
            t.join(timeout=5)
        self._threads.clear()
        print("[StreamManager] All streams stopped")
