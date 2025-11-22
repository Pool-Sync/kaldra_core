# 🧬 Kindra Cultural Modulation Layer (3×48)

A **Kindra Cultural Modulation Layer** é um módulo neural (PyTorch) que aplica um viés cultural dinâmico sobre a distribuição de estados da Δ144.

Ela conecta o contexto semântico (embedding) aos 144 estados arquetípicos através da matriz intermediária de **Kindras** (Vetores Culturais).

## Arquitetura

A camada opera em três planos vibracionais (3, 6, 9), cada um contendo 48 vetores Kindra.

```mermaid
graph LR
    Context[Context Embedding] -->|Norm| NormContext
    NormContext -->|Linear| Kindras3[Kindras Plano 3 (48)]
    NormContext -->|Linear| Kindras6[Kindras Plano 6 (48)]
    NormContext -->|Linear| Kindras9[Kindras Plano 9 (48)]
    
    Kindras3 -->|Proj M3| Gain3[Ganho Δ144 (144)]
    Kindras6 -->|Proj M6| Gain6[Ganho Δ144 (144)]
    Kindras9 -->|Proj M9| Gain9[Ganho Δ144 (144)]
    
    Gain3 --> Sum((+))
    Gain6 --> Sum
    Gain9 --> Sum
    
    BaseProbs[Δ144 Base Probs] --> Mult((x))
    Sum -->|Gain Total| Mult
    Mult -->|Softmax| FinalProbs[Probabilidades Moduladas]
```

## Parâmetros

- **`d_ctx`**: Dimensão do vetor de contexto de entrada (default: 256).
- **`W`**: Pesos que mapeiam Contexto → 48 Kindras (por plano).
- **`M`**: Matriz de projeção 48 Kindras → 144 Estados (por plano).
- **`lambda`**: Pesos escalares aprendíveis que controlam a influência de cada plano (3, 6, 9).

## Uso

```python
import torch
from src.kindras.kindra_cultural_mod import KaldraKindraCulturalMod

# Inicialização
mod_layer = KaldraKindraCulturalMod(d_ctx=256)

# Dados simulados
batch_size = 1
probs_base = torch.softmax(torch.randn(batch_size, 144), dim=-1)
context = torch.randn(batch_size, 256)

# Forward pass
probs_modulated = mod_layer(probs_base, context)

print(probs_modulated.shape) # torch.Size([1, 144])
```
