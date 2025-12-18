# KALDRA Core v2.3 — Embedding Generation & Cache Layer

**Version:** 2.3  
**Status:** Production-Ready  
**Last Updated:** 2025-11-26

---

## 1. Overview

Este documento descreve a **infraestrutura oficial de embeddings** do KALDRA Core v2.3, que substitui o antigo esquema de embeddings placeholder (hash / random) por um sistema:

* Multi-provider (Sentence Transformers, OpenAI, Cohere, Custom)
* Com camada de cache (memória + Redis opcional)
* Determinístico, configurável e extensível
* Sem quebrar nenhuma API existente do Master Engine

Esta camada é o ponto único de geração de embeddings textuais que poderão alimentar:

* `KaldraMasterEngineV2`
* Pipelines KALDRA-Alpha, GEO, Product, Safeguard
* Ferramentas de ingestão / Data Lab
* Futuras aplicações (Dashboard 4iam.ai, etc.)

---

## 2. Files & Components

### 2.1 `src/core/embedding_cache.py`

**Purpose:** Infraestrutura de cache de embeddings  
**Tamanho:** ~140 linhas

**Componentes principais:**

* `BaseEmbeddingCache`
* `InMemoryEmbeddingCache`
* `RedisEmbeddingCache`
* `make_embedding_cache_key(...)`
* `export_cache_to_disk(...)`

#### 2.1.1 `BaseEmbeddingCache`

Interface abstrata para caches de embedding:

```python
class BaseEmbeddingCache:
    def get(self, key: str) -> Optional[np.ndarray]:
        raise NotImplementedError
    
    def set(self, key: str, value: np.ndarray) -> None:
        raise NotImplementedError
```

Contratos:

* `get(key)` → `np.ndarray` ou `None`
* `set(key, value)` → armazena um vetor 1D ou 2D (float32)

#### 2.1.2 `InMemoryEmbeddingCache`

Cache em memória baseado em `dict`, ideal para:

* Desenvolvimento local
* Testes unitários / integração
* Pequenos experimentos

Características:

* `copy-on-store` (sempre salva uma cópia do array)
* Chaves arbitrárias (strings)
* 100% determinístico

Exemplo:

```python
from src.core.embedding_cache import InMemoryEmbeddingCache, make_embedding_cache_key
import numpy as np

cache = InMemoryEmbeddingCache()
key = make_embedding_cache_key("st", "all-MiniLM-L6-v2", ["Hello world"])

emb = np.random.randn(1, 384).astype(np.float32)
cache.set(key, emb)

cached = cache.get(key)
assert cached is not None
```

#### 2.1.3 `RedisEmbeddingCache`

Cache opcional, baseado em Redis:

* Requer `redis` instalado e um cliente do tipo `redis.Redis`
* Ideal para ambiente de produção / múltiplos processos

Comportamento:

* Serializa embeddings como `float32` → `tobytes()`
* Na leitura, reconstrói com `np.frombuffer(...)`
* Em caso de erro de desserialização, devolve `None` (cache miss silencioso)

#### 2.1.4 `make_embedding_cache_key(...)`

Gera uma chave determinística para um batch de textos:

```python
def make_embedding_cache_key(
    provider: str,
    model_name: str,
    texts: Sequence[str],
) -> str:
    ...
    return f"{provider}:{model_name}:{digest}"
```

Propriedades:

* Normaliza textos com `.strip()`
* Junta com `\n` e calcula `sha256`
* Mesmo `(provider, model_name, texts)` → mesma chave
* Ordem dos textos **importa** (batches diferentes → chaves diferentes)

#### 2.1.5 `export_cache_to_disk(...)`

Função utilitária para debugging:

```python
def export_cache_to_disk(cache: InMemoryEmbeddingCache, path: str | Path) -> None:
    ...
```

* Exporta conteúdo do `InMemoryEmbeddingCache` como dump binário simples
* Não é parte do pipeline de produção
* Útil para inspeção/offline debugging

---

### 2.2 `src/core/embedding_generator.py`

**Purpose:** Camada unificada de geração de embeddings  
**Tamanho:** ~260 linhas

**Componentes:**

* `EmbeddingConfig`
* `EmbeddingGenerator`

Suporte a múltiplos providers:

* `"sentence-transformers"` (principal, implementado)
* `"openai"` (skeleton via client injetado)
* `"cohere"` (skeleton via client injetado)
* `"custom"` (callable externo)

#### 2.2.1 `EmbeddingConfig`

Dataclass de configuração:

```python
@dataclass
class EmbeddingConfig:
    provider: str = "sentence-transformers"
    model_name: str = "all-MiniLM-L6-v2"
    normalize: bool = True
    batch_size: int = 16
    device: Optional[str] = None
    dim: Optional[int] = None
```

Principais campos:

