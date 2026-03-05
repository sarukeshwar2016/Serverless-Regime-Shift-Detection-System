import time
import sys
import os

# Ensure the parent directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from detection.test_engine import test_flat_prices, test_spiked_prices
from ingestion.adapters.binance_adapter import BinanceAdapter
from ingestion.window_builder import WindowBuilder
from ingestion.stream_manager import StreamManager

def run_demo():
    print("==================================================")
    print("      REGIME PLATFORM DEMO (PHASES 1-3)           ")
    print("==================================================")
    
    print("\n--- [PART 1] DETECTION ENGINE (Ruptures + River) ---")
    time.sleep(1)
    
    print("\nTest 1: Normal Market Conditions (Stable Prices)")
    test_flat_prices()
    time.sleep(1)
    
    print("\nTest 2: Offline Financial Datasets (Phase 9 Integration)")
    from demo.simulator.data_injector import DataInjector
    # Test the fraud wave
    csv_path = os.path.join(os.path.dirname(__file__), 'demo', 'datasets', 'payments_fraud_wave.csv')
    injector = DataInjector(csv_path=csv_path, speed_multiplier=20)
    injector.run()
    time.sleep(1)
    
    print("\n--- [PART 2] LIVE DATA INGESTION (Binance) ---")
    print("Starting Live Stream...")
    print("We will capture 10 seconds of live crypto data to prove connectivity.\n")
    
    # We use a 10s window just for a quick demo, so the professor doesn't wait 60s
    window_builder = WindowBuilder(window_seconds=10) 
    manager = StreamManager(window_builder)
    manager.register(BinanceAdapter())
    manager.start()
    
    try:
        # Wait for exactly 12 seconds to ensure we capture a 10s window cleanly
        # and print out the live trades falling into the window as they happen.
        for i in range(12):
            print(f"Waiting for live data... {12-i} seconds left")
            time.sleep(1)
            
        windows = window_builder.get_windows()
        print(f"\n--- [Live Ingestion Result] ---")
        if not windows:
            print("No data received in 10 seconds. Market might be quiet, or connection issue.")
        else:
            for w in windows:
                print(f"Source: {w['source']} | Asset: {w['asset']}")
                print(f"Events Captured: {w['event_count']}")
                print(f"Mean Price: ${w['mean_value']:.2f}")
                print(f"Change Percentage: {w['value_change_pct']:.4f}%")
                print(f"Current Regime Snapshot: {w['compression_tier']}")
    finally:
        manager.stop()
        
    print("\n==================================================")
    print("                 DEMO COMPLETE!                   ")
    print("==================================================")

if __name__ == "__main__":
    run_demo()
