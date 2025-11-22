# KALDRA-ALPHA — Financial Earnings App (v0.1)

Este módulo fornece uma camada de aplicação mínima para processar
transcrições de earnings calls usando o KALDRA CORE.

- Entrada: texto da call (`raw_text`).
- Pipeline: `ingest_source` → `generate_kaldra_signal`.
- Saída: JSON no formato `kaldra_signal.schema.json`.

Nenhuma lógica financeira específica foi implementada ainda.
