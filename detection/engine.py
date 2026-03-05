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

    def classify_regime(self, window: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensemble voting: both->STRESSED, one->TRANSITIONING, neither->STABLE.
        """
        values = window.get("values", [])
        pelt_triggered = False
        drift_triggered = False
        
        if len(values) >= 5:
            try:
                offline_res = self.detect_offline(values)
                pelt_triggered = offline_res.get("n_changepoints", 0) > 0
            except Exception:
                pass
            
        for v in values:
            if self.detect_online(v):
                drift_triggered = True
                break
                
        if drift_triggered:
            self.reset_online()

        if pelt_triggered and drift_triggered:
            regime = "STRESSED"
            confidence = 1.0
        elif pelt_triggered or drift_triggered:
            regime = "TRANSITIONING"
            confidence = 0.5
        else:
            regime = "STABLE"
            confidence = 1.0
            
        import time
        return {
            "source": window.get("source"),
            "asset": window.get("asset"),
            "asset_class": window.get("asset_class"),
            "regime": regime,
            "confidence": confidence,
            "pelt_triggered": pelt_triggered,
            "drift_triggered": drift_triggered,
            "mean_value": window.get("mean_value", 0.0),
            "detected_at": time.time()
        }


class RegimeTracker:
    """Suppresses false positives by requiring consecutive windows to confirm a regime change."""
    
    def __init__(self, confirmations_required: int = 3):
        self.confirmations_required = confirmations_required
        self._state: Dict[tuple, Dict[str, Any]] = {}

    def track(self, classification: Dict[str, Any]) -> str:
        """
        Takes a classification dict and returns the confirmed regime.
        """
        key = (classification.get("source"), classification.get("asset"))
        new_regime = classification.get("regime", "STABLE")
        
        if key not in self._state:
            self._state[key] = {
                "current_regime": "STABLE",
                "pending_regime": new_regime,
                "count": 1
            }
        else:
            state = self._state[key]
            if new_regime == state["pending_regime"]:
                state["count"] += 1
                if state["count"] >= self.confirmations_required:
                    state["current_regime"] = new_regime
            else:
                state["pending_regime"] = new_regime
                state["count"] = 1
                
        return self._state[key]["current_regime"]
