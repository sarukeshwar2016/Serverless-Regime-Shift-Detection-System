import sys
import os
import time
from pprint import pprint

# Ensure parent directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from storage.mongo_client import MongoStorageClient

def test_mongo_cloud_storage():
    print("==================================================")
    print("    REGIME PLATFORM - PHASE 5 MONGODB CLOUD TEST  ")
    print("==================================================")
    
    mongo_db = MongoStorageClient()
    if not mongo_db.client:
        print("\n❌ Cannot proceed. Make sure you replaced <db_password> in the .env file.")
        return

    print("\n[1] Preparing a synthetic anomaly log...")
    
    # Simulate a historically confirmed STRESSED regime state
    anomaly_data = {
        "regime": "STRESSED",
        "confidence": 1.0,
        "mean_value": 42000.0,
        "details": "Major price drop detected. ADWIN and PELT triggered.",
        "updated_at": time.time()
    }
    
    print("\n[2] Pushing log to MongoDB Atlas (regime_platform -> anomaly_logs)...")
    success = mongo_db.log_anomaly(source="test_source", asset="BTC-USD", anomaly_data=anomaly_data)
    
    if success:
        print("    -> Document successfully inserted into cloud database!")
        print("\n✅ Phase 5 Test Complete! Go check your Atlas Dashboard > Browse Collections.")
    else:
        print("    -> ⚠️ Failed to insert document.")
        
    print("==================================================")

if __name__ == "__main__":
    test_mongo_cloud_storage()
