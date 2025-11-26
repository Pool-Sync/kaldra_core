# KALDRA Core — Master Engine & Data Lab Overview  
**Version:** 2.3  
**Status:** Production-Ready  
**Last Updated:** 2025-11-26  

---

# 1. Overview

O ecossistema KALDRA é estruturado em dois pilares fundamentais:

### **A. Master Engine (Interpretação)**
Pipeline matemático–simbólico que transforma embeddings em sinais narrativos estruturados.  
Responsável por:

- Δ144 Archetype Engine
- Kindra 3×48 cultural modulation
- TW369 drift dynamics
- Epistemic decision engine
- Logging + audit trail

### **B. Data Lab (Preparação de Dados)**
Módulo responsável pelo fluxo completo de ingestão e preparação de dados:

- PDFs, HTML, texto, APIs
- Limpeza, normalização, tokenização
- Segmentação por domínio
- Preparação para geração de embeddings  

O Data Lab produz *texto limpo e segmentado*.  
O Master Engine interpreta *embeddings numéricos*.

---

# 2. System Architecture Diagram

```
    ┌────────────────────────────────────┐
    │             DATA LAB               │
    │ Ingest → Clean → Normalize → Prep  │
    └──────────────────┬─────────────────┘
                       ↓
       ┌────────────────────────────────┐
       │       Embedding Generator      │
       │  ST / OpenAI / Cohere / Custom │
       └──────────────────┬─────────────┘
                       ↓
  ┌──────────────────────────────────────────┐
  │          KALDRA MASTER ENGINE            │
  │ Δ144 → Kindra → TW369 → Epistemic → Log │
  └──────────────────┬──────────────────────┘
                     ↓
             KaldraSignal
```

---

# 3. Responsibilities

## 3.1 Master Engine (src/core/kaldra_master_engine.py)

### **Input**
- `embedding: np.ndarray`
- `tw_window: Optional[np.ndarray]`

### **Process**
1. Δ144: arquétipos base
2. Kindra: modulação cultural/semiotic/estrutural
3. TW369: drift + tensões
4. Epistemic: decisão
5. Logging & Audit

### **Output**
Um `KaldraSignal` contendo:
- Probabilidades 144-dimensional
- Decisão epistemológica
- Delta state
- TW stats
- Flags de drift
- Audit record (opcional)

---

## 3.2 Data Lab (kaldra_data/)

### Funções principais:
- ingestão multi-formato
- normalização textual
- segmentação por domínio (Alpha, GEO, Product, Safeguard)
- preparação para embeddings

### Não faz:
- embeddings
- Δ144
- TW369
- Kindra

---

# 4. Embedding Integration

Data Lab → Embedding Generator → Master Engine

```
(texto limpo)
→ EmbeddingGenerator.encode()
→ vetor (1, D)
→ infer_from_embedding()
→ KaldraSignal
```

---

# 5. Why This Separation?

### Master Engine
**interpreta narrativas**  
(arquétipos, tensões, cultura, drift, epistemologia)

### Data Lab
**prepara dados**  
(ingestão, limpeza, normalização, batching)

### Embedding Generator
**transforma texto em números**

Cada módulo fica independente, testável e extensível.

---

# 6. Future Extensions (v2.4–v2.6)

### Master Engine
- Painlevé II full solver
- Advanced drift models (B/C/D)
- Story-level evolution

### Data Lab
- Multilanguage ingestion
- Entity linking
- Streaming data

### Embedding Generator
- Async encode()
- Model registry
- Quantized embeddings

---

# 7. File Index

```
docs/core/MASTER_ENGINE_AND_DATALAB_OVERVIEW.md

src/core/kaldra_master_engine.py
src/core/kaldra_logger.py
src/core/audit_trail.py

kaldra_data/ingestion/*
kaldra_data/preprocessing/*
kaldra_data/transformation/*
kaldra_data/export/*
```

---

# 8. Appendix: Example Full Pipeline

```python
from kaldra_data.ingestion.pdf_ingest import PDFIngest
from src.core.embedding_generator import EmbeddingGenerator
from src.core.kaldra_master_engine import KaldraMasterEngineV2

# 1. Data Lab → texto limpo
text = PDFIngest().load("META_Q1_2025.pdf").extract_text()

# 2. Embedding
gen = EmbeddingGenerator()
emb = gen.encode(text)[0]

# 3. Master Engine
engine = KaldraMasterEngineV2(d_ctx=emb.shape[-1])
signal = engine.infer_from_embedding(emb)

print(signal.summary())
```

---

**End of document**
