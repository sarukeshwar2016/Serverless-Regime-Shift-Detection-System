FROM node:20-bullseye

# Install Python and Redis
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Setup Python Virtual Environment and install requirements
COPY requirements.txt /app/
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . /app/

# Install Next.js dependencies and build the frontend dashboard
WORKDIR /app/dashboard
RUN npm install
RUN npm run build

# Move back to root directory and prepare the start script
WORKDIR /app
RUN chmod +x start.sh

# Provide the 7860 port for Hugging Face Spaces (and Next.js)
ENV PORT=7860
EXPOSE 7860

# Command to run on startup
CMD ["./start.sh"]
