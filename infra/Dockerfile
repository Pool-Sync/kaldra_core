FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    KALDRA_ENV=container \
    KALDRA_LOG_LEVEL=INFO

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar infra (requirements) e código
COPY infra/ ./infra/
COPY kaldra_core/ ./kaldra_core/
COPY kaldra_api/ ./kaldra_api/

# Instalar dependências
COPY infra/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Comando real da API
CMD ["sh", "-c", "uvicorn kaldra_api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
