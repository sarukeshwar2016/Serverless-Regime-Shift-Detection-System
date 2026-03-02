"""
Scenario runner — runs pre-defined demo scenarios end-to-end.
Each scenario generates data, runs detection, and prints results.
"""

import sys
import os

# Add project root to path so imports work when run standalone
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from detection.engine import DetectionEngine
from demo.simulator.shift_trigger import generate_shift_signal


def run_scenario(name: str, n: int = 500, n_shifts: int = 3) -> None:
    """Run a single named scenario."""
    print(f"\n{'='*60}")
    print(f"  Scenario: {name}")
    print(f"{'='*60}")

    signal = generate_shift_signal(n=n, n_shifts=n_shifts)
    engine = DetectionEngine()

    # Offline
    offline = engine.detect_offline(signal)
    print(f"  Offline breakpoints : {offline['breakpoints']}")
    print(f"  Change-points found : {offline['n_changepoints']}")

    # Online
    drift_count = 0
    for val in signal:
        res = engine.detect_online(val)
        if res:
            drift_count += 1
    print(f"  Online drifts found : {drift_count}")


if __name__ == "__main__":
    run_scenario("Calm Market → Crash → Recovery", n=600, n_shifts=2)
    run_scenario("High Volatility Multi-Shift", n=1000, n_shifts=5)
    run_scenario("Single Sudden Shift", n=400, n_shifts=1)
    print("\n✅ All scenarios complete.")
