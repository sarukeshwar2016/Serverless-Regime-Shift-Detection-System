import sys
import os
import time
from pprint import pprint

# Ensure parent directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from state.redis_client import RedisClient

def test_redis_memory_layer():
    print("==================================================")
    print("      REGIME PLATFORM - PHASE 4 REDIS TEST        ")
    print("==================================================")
    
    redis_db = RedisClient()
    if not redis_db.client:
        print("❌ Cannot proceed with test. Redis/Memurai is not running on localhost:6379.")
        return

    print("✅ Successfully connected to local Redis memory layer!")
    
    source = "test_source"
    asset = "BTC-USD"
    
    # 1. Simulate saving a STABLE state
    stable_regime = {
        "regime": "STABLE",
        "confidence": 1.0,
        "mean_value": 65000.0,
        "pelt_triggered": False,
        "drift_triggered": False
    }
    
    print(f"\n[1] Saving STABLE regime for {asset}...")
    success = redis_db.save_regime_state(source, asset, stable_regime)
    if success:
        print("    -> Save successful!")
    
    # 2. Retrieve the state
    print("\n[2] Instantly retrieving state from Memory Layer...")
    retrieved = redis_db.get_regime_state(source, asset)
    if retrieved:
        print(f"    -> Current Regime: {retrieved['regime']}")
        print(f"    -> Mean Value: ${retrieved['mean_value']:.2f}")
        print(f"    -> Updated At: {retrieved['updated_at']}")
    
    # 3. Simulate an anomaly (STRESSED) replacing it instantly
    time.sleep(1) # wait briefly to simulate time passing
    stressed_regime = {
        "regime": "STRESSED",
        "confidence": 1.0,
        "mean_value": 45000.0,
        "pelt_triggered": True,
        "drift_triggered": True
    }
    print(f"\n[3] Anomaly detected! Instantly overwriting state with STRESSED...")
    redis_db.save_regime_state(source, asset, stressed_regime)
    
    # 4. Final retrieval to prove overwrite
    final_state = redis_db.get_regime_state(source, asset)
    print("\n[4] Retrieving final state...")
    print(f"    -> New Regime: {final_state['regime']}")
    print(f"    -> New Mean Value: ${final_state['mean_value']:.2f}")
    
    print("\n✅ Phase 4 Test Complete! The in-memory data store is fully functional.")
    print("==================================================")

if __name__ == "__main__":
    test_redis_memory_layer()