* `provider`: `"sentence-transformers" | "openai" | "cohere" | "custom"`
* `model_name`: nome do modelo (ST, OpenAI, Cohere)
* `normalize`: aplica L2 norm se `True`
* `batch_size`: usado para ST
* `device`: `"cpu"`, `"cuda"`, etc. (ST)
* `dim`: dimensão esperada (ainda **não** estritamente validada)

#### 2.2.2 `EmbeddingGenerator`

Classe principal:

```python
class EmbeddingGenerator:
    def __init__(
        self,
        config: Optional[EmbeddingConfig] = None,
        cache: Optional[BaseEmbeddingCache] = None,
        openai_client: Any = None,
        cohere_client: Any = None,
        custom_encoder: Optional[Callable[[Sequence[str]], np.ndarray]] = None,
    ) -> None:
        ...
```

Responsabilidades:

* Normalizar input (`str` ou `Sequence[str]`)
* Integrar com cache (`BaseEmbeddingCache`)
* Carregar modelos ST lazy
* Encodar via provider selecionado
* Normalizar L2 se configurado
* Retornar sempre `np.ndarray[float32]` 2D `(N, D)`

##### API pública

```python
def encode(self, texts: TextLike) -> np.ndarray:
    ...
```

* `texts`: `str` ou lista de `str`
* Retorno: `np.ndarray`, shape `(N, D)`, dtype `float32`

Fluxo interno:

1. Normaliza textos (`_normalize_input`)
2. Gera chave de cache (`make_embedding_cache_key`)
3. Tenta `cache.get(key)`
   * Se hit: retorna embedding do cache
4. Senão, chama o provider apropriado:
   * `_encode_sentence_transformers`
   * `_encode_openai`
   * `_encode_cohere`
   * `_encode_custom`
5. Aplica `_postprocess` (2D + L2 norm)
6. Salva no cache com `cache.set(key, embeddings)`
7. Retorna embeddings

##### Providers suportados

**a) Sentence Transformers (ST)**

* Provider: `"sentence-transformers"`
* Requer `sentence-transformers` instalado
* Lazy load de `SentenceTransformer(model_name)`

```python
emb = self._st_model.encode(
    list(texts),
    batch_size=self.config.batch_size,
    convert_to_numpy=True,
    normalize_embeddings=False,
)
```

Se ST não estiver instalado:

```python
raise RuntimeError(
    "sentence-transformers is not installed. "
    "Install via `pip install sentence-transformers`."
)
```

**b) OpenAI (skeleton)**

* Provider: `"openai"`
* Requer `openai_client` injetado
* API esperada: `openai_client.embeddings.create(model=..., input=[...])`

```python
response = self.openai_client.embeddings.create(
    model=self.config.model_name,
    input=list(texts),
)
vectors = [np.array(item.embedding, dtype=np.float32) for item in response.data]
return np.vstack(vectors)
```

**c) Cohere (skeleton)**

* Provider: `"cohere"`
* Requer `cohere_client` injetado
* API esperada: `cohere_client.embed(texts=[...], model=...)`

```python
resp = self.cohere_client.embed(
    texts=list(texts),
    model=self.config.model_name,
)
vectors = [np.array(vec, dtype=np.float32) for vec in resp.embeddings]
return np.vstack(vectors)
```

**d) Custom**

* Provider: `"custom"`
* Requer `custom_encoder: (Sequence[str]) -> np.ndarray`

```python
arr = self.custom_encoder(list(texts))
return np.asarray(arr, dtype=np.float32)
```

---

## 3. Usage Patterns

### 3.1 Sentence Transformers (padrão)

```python
from src.core.embedding_generator import EmbeddingGenerator

generator = EmbeddingGenerator()  # defaults: ST + all-MiniLM-L6-v2
emb = generator.encode("The company reported strong earnings.")

print(emb.shape)       # (1, 384) típico para all-MiniLM
print(emb.dtype)       # float32
```

### 3.2 Custom Encoder (sem dependências externas)

```python
import numpy as np
from src.core.embedding_generator import EmbeddingGenerator, EmbeddingConfig

def my_encoder(texts):
    return np.random.randn(len(texts), 128).astype(np.float32)

config = EmbeddingConfig(provider="custom", dim=128)
generator = EmbeddingGenerator(config=config, custom_encoder=my_encoder)

emb = generator.encode(["Text 1", "Text 2"])
# shape: (2, 128)
```

### 3.3 Uso com cache em memória

```python
from src.core.embedding_cache import InMemoryEmbeddingCache
from src.core.embedding_generator import EmbeddingGenerator

cache = InMemoryEmbeddingCache()
generator = EmbeddingGenerator(cache=cache)

texts = ["Hello world"] * 100

# 1ª chamada — ST real (cache miss)
emb1 = generator.encode(texts)

# 2ª chamada — cache hit
emb2 = generator.encode(texts)
```

