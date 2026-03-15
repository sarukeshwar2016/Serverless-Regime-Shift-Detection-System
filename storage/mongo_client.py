import os
import time
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

class MongoStorageClient:
    """
    Handles permanent cloud storage for the Regime Platform using MongoDB Atlas.
    Matches the 3-table Serverless architecture (RegimeEvents, WindowData, CurrentRegime).
    """
    def __init__(self):
        self.uri = os.getenv("MONGO_URI")
        if not self.uri or "<db_password>" in self.uri:
            print("⚠️ MongoDB URI missing or <db_password> not replaced in .env")
            self.client = None
            return
            
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client["regime_platform"]
            
            # The 3 collections as requested by the 2-Tier Architecture design
            self.regime_events = self.db["regime_events"]
            self.window_data = self.db["window_data"]
            self.current_regime = self.db["current_regime"]
            
        except Exception as e:
            print(f"⚠️ MongoDB connection failed: {e}")
            self.client = None

    def log_regime_event(self, source: str, asset: str, result: dict, timestamp_ms: int) -> bool:
        """Table 1 - RegimeEvents: Primary audit trail for confirmed events."""
        if not self.client: return False
        try:
            document = {
                "source_asset": f"{source}#{asset}",
                "timestamp": timestamp_ms,
                "source": source,
                "asset": asset,
                "regime_data": result, # For backwards compatibility with dashboard
                "regime": result.get("regime"),
                "confidence": result.get("confidence", 1.0),
                "pelt_triggered": result.get("pelt_triggered", False),
                "drift_triggered": result.get("drift_triggered", False),
            }
            self.regime_events.insert_one(document)
            return True
        except Exception as e:
            print(f"MongoDB log_regime_event error: {e}")
            return False

    def write_window_data(self, source: str, asset: str, window_dict: dict, regime: str) -> bool:
        """Table 2 - WindowData: Implements regime-aware compression."""
        if not self.client: return False
        try:
            raw_points = window_dict.get('raw_points', [])
            values = window_dict.get('values', [])
            
            # Get timestamps from raw points if available, otherwise fallback
            window_open = raw_points[0].get('T', time.time() * 1000) if raw_points else time.time() * 1000
            window_close = raw_points[-1].get('T', time.time() * 1000) if raw_points else time.time() * 1000
            
            base = {
                "source_asset": f"{source}#{asset}",
                "window_open": int(window_open),
                "window_close": int(window_close),
                "regime": regime,
                "tick_count": len(raw_points)
            }
            
            if regime == "STABLE":
                # Compress into 5 numbers (OHLCV)
                if values:
                    base.update({
                        "compression": "OHLCV_1MIN",
                        "open": float(values[0]),
                        "high": float(max(values)),
                        "low": float(min(values)),
                        "close": float(values[-1]),
                        "volume": sum(float(p.get("q", 0) or p.get("amount", 0)) for p in raw_points),
                        "raw_ticks": None
                    })
            elif regime == "TRANSITIONING":
                # Sample roughly every 10 items (or 10 seconds if 1 tick/sec)
                sampled = raw_points[::10]
                base.update({
                    "compression": "TEN_SECOND",
                    "intervals": sampled,
                    "raw_ticks": None
                })
            elif regime == "STRESSED":
                # Preserve all raw ticks
                base.update({
                    "compression": "NONE",
                    "raw_ticks": raw_points
                })
                
            self.window_data.insert_one(base)
            return True
        except Exception as e:
            print(f"MongoDB write_window_data error: {e}")
            return False

    def update_current_regime(self, source: str, asset: str, regime: str, confidence: float, timestamp_ms: int) -> bool:
        """Table 3 - CurrentRegime: Upserts the latest state."""
        if not self.client: return False
        try:
            query = {"source_asset": f"{source}#{asset}"}
            update = {"$set": {
                "regime": regime,
                "confidence": confidence,
                "last_updated": timestamp_ms
            }}
            self.current_regime.update_one(query, update, upsert=True)
            return True
        except Exception as e:
            print(f"MongoDB update_current_regime error: {e}")
            return False
            
    # Keep the old method for backwards compatibility with test scripts
    def log_anomaly(self, source: str, asset: str, anomaly_data: dict) -> bool:
        return self.log_regime_event(source, asset, anomaly_data, int(time.time() * 1000))
