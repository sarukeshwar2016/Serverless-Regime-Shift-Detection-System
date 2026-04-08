#!/bin/bash

# Start Redis in daemon mode
echo "Starting Redis..."
redis-server --daemonize yes

# Wait a second for Redis to be fully available
sleep 2

# Start the Ingestion pipeline in the background
echo "Starting Ingestion Pipeline..."
python ingestion/run.py &

# Start the FastAPI Backend in the background
echo "Starting FastAPI Backend..."
python api/main.py &

# Wait for FastAPI to bind
sleep 3

# Start the Next.js Frontend in the foreground (Hugging Face needs port 7860 exposed)
echo "Starting Next.js Frontend..."
cd dashboard
npm run start
