#!/bin/bash
set -e

echo "==> Starting Redis..."
redis-server --daemonize yes --port 6379

echo "==> Starting FastAPI backend..."
cd /app
uvicorn api.main:app --host 0.0.0.0 --port 8000 &

echo "==> Waiting for API to be ready..."
sleep 5

echo "==> Starting Binance ingestion engine..."
python ingestion/run.py &

echo "==> Starting Next.js frontend on port 7860..."
cd /app/dashboard
PORT=7860 npm run start
