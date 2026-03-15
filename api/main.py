"""
FastAPI REST API — exposes regime-shift detection capabilities
and recent results over HTTP for the React Dashboard.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add parent directory to path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from state.redis_client import RedisClient
from storage.mongo_client import MongoStorageClient

app = FastAPI(
    title="Regime Shift Detection API",
    description="Real-time and historical regime shift data API for the dashboard.",
    version="1.0.0",
)

# Enable CORS so the React Dashboard frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize storage clients 
redis_db = RedisClient()
mongo_db = MongoStorageClient()

@app.get("/")
def root():
    return {"status": "ok", "message": "Regime Platform API running."}

@app.get("/health")
def health():
    return {"status": "healthy"}

# --- HOT LAYER: Redis (Real-Time State) ---

@app.get("/api/state/all", summary="Get current regime state for all assets")
def get_all_states():
    """Returns the instant snapshot of current market regimes across all processed streams."""
    states = redis_db.get_all_states()
    return {"status": "success", "data": states}

@app.get("/api/state/{source}/{asset}", summary="Get current regime state for a specific asset")
def get_asset_state(source: str, asset: str):
    """Returns the instant snapshot of a specific asset from the Hot Layer."""
    state = redis_db.get_regime_state(source, asset)
    if not state:
        raise HTTPException(status_code=404, detail=f"No active state found for {source}:{asset}")
    return {"status": "success", "data": state}

# --- COLD LAYER: MongoDB (Historical Anomalies) ---

@app.get("/api/history", summary="View the historical ledger of all STRESSED/TRANSITIONING anomalies")
def get_historical_anomalies(limit: int = 50):
    """Retrieves the permanent historical logs of all confirmed anomalies."""
    if not mongo_db.client:
        return {"status": "error", "message": "MongoDB is not connected."}
        
    try:
        # Fetch latest anomalies, ignoring the _id field because it is not JSON serializable by default
        docs = list(mongo_db.collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit))
        return {"status": "success", "count": len(docs), "data": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
