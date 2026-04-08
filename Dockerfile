FROM node:20-bullseye

# Set working directory for the frontend
WORKDIR /app/dashboard

# Copy package files into container
COPY dashboard/package*.json ./

# Install pristine modules
RUN npm install

# Copy all the dashboard source code
COPY dashboard/ ./

# Build Next.js Production App
RUN npm run build

# Next.js will default run on port 3000, but we pass PORT 7860 so it binds to HF specs.
ENV PORT=7860
EXPOSE 7860

# Standalone start command
CMD ["npm", "run", "start"]
