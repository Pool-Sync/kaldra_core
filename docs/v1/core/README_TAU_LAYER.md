# 🛡️ Camada τ (Tau) / Epistemic Limiter

A **Camada τ** (Tau Layer) é o mecanismo de segurança epistêmica do KALDRA. Ela impede que o sistema alucine certezas onde só existe ambiguidade.

## Função

Ela atua como um filtro final sobre a distribuição de probabilidades gerada pelo Master Engine.

Se a confiança do arquétipo dominante ($P_{max}$) for menor que o limiar $\tau$, o sistema se recusa a emitir um diagnóstico fechado e marca o sinal como **INCONCLUSIVO**.

## Lógica

$$
\text{Decisão} = \begin{cases} 
\text{MANIFESTAR}, & \text{se } P_{max} \ge \tau \\
\text{DELEGAR}, & \text{se } P_{max} < \tau 
\end{cases}
$$

## Uso

```python
from src.core.epistemic_limiter import EpistemicLimiter

# Inicializa com limiar de 65%
limiter = EpistemicLimiter(tau=0.65)

# Probabilidades vindas do engine
probs = [0.1, 0.2, 0.6, 0.1] # Max é 0.6 (60%)

decision = limiter.from_probs(probs)

if decision.delegate:
    print("Sinal fraco. Revisão humana necessária.")
else:
    print(f"Arquétipo confirmado: {decision.archetype_idx} com {decision.confidence:.2f}")
```

## Integração

No **Master Engine**, a Camada τ é a última etapa antes da emissão do `KaldraSignal`. Isso garante que apenas sinais robustos acionem triggers em sistemas downstream (como trades ou alertas de segurança).
