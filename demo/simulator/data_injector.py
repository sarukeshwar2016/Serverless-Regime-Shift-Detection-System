"""
Data injector — feeds historical or synthetic data into the detection engine
as if it were live streaming data, for demo purposes.
"""

import time
import pandas as pd
from detection.engine import DetectionEngine


class DataInjector:
    """Replay CSV data through the detection engine at a configurable speed."""

    def __init__(self, csv_path: str, speed_multiplier: float = 10.0):
        self.csv_path = csv_path
        self.speed = speed_multiplier
        self.engine = DetectionEngine()

    def run(self) -> None:
        """Stream rows from the CSV and print regime-shift detections."""
        df = pd.read_csv(self.csv_path)
        prices = df["price"].tolist() if "price" in df.columns else df.iloc[:, 0].tolist()

        print(f"[Injector] Replaying {len(prices)} data points from {self.csv_path}")
        
        # Simulate 60-event windows to match our architecture
        window_size = 60
        for i in range(0, len(prices), window_size):
            chunk = prices[i:i+window_size]
            
            # Format to match WindowBuilder output
            window = {
                "source": "stripe",
                "asset": "charge",
                "asset_class": "payments",
                "values": chunk,
                "mean_value": sum(chunk) / len(chunk) if chunk else 0.0
            }
            
            # Feed window into the ensemble classifier
            result = self.engine.classify_regime(window)
            print(f"  Window {i//window_size + 1} | Mean: ${window['mean_value']:.2f} | Regime: {result['regime']}")
            
            time.sleep(1.0 / self.speed)

        print("[Injector] Replay complete.")
        # Also run offline detection on the full window
        offline = self.engine.detect_offline(prices)
        print(f"[Injector] Offline breakpoints: {offline['breakpoints']}")
