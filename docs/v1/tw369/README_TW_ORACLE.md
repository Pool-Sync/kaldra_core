# 🔮 TW-Painlevé Oracle

O **TW-Painlevé Oracle** é um detector de anomalias de alta sensibilidade baseado na teoria de Matrizes Aleatórias (Random Matrix Theory - RMT). Ele monitora a coerência sistêmica dos sinais KALDRA analisando o espectro de autovalores da matriz de correlação dos sinais.

## Fundamentação Teórica

A distribuição do maior autovalor ($\lambda_{max}$) de matrizes aleatórias de covariância (Wishart) converge para a **Distribuição de Tracy-Widom** (TW).

Quando $\lambda_{max}$ excede o limite crítico previsto pela TW (ajustado pela equação de Painlevé II), isso indica uma **quebra de simetria** ou **transição de fase**: o sistema deixou de ser ruído aleatório e formou um padrão emergente forte (um "cisne negro" ou sinal de alta convicção).

## Uso

```python
from src.tw369.oracle_tw_painleve import TWPainleveOracle, TWConfig
import numpy as np

# Configuração
config = TWConfig(window_size=50, alpha=0.99)
oracle = TWPainleveOracle(config)

# Janela de dados (Tempo x Features)
# Ex: 50 amostras temporais de 16 sinais monitorados
window = np.random.randn(50, 16)

# Detecção
trigger, stats = oracle.detect(window)

if trigger:
    print(f"⚠️ ANOMALIA DETECTADA! Lambda: {stats.lambda_max:.2f} > Threshold: {stats.threshold:.2f}")
else:
    print("Sistema estável (regime de ruído).")
```

## Integração no KALDRA

O Oracle atua como um **gatekeeper de volatilidade**:
1. Recebe fluxo de vetores de embedding ou scores de arquétipos.
2. Calcula a coerência espectral.
3. Se `trigger == True`, sinaliza que o estado atual é estatisticamente significativo e não fruto do acaso.
