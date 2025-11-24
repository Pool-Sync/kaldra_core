# KALDRA Data Lab — Workers

## Purpose
Os workers executam ingestões periódicas de dados (notícias, earnings, geopolitics, UX reviews).

## Estrutura

kaldra_data/workers/
 └── news_ingest_worker.py

scripts/
 └── run_news_ingest.py

## Como rodar localmente

source .venv/bin/activate
python scripts/run_news_ingest.py --query "AI" --limit 50

## Produção (Render Cron Job)
No painel do Render:
Jobs → New Job → Command:

python scripts/run_news_ingest.py --query "AI" --limit 50

## Futuro
- earnings_ingest_worker.py
- geo_ingest_worker.py
- product_reviews_worker.py
