# Regime Platform — Phase Roadmap

## Phase 1 ✅ COMPLETE — Set Up Workspace
- Python verified, folder structure created, all libraries installed, .env configured, README written.

---

## Phase 2 — Generic Ingestion Layer
**Goal:** Connect to live financial data from multiple sources
**Time:** 2–3 days | **Difficulty:** Easy–Medium

### Tasks:
1. **Base Adapter** (`ingestion/adapters/base_adapter.py`) — Abstract base class with `connect()`, `disconnect()`, `normalize_event()`, `get_source_name()`, `validate_event()`. Standard format: `{source, asset, asset_class, timestamp, value, volume, metadata}`
2. **Binance Adapter** (`ingestion/adapters/binance_adapter.py`) — WebSocket to `wss://stream.binance.com:9443/ws/btcusdt@trade`, auto-reconnect, logging to `ingestion_binance.log`
3. **Window Builder** (`ingestion/window_builder.py`) — Groups events by source+asset, produces 60s windows with `{source, asset, asset_class, window_start, window_end, values, mean_value, value_change_pct, event_count, compression_tier}`
4. **Stream Manager** (`ingestion/stream_manager.py`) — `add_adapter()`, `start_all()` (threaded), `stop_all()`, feeds WindowBuilder
5. **Main Runner** (`ingestion/run.py`) — Creates adapters, starts StreamManager, prints status every 60s
6. **Test** — Verify live prices normalize, windows print every 60s, logs written

---

## Phase 3 — Detection Engine
**Goal:** Detect when financial behavior changes
**Time:** 3–4 days | **Difficulty:** Medium

### Tasks:
1. **PELT Detection** — `run_pelt_detection(values)` using ruptures, model="rbf", returns `{triggered, score}`
2. **Drift Detection** — `run_drift_detection(values)` using river ADWIN, returns `{triggered, score}`
3. **Ensemble Voting** — `classify_regime(window)`: both→STRESSED, one→TRANSITIONING, neither→STABLE. Returns `{source, asset, asset_class, regime, confidence, pelt_triggered, drift_triggered, mean_value, detected_at}`
4. **False Positive Suppression** — `RegimeTracker` class: 3 consecutive windows to confirm regime change
5. **Test** — Flat prices→STABLE, spiked prices→STRESSED, for both crypto and payment formats

---

## Phase 4 — Redis Memory Layer
**Goal:** Make the system remember state between steps
**Time:** 2–3 days | **Difficulty:** Medium

### Tasks:
1. **Install Redis** — Memurai (Windows Redis alternative), verify with `redis-cli ping`
2. **Redis Client** (`state/redis_client.py`) — `RegimeStateManager`: `save_current_regime()`, `get_current_regime()`, `save_window_to_history()`, `get_window_history()`, `save_regime_event()`, `get_all_active_sources()`
3. **Connect Detection Engine** — Save regime after classification, save windows, save events on change, restore state on startup
4. **Test** — Run 3 min, check `KEYS *`, verify separate keys per source, verify restart loads previous regime

---

## Phase 5 — DynamoDB Permanent Storage
**Goal:** Save all regime events permanently to AWS
**Time:** 2–3 days | **Difficulty:** Medium

### Tasks:
1. **Verify AWS Credentials** — `aws sts get-caller-identity`
2. **Create DynamoDB Tables** (`setup_dynamo.py`) — `RegimeEvents` (PK: asset, SK: timestamp), `WindowData` (PK: asset, SK: timestamp), `CurrentRegime` (PK: asset)
3. **Storage Client** (`storage/dynamo_client.py`) — `RegimeStorage`: `save_regime_event()`, `save_window_compressed()` (adaptive: STABLE=summary, STRESSED=full), `update_current_regime()`, `query_recent_events()`, `query_by_asset_class()`
4. **Connect to Detection Engine** — Save events/windows/regime after every classification
5. **Verify** — Run 3 min, check AWS Console for tables with records, confirm STABLE has less data

---

## Phase 6 — REST API
**Goal:** Expose regime signals through a public API
**Time:** 2–3 days | **Difficulty:** Medium

### Endpoints:
- `GET /` — status + active sources
- `GET /regime/current` — current regime (filter: `?source=`, `?asset_class=`)
- `GET /regime/events` — regime transitions (filter: `?hours=`, `?asset_class=`, `?source=`)
- `GET /regime/history` — last N windows (filter: `?asset=`, `?windows=`)
- `GET /sources` — all active sources with regime
- `GET /health` — Redis/DynamoDB/stream status

