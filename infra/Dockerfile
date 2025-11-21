FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    KALDRA_ENV=container \
    KALDRA_LOG_LEVEL=INFO

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar infra (requirements) e código principal do KALDRA
COPY infra/ ./infra/
COPY core/ ./core/
COPY data/ ./data/
COPY kaldra_engine/ ./kaldra_engine/
COPY kaldra_api/ ./kaldra_api/
COPY kaldra_data/ ./kaldra_data/
COPY apps/ ./apps/
COPY scripts/ ./scripts/

# Instalar dependências do backend
COPY infra/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Entrypoint do KALDRA API para Render (usa PORT se existir)
CMD ["sh", "-c", "uvicorn kaldra_api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
