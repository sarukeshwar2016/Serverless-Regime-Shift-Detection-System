import time
import sys
import os

# Ensure the parent directory is in the path so we can import ingestion modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.adapters.binance_adapter import BinanceAdapter
from ingestion.window_builder import WindowBuilder
from ingestion.stream_manager import StreamManager

def main():
    # Phase 2 requires 60 second windows. For testing we can use 10 seconds or wait.
    print("[Main Runner] Starting ingestion pipeline...")
    window_builder = WindowBuilder(window_seconds=60)
    manager = StreamManager(window_builder)
    
    manager.register(BinanceAdapter())
    
    manager.start()
    
    from detection.engine import DetectionEngine, RegimeTracker
    
    engine = DetectionEngine()
    tracker = RegimeTracker()
    
    try:
        while True:
            time.sleep(60)
            windows = window_builder.get_windows()
            window_builder.clear()
            
            print("\n--- [Main Runner] 60s Window Elapsed ---")
            
            for w in windows:
                # 1. Detect Regime (Phase 3)
                result = engine.classify_regime(w)
                confirmed_regime = tracker.track(result)
                    
                print(f"[{w['source']}:{w['asset']}] -> Confirmed Regime: {confirmed_regime} | Events: {w['event_count']}")
                
    except KeyboardInterrupt:
        print("\nStopping ingestion pipeline...")
        manager.stop()
        sys.exit(0)


if __name__ == "__main__":
    main()
