"""
Window builder — collects streaming data into fixed-size time windows
for downstream analysis by the detection engine.
"""

import time
import numpy as np
from collections import deque, defaultdict
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

    def get_windows(self) -> List[Dict[str, Any]]:
        """Return aggregated windows grouped by source and asset."""
        cutoff = time.time() - self.window_seconds
        valid_points = [p for p in self._buffer if p.get("_ingested_at", 0) >= cutoff]
        
        grouped = defaultdict(list)
        for p in valid_points:
            source = p.get("source", "unknown")
            asset = p.get("symbol") or p.get("event_type") or "unknown"
            grouped[(source, asset)].append(p)
            
        windows = []
        window_end = time.time()
        window_start = window_end - self.window_seconds
        
        for (source, asset), points in grouped.items():
            if source == "binance":
                values = [p.get("price", 0.0) for p in points]
                asset_class = "crypto"
            elif source == "stripe":
                values = [p.get("amount", 0.0) for p in points]
                asset_class = "payments"
            else:
                values = [p.get("value", 0.0) for p in points]
                asset_class = "unknown"
                
            mean_val = np.mean(values) if values else 0.0
            if len(values) > 1 and values[0] != 0:
                change_pct = ((values[-1] - values[0]) / values[0]) * 100
            else:
                change_pct = 0.0
                
            compression_tier = "STABLE" if abs(change_pct) < 5.0 else "STRESSED"
            
            windows.append({
                "source": source,
                "asset": asset,
                "asset_class": asset_class,
                "window_start": window_start,
                "window_end": window_end,
                "values": values,
                "mean_value": float(mean_val),
                "value_change_pct": float(change_pct),
                "event_count": len(points),
                "compression_tier": compression_tier
            })
            
        return windows

    def clear(self) -> None:
        """Clear the buffer."""
        self._buffer.clear()

    @property
    def size(self) -> int:
        return len(self._buffer)
