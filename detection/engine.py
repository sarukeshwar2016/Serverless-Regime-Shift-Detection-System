"""
Detection engine — runs regime-shift detection on windowed data
using the ruptures (offline) and river (online) libraries.
"""

from typing import Any, Dict, List, Optional

import numpy as np
import ruptures
from river import drift


class DetectionEngine:
    """Detects regime shifts in financial time-series data."""

    def __init__(self, penalty: float = 3.0):
        self.penalty = penalty
        # Online drift detector (ADWIN from river)
        self.online_detector = drift.ADWIN()

    # ── Offline detection with ruptures ──────────────────────────
    def detect_offline(self, prices: List[float], model: str = "l2", min_size: int = 5) -> Dict[str, Any]:
        """
        Run offline change-point detection on a completed price window.
        Returns breakpoints and segment metadata.
        """
        signal = np.array(prices)
        algo = ruptures.Pelt(model=model, min_size=min_size).fit(signal)
        breakpoints = algo.predict(pen=self.penalty)
        return {
            "method": "ruptures_pelt",
            "model": model,
            "penalty": self.penalty,
            "breakpoints": breakpoints,
            "n_changepoints": len(breakpoints) - 1,  # last element is signal length
            "signal_length": len(signal),
        }

    # ── Online detection with river ─────────────────────────────
    def detect_online(self, value: float) -> Optional[Dict[str, Any]]:
        """
        Feed a single value into the online drift detector.
        Returns a result dict when drift is detected, else None.
        """
        self.online_detector.update(value)
        if self.online_detector.drift_detected:
            return {
                "method": "river_adwin",
                "drift_detected": True,
                "value": value,
            }
        return None

    def reset_online(self) -> None:
        """Reset the online detector state."""
        self.online_detector = drift.ADWIN()
