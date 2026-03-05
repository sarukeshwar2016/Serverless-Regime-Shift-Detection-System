# 🔍 Regime Shift Detection Platform

A **Generic Financial Behavior Monitoring Platform** that ingests live financial data from multiple sources (crypto, payments, stocks, forex), detects regime shifts in real time, stores results in AWS DynamoDB, and exposes findings via a REST API.

---

## 🧠 What This Platform Does (Plain English)

Financial markets don't behave the same way all the time. Sometimes prices are calm, sometimes they crash, sometimes they spike. A **regime shift** is when the market's behavior fundamentally changes — like going from "steady growth" to "sudden crash."

This platform:
1. **Listens** to live data streams (Binance crypto trades, synthetic payment streams)
2. **Detects** when the behavior changes using two methods:
   - **Offline detection** (ruptures library) — analyzes a batch of data after it's collected
   - **Online detection** (river library) — spots changes point-by-point as data arrives
3. **Saves** results to AWS DynamoDB for historical analysis
4. **Serves** results through a REST API so dashboards and other tools can use them

---

## 📂 Project Structure

```
regime-platform/
├── .env                        # Environment variables (AWS keys, Redis, etc.)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── verify_install.py           # Script to verify all libraries are installed
│
├── ingestion/                  # DATA INGESTION — connects to live data sources
│   ├── adapters/
│   │   ├── base_adapter.py     #   Abstract base class for all adapters
│   │   ├── binance_adapter.py  #   Binance WebSocket crypto trade stream

│   ├── window_builder.py       #   Collects data into time-based windows
│   └── stream_manager.py       #   Manages multiple adapters in parallel
│
├── detection/                  # DETECTION ENGINE — finds regime shifts
│   └── engine.py               #   Offline (ruptures) + online (river) detection
│
├── storage/                    # STORAGE — persists results
│   └── dynamo_client.py        #   AWS DynamoDB read/write wrapper
│
├── state/                      # STATE MANAGEMENT — real-time caching
│   └── redis_client.py         #   Redis wrapper for live state
│
├── api/                        # REST API — exposes results over HTTP
│   └── main.py                 #   FastAPI server with health & results endpoints
│
├── lambda_functions/           # SERVERLESS — AWS Lambda handlers
│   ├── detection_handler.py    #   Lambda wrapper for the detection engine
│   └── api_handler.py          #   Mangum wrapper to run FastAPI on Lambda
│
├── demo/                       # DEMO & TESTING — try the platform without live data
│   ├── datasets/
│   │   └── download_datasets.py#   Download stock data & generate synthetic data
│   ├── simulator/
│   │   ├── data_injector.py    #   Replay CSV data through the detection engine
│   │   ├── shift_trigger.py    #   Generate synthetic regime-shift signals
│   │   └── scenario_runner.py  #   Run pre-defined demo scenarios end-to-end
│   └── demo_api.py             #   Lightweight demo API for quick testing
│
└── dashboard/                  # DASHBOARD — web-based monitoring UI
    └── index.html              #   Dark-themed real-time dashboard
```

---

## 🚀 How to Start

### 1. Verify Installation
```bash
python verify_install.py
```
All libraries should show **OK**.

### 2. Start the API Server
```bash
python -m api.main
```
Visit [http://localhost:8000](http://localhost:8000) to see the API.

### 3. Run the Demo API (no AWS required)
```bash
python -m demo.demo_api
```
Visit [http://localhost:8001/demo/detect](http://localhost:8001/demo/detect) to generate synthetic data and see detection results.

### 4. Run Demo Scenarios
```bash
python -m demo.simulator.scenario_runner
```

### 5. Open the Dashboard
Open `dashboard/index.html` in your browser. It will auto-connect to the API if it's running.

---

## ⚙️ Configuration

Edit the `.env` file with your real credentials:

| Variable | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
| `AWS_REGION` | AWS region (default: us-east-1) |
| `REDIS_HOST` | Redis server host |
| `REDIS_PORT` | Redis server port |
| `BINANCE_STREAM_URL` | Binance WebSocket stream URL |

| `DEMO_MODE` | Set to `true` to use synthetic data |

---

## 📚 Key Libraries

| Library | Purpose |
|---|---|
| **ruptures** | Offline change-point detection (PELT algorithm) |
| **river** | Online drift detection (ADWIN algorithm) |
| **FastAPI** | REST API framework |
| **boto3** | AWS SDK for DynamoDB |
| **redis** | Real-time state caching |
| **websocket-client** | Binance WebSocket connection |
| **yfinance** | Historical stock data |
| **mangum** | Run FastAPI on AWS Lambda |
