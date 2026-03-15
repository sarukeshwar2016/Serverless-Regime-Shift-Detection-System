import redis
import json
from typing import Dict, Any, Optional
import time

class RedisClient:
    """
    Handles local in-memory storage (Redis/Memurai) for the Regime Platform.
    Stores the latest detected regime state for each asset, ensuring the dashboard
    and API can instantly read the current state without querying a database.
    """
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        try:
            self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
            # Test connection
            self.client.ping()
        except redis.ConnectionError as e:
            print(f"⚠️ Redis connection failed. Is Redis/Memurai running? Error: {e}")
            self.client = None

    def save_regime_state(self, source: str, asset: str, regime_data: Dict[str, Any]) -> bool:
        """
        Saves the latest regime state for a specific source and asset.
        Key format: regime:{source}:{asset}
        """
        if not self.client:
            return False
            
        key = f"regime:{source}:{asset}"
        
        # Add timestamp if not present
        if "updated_at" not in regime_data:
            regime_data["updated_at"] = time.time()
            
        try:
            # Save as JSON string
            self.client.set(key, json.dumps(regime_data))
            
            # Also publish to a channel for real-time subscribers (e.g. websockets)
            self.client.publish("regime_updates", json.dumps(regime_data))
            return True
        except Exception as e:
            print(f"Redis save error: {e}")
            return False

    def save_adwin_state(self, source: str, asset: str, adwin_obj: Any) -> bool:
        """Serializes and saves the ADWIN state to Redis using Pickle & Base64."""
        if not self.client:
            return False
        try:
            import pickle
            import base64
            key = f"adwin:{source}:{asset}"
            pickled_data = pickle.dumps(adwin_obj)
            encoded_data = base64.b64encode(pickled_data).decode('utf-8')
            self.client.set(key, encoded_data)
            return True
        except Exception as e:
            print(f"Redis save adwin error: {e}")
            return False

    def load_adwin_state(self, source: str, asset: str) -> Optional[Any]:
        """Loads and deserializes the ADWIN state from Redis."""
        if not self.client:
            return None
        try:
            import pickle
            import base64
            key = f"adwin:{source}:{asset}"
            data = self.client.get(key)
            if data:
                decoded_data = base64.b64decode(data)
                return pickle.loads(decoded_data)
            return None
        except Exception as e:
            print(f"Redis load adwin error: {e}")
            return None

    def get_regime_state(self, source: str, asset: str) -> Optional[Dict[str, Any]]:
        """Retrieves the latest regime state for a specific asset."""
        if not self.client:
            return None
            
        key = f"regime:{source}:{asset}"
        try:
            data = self.client.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None
            
    def get_all_states(self) -> Dict[str, Dict[str, Any]]:
        """Retrieves all current regime states across all assets."""
        if not self.client:
            return {}
            
        states = {}
        try:
            keys = self.client.keys("regime:*")
            for key in keys:
                data = self.client.get(key)
                if data:
                    states[key] = json.loads(data)
            return states
        except Exception:
            return {}
