"""
FastAPI REST API — exposes regime-shift detection capabilities
and recent results over HTTP.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Regime Shift Detection API",
    description="REST API for the Generic Financial Behavior Monitoring Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Regime Shift Detection API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/results")
def get_results():
    """Placeholder — will return recent detection results from DynamoDB."""
    return {"results": [], "message": "Connect DynamoDB to see real results"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
