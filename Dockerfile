FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# ── System packages ──────────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    redis-server \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# ── Install Node.js 20 ───────────────────────────────────────────────────────
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# ── Python dependencies ───────────────────────────────────────────────────────
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools wheel \
    && pip3 install --no-cache-dir -r requirements.txt

# ── Copy Python backend source ────────────────────────────────────────────────
COPY api/ ./api/
COPY detection/ ./detection/
COPY ingestion/ ./ingestion/
COPY state/ ./state/
COPY storage/ ./storage/

# ── Next.js frontend ──────────────────────────────────────────────────────────
WORKDIR /app/dashboard
COPY dashboard/package*.json ./
RUN npm install
COPY dashboard/ ./
RUN npm run build

# ── Boot script ───────────────────────────────────────────────────────────────
WORKDIR /app
COPY start.sh .
RUN chmod +x start.sh

# Hugging Face Spaces requires port 7860
EXPOSE 7860

# Environment (MONGO_URI is injected via HF Space Secrets)
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379
ENV BINANCE_STREAM_URL=wss://stream.binance.com:9443/stream?streams=btcusdt@trade/ethusdt@trade/solusdt@trade/bnbusdt@trade/xrpusdt@trade/adausdt@trade

CMD ["bash", "start.sh"]