### Tasks:
1. Build all endpoints in `api/main.py`
2. CORS + auto docs at `/docs`
3. Test all endpoints with browser screenshots

---

## Phase 7 — Dashboard
**Goal:** See everything visually in a browser
**Time:** 2–3 days | **Difficulty:** Easy–Medium

### Sections:
1. **Header** — Platform name, health dots (Redis/DynamoDB/Stream), updates every 30s
2. **Sources Panel** — Dynamic cards per source, color-coded (GREEN/YELLOW/RED), updates every 10s
3. **Live Chart** — Chart.js line chart, one line per source, last 20 windows, updates every 60s
4. **Event History Table** — Last 20 regime events, color-coded rows, updates every 30s
5. **Demo Control Panel** — Scenario buttons, manual inject buttons, historical replay buttons, status bar
6. **Verify** — Screenshot STABLE and STRESSED states

---

## Phase 8A — Prepare AWS Environment
**Goal:** Set up all AWS infrastructure
**Time:** 1 day

### Tasks:
1. Verify AWS CLI
2. Create IAM role `regime-lambda-role` with Lambda + DynamoDB policies
3. Verify DynamoDB tables
4. Create CloudWatch log groups
5. Create HTTP API Gateway `regime-api`
6. Save all ARNs/URLs to `aws_config.txt`

---

## Phase 8B — Deploy Detection Lambda
**Goal:** Run detection in the cloud every 60 seconds
**Time:** 1–2 days

### Tasks:
1. Lambda handler (`lambda_functions/detection_handler.py`) — reads WindowData, runs detection, saves results
2. Package Lambda with dependencies into zip
3. Deploy to AWS (Python 3.11, 256MB, 30s timeout)
4. EventBridge rule: `rate(1 minute)` → detection Lambda
5. Test via AWS Console + CloudWatch

---

## Phase 8C — Deploy API Lambda
**Goal:** Give platform a live public URL
**Time:** 1–2 days

### Tasks:
1. Wrap FastAPI with Mangum, Redis fallback to DynamoDB
2. Package Lambda into zip
3. Deploy to AWS
4. Connect API Gateway routes (`ANY /` and `ANY /{proxy+}`)
5. Test public URL endpoints

---

## Phase 8D — End-To-End Cloud Test
**Goal:** Confirm full pipeline works
**Time:** 1 day

### Tasks:
1. Update ingestion to write windows to DynamoDB
2. Create `run_ingestion.bat`
3. End-to-end test: ingestion → DynamoDB → Lambda → API Gateway
4. Verify with browser screenshots

---

## Phase 9 — Demo Mode & Test Datasets
**Goal:** Guarantee visible regime shifts during university presentation
**Time:** 2–3 days | **Difficulty:** Easy–Medium

### 5-Minute Presentation Script:
- 0:00 → Dashboard STABLE (all green)
- 0:30 → Stress Crypto → RED
- 1:00 → Show dashboard + API + DynamoDB live
- 1:30 → Stress Payments → two RED
- 2:00 → Cross-source detection proven
- 2:30 → Reset → GREEN
- 3:00 → Replay COVID Crash
- 3:30 → Detection fires at crash point
- 4:00 → Show detection latency
- 4:30 → Show DynamoDB filled
- 5:00 → Done

### Tasks:
1. **Download Datasets** — BTC COVID crash, BTC May 2021, S&P 500 March 2020, Black Friday payments (generated), Fraud wave (generated)
2. **Data Injector** (`demo/simulator/data_injector.py`) — `load_dataset()`, `replay_at_speed(300x)`, `replay_scenario()`
3. **Shift Trigger** (`demo/simulator/shift_trigger.py`) — `inject_stressed_regime()`, `inject_transitioning_regime()`, `inject_stable_regime()`, `inject_all_sources()`
4. **Scenario Runner** (`demo/simulator/scenario_runner.py`) — `university_demo` (4min scripted), `quick_demo` (2min)
5. **Demo API Endpoints** — `POST /demo/trigger-shift`, `POST /demo/trigger-scenario`, `POST /demo/replay`, `POST /demo/reset`, `GET /demo/status`
6. **Dashboard Demo Panel** — Scenario buttons, manual inject, historical replay, status bar
7. **Full Test** — Run university_demo, screenshot all 5 transitions
