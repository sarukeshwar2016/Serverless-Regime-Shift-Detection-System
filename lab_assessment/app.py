import gradio as gr
import sys
import os
import json
import math

# Ensure parent directory is in the path to import our detection engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from detection.engine import DetectionEngine

def predict(price1, price2, price3, price4, price5):
    """
    Hybrid approach:
    - STEP 1: Use ADWIN + PELT (ML) to handle STABLE and TRANSITIONING.
    - STEP 2: Z-score formula used as tiebreaker.
                If PELT fires AND spike Z-score >= 2.0 → STRESSED
    This ensures the ML handles the normal cases correctly,
    while the formula catches clear spikes that ADWIN misses due to short history.
    """
    engine = DetectionEngine()

    # Build window: 60 stable baseline points + 30 spike points
    baseline = [float(price1), float(price2), float(price3)] * 20
    spike    = [float(price4), float(price5)] * 15
    prices   = baseline + spike
    mean_val = sum(prices) / len(prices)

    # --- STEP 1: ML detection (PELT offline + ADWIN online) ---
    try:
        offline = engine.detect_offline(prices)
        pelt_triggered = offline.get("n_changepoints", 0) > 0
    except Exception:
        pelt_triggered = False

    drift_triggered = False
    for v in prices:
        if engine.detect_online(v):
            drift_triggered = True
            engine.reset_online()
            break

    # --- STEP 2: Z-score formula (tiebreaker for STRESSED) ---
    baseline_mean = sum(baseline) / len(baseline)
    variance      = sum((x - baseline_mean) ** 2 for x in baseline) / len(baseline)
    baseline_std  = math.sqrt(variance) if variance > 0 else 1.0
    z_scores      = [abs(v - baseline_mean) / baseline_std for v in spike]
    max_z         = max(z_scores)

    # Z-score confirms a major spike that ADWIN hasn't seen enough history to confirm
    z_confirms_stressed = (max_z >= 2.0)

    # --- Ensemble classification ---
    if pelt_triggered and (drift_triggered or z_confirms_stressed):
        # ML detected structure change + either ADWIN confirmed or Z-score confirms spike
        regime     = "STRESSED"
        confidence = 1.0
        emoji      = "🔴"
    elif pelt_triggered or drift_triggered:
        # Only one ML detector fired
        regime     = "TRANSITIONING"
        confidence = 0.5
        emoji      = "🟠"
    else:
        # No structural change detected
        regime     = "STABLE"
        confidence = 1.0
        emoji      = "🟢"

    details = {
        "ml_pelt_triggered":    pelt_triggered,
        "ml_adwin_triggered":   drift_triggered,
        "z_score_max":          round(max_z, 2),
        "z_confirms_stressed":  z_confirms_stressed,
        "confidence":           confidence,
        "baseline_mean":        round(baseline_mean, 2),
        "baseline_std":         round(baseline_std, 2),
    }

    return (
        f"{emoji} Predicted Regime: {regime}\n\n"
        f"ML: PELT={pelt_triggered} | ADWIN={drift_triggered}\n"
        f"Z-score (tiebreaker): max_z={max_z:.2f} — confirms_stressed={z_confirms_stressed}\n\n"
        "Details:\n" + json.dumps(details, indent=2)
    )


# ── Gradio UI ────────────────────────────────────────────────────────────────
iface = gr.Interface(
    fn=predict,
    inputs=[
        gr.Number(label="Normal Event 1 (baseline)", value=10.0),
        gr.Number(label="Normal Event 2 (baseline)", value=12.0),
        gr.Number(label="Normal Event 3 (baseline)", value=11.0),
        gr.Number(label="Spike Event 4 (anomaly)",   value=5000.0),
        gr.Number(label="Spike Event 5 (anomaly)",   value=4800.0),
    ],
    outputs=gr.Textbox(label="Detection Engine Results", lines=16),
    title="Real-Time Regime Detection API",
    description=(
        "Enter 3 normal baseline values and 2 spike/anomaly values. "
        "The engine uses PELT + ADWIN (ML) as primary detectors, "
        "with a Z-score formula as tiebreaker to confirm STRESSED regimes."
    ),
    examples=[
        [10,  12,  11,   5000,  4800],   # clear spike  → STRESSED
        [100, 102, 101,  105,   103 ],   # no spike     → STABLE
        [50,  52,  51,   80,    75  ],   # mild change  → TRANSITIONING
    ]
)

if __name__ == "__main__":
    iface.launch(server_name="127.0.0.1", server_port=7862)
