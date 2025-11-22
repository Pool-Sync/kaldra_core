# KALDRA-PRODUCT — Product & UX App (v0.1)

Aplicação mínima para análise de produtos, reviews e UX usando o KALDRA CORE.

- Entrada: texto de reviews, feedbacks, UX reports (`raw_text`).
- Pipeline: `ingest_source` → `generate_kaldra_signal`.
- Saída: JSON no formato `kaldra_signal.schema.json`.
