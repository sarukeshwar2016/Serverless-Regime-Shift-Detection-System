"""
Demo API — a lightweight FastAPI server that generates synthetic data
and runs detection on-the-fly for quick demonstrations.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from detection.engine import DetectionEngine
from demo.simulator.shift_trigger import generate_shift_signal

app = FastAPI(title="Regime Platform Demo API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

engine = DetectionEngine()


@app.get("/")
def root():
    return {"status": "demo", "message": "Regime Platform Demo API"}


@app.get("/demo/detect")
def demo_detect(n: int = 500, shifts: int = 3):
    """Generate synthetic data and run detection."""
    signal = generate_shift_signal(n=n, n_shifts=shifts)
    result = engine.detect_offline(signal)
    return {
        "signal_length": len(signal),
        "signal_preview": signal[:20],
        "detection": result,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
