"""
Window builder — collects streaming data into fixed-size time windows
for downstream analysis by the detection engine.
"""

import time
from collections import deque
from typing import Any, Dict, List


class WindowBuilder:
    """Collects data points into time-based windows."""

    def __init__(self, window_seconds: int = 60, max_points: int = 10_000):
        self.window_seconds = window_seconds
        self.max_points = max_points
        self._buffer: deque = deque(maxlen=max_points)

    def add(self, data_point: Dict[str, Any]) -> None:
        """Add a data point with the current timestamp."""
        data_point.setdefault("_ingested_at", time.time())
        self._buffer.append(data_point)

    def get_window(self) -> List[Dict[str, Any]]:
        """Return all data points within the current time window."""
        cutoff = time.time() - self.window_seconds
        return [p for p in self._buffer if p.get("_ingested_at", 0) >= cutoff]

    def clear(self) -> None:
        """Clear the buffer."""
        self._buffer.clear()

    @property
    def size(self) -> int:
        return len(self._buffer)