### 3.4 Integração futura com Master Engine

Quando você decidir plugar isso no pipeline real:

```python
from src.core.embedding_generator import EmbeddingGenerator
from src.core.kaldra_master_engine import KaldraMasterEngineV2

generator = EmbeddingGenerator()  # ST, 384 dims
text = "The company reported strong earnings growth."

emb = generator.encode(text)  # shape: (1, 384)
engine = KaldraMasterEngineV2(d_ctx=384)

signal = engine.infer_from_embedding(emb[0])
```

> 🔎 **Importante:** Por enquanto, o Master Engine ainda aceita qualquer `np.ndarray` (como antes). O `EmbeddingGenerator` é **aditivo** — não quebra nada.

---

## 4. Design Decisions

### 4.1 Dependências opcionais

* `sentence-transformers`, `openai`, `cohere` **não** são hard deps
* Import do repositório funciona mesmo sem essas libs
* Erro só acontece quando você **usa** o provider correspondente

Benefício:

* Repositório permanece leve
* Usuário escolhe qual stack quer instalar
* Facilita ambientes "mínimos" (teste, CI, etc.)

### 4.2 Cache em nível de batch

* A chave considera todos os textos do batch
* Mesmo batch → mesmo key → cache hit
* Alterar um texto → nova key → cache miss

É simples e robusto, mas:

* Não faz deduplicação por texto individual
* É a melhor escolha inicial pro uso típico do KALDRA (batches coerentes por análise)

### 4.3 L2 Normalization

* Padrão: `normalize=True`
* Motivação:
  * Facilita uso com cosine similarity
  * Torna embeddings comparáveis entre si
* Pode ser desativado caso o modelo já normalize internamente ou se o consumidor preferir trabalhar com vetores crus

---

## 5. Validation & Tests

### 5.1 Imports

```bash
python3 -c "from src.core.embedding_cache import InMemoryEmbeddingCache; print('✅')"
python3 -c "from src.core.embedding_generator import EmbeddingGenerator; print('✅')"
# Ambos importam sem erros
```

### 5.2 Test Suite Existente

```bash
pytest tests/meta/ tests/integration/test_full_pipeline.py -v
# Resultado: 35 passed em ~4.3s
```

* Nenhum teste antigo foi quebrado
* Nenhuma lógica de Δ144 / TW369 / Kindra foi alterada

### 5.3 Exemplos

Arquivo criado:

* `examples/embedding_usage_examples.py`

Executando:

```bash
python3 examples/embedding_usage_examples.py
# Todos os exemplos concluem com sucesso
# Custom encoder: determinístico ✅
# Cache keys: consistentes ✅
```

---

## 6. Known Limitations

1. **Cache em nível de batch**
   * Mudar 1 texto no batch → nova key
   * Para uso ultra-fino, seria necessário cache por texto

2. **`config.dim` não é validado estritamente**
   * Hoje é apenas informativo
   * Se a dimensão do modelo mudar, isso pode estourar em outro lugar

3. **Redis sem TTL / eviction**
   * Cache cresce indefinidamente
   * Precisa de política de TTL/eviction em versões futuras

---

## 7. Future Implementations & Enhancements (v2.4+)

> Marcar estes itens explicitamente como **Future Implementation / Enhancement** no roadmap.

### 7.1 Future Implementation — Dimension Validation

* **Strict mode**:
  * Se `config.dim` estiver definido e `arr.shape[1] != dim` → `RuntimeError`
* **Truncate/pad mode**:
  * Possibilidade de adaptar automaticamente a dimensão (ex: cortar ou preencher com zeros)

### 7.2 Future Enhancement — Async & Streaming

* `async def encode_async(...)` para integração com pipelines assíncronos
* Suporte a processar grandes corpora com streaming:
  * Iterador de embeddings
  * Backpressure

### 7.3 Future Enhancement — Model Registry

* Registry interno com perfis:
  * `"kaldra_default_local"`
  * `"kaldra_high_quality_cloud"`
* Auto-download e cache de modelos ST
* Metadados: dim, custo estimado, latência estimada

### 7.4 Future Enhancement — Metrics

* Integração com logger/metrics:
  * Cache hit/miss
  * Latência de encoding
  * Contador de chamadas por provider
* Exposição via Prometheus / logging estruturado

---

## 8. Status & Versioning

* **Implementation Date:** 2025-11-26
* **KALDRA Core Version:** v2.3
* **Module Status:** ✅ Complete / Production-Ready
* **Breaking Changes:** Nenhuma
* **Dependências extras:** Todas opcionais

Este documento serve como **referência oficial** da camada de Embedding & Cache no KALDRA Core, e como base para a futura integração com:

* KALDRA-Alpha / GEO / Product / Safeguard
* 4iam.ai Dashboard
* Módulos de análise narrativa em tempo real.
