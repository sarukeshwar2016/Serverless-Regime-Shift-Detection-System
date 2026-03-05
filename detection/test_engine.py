import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from detection.engine import DetectionEngine, RegimeTracker

def test_flat_prices():
    engine = DetectionEngine()
    tracker = RegimeTracker(confirmations_required=3)
    
    # Flat crypto
    window = {
        "source": "binance",
        "asset": "BTCUSDT",
        "asset_class": "crypto",
        "values": [50000.0] * 60,
        "mean_value": 50000.0
    }
    
    print("Testing flat prices (Crypto)...")
    for i in range(4):
        res = engine.classify_regime(window)
        confirmed = tracker.track(res)
        print(f"Window {i+1} | Raw: {res['regime']} | Confirmed: {confirmed}")
        assert res['regime'] == "STABLE"

def test_spiked_prices():
    engine = DetectionEngine()
    tracker = RegimeTracker(confirmations_required=3)
    
    print("\nTesting spiked prices (Payments)...")
    # Base flat prices
    for i in range(2):
        window = {
            "source": "payments",
            "asset": "charge",
            "asset_class": "payments",
            "values": [10.0] * 60,
            "mean_value": 10.0
        }
        res = engine.classify_regime(window)
        confirmed = tracker.track(res)
        print(f"Flat Window {i+1} | Raw: {res['regime']} | Confirmed: {confirmed}")
        
    # Sudden spike
    spiked_window = {
        "source": "payments",
        "asset": "charge",
        "asset_class": "payments",
        "values": [10.0]*30 + [500.0]*30,
        "mean_value": 255.0
    }
    for i in range(4):
        res = engine.classify_regime(spiked_window)
        confirmed = tracker.track(res)
        print(f"Spike Window {i+1} | Raw: {res['regime']} | Confirmed: {confirmed}")

if __name__ == "__main__":
    test_flat_prices()
    test_spiked_prices()
    print("\nTests completed!")
