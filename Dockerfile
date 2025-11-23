# ============================================
# KALDRA API Gateway - Production Dockerfile
# ============================================
# Base: Python 3.11 slim for smaller image size
# Compatible with PyTorch and NumPy

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PyTorch and NumPy
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# .dockerignore filters out: .git, .venv, node_modules, __pycache__, etc.
# Includes: src/, kaldra_api/, kaldra_data/, schema/, data/
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 kaldra && chown -R kaldra:kaldra /app
USER kaldra

# Expose port (Render will set $PORT dynamically)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:${PORT:-8000}/health')"

# Start command (Render will override $PORT)
CMD uvicorn kaldra_api.main:app --host 0.0.0.0 --port ${PORT:-8000}
