# KALDRA CORE → Frontend 4iam.ai — Handoff

## Fluxo

1. Frontend envia `POST /engine/kaldra/signal` com `{ "text": "..." }`.
2. API Gateway chama `generate_kaldra_signal(text)`.
3. Resposta é retornada ao frontend com o schema `kaldra_signal.schema.json`.

## Campos chave para UI

### `tw_regime`
- **Tipo**: `"STABLE" | "CRITICAL" | "UNSTABLE"`
- **UI**: Usar para status visual (cores, ícones)
  - STABLE: Verde 🟢
  - CRITICAL: Amarelo 🟡
  - UNSTABLE: Vermelho 🔴

### `bias_score`
- **Tipo**: `number` (0.0 - 1.0)
- **UI**: Slider/medidor de intensidade
- **Interpretação**:
  - < 0.3: Neutral
  - 0.3 - 0.6: Moderate
  - 0.6 - 0.8: High
  - > 0.8: Extreme

### `kindra_distribution`
- **Tipo**: `Record<string, number>`
- **UI**: Gráficos de barras / radar chart
- **Exemplo**: `{ "K01": 0.45, "K02": 0.35, "K03": 0.20 }`

### `confidence`
- **Tipo**: `number` (0.0 - 1.0)
- **UI**: Indicação global de confiança (badge, percentage)

### `explanation`
- **Tipo**: `string`
- **UI**: Texto curto para tooltips / descrição do sinal

### `meta_modifiers`
- **Tipo**: `{ strength: number[], journey: number[], discipline: number[] }`
- **UI**: Gráficos de linha / heatmaps (opcional, avançado)

## Tipos para TypeScript

```typescript
export type TWRegime = "STABLE" | "CRITICAL" | "UNSTABLE";

export interface KaldraSignal {
  archetype: string;
  delta_state: string;
  tw_regime: TWRegime;
  kindra_distribution: Record<string, number>;
  bias_score: number;
  bias_label?: string;
  meta_modifiers: {
    strength: number[];
    journey: number[];
    discipline: number[];
  };
  confidence: number;
  explanation: string;
  narrative_risk?: "low" | "medium" | "high"; // Safeguard only
}

export interface SignalRequest {
  text: string;
}

export interface SignalResponse {
  signal: KaldraSignal;
  timestamp?: string;
  request_id?: string;
}
```

## Exemplo de Integração (React)

```typescript
import { useState } from 'react';
import type { KaldraSignal } from '@/types/kaldra';

export function useKaldraSignal() {
  const [loading, setLoading] = useState(false);
  const [signal, setSignal] = useState<KaldraSignal | null>(null);
  const [error, setError] = useState<string | null>(null);

  const generateSignal = async (text: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/engine/kaldra/signal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      
      if (!response.ok) throw new Error('Failed to generate signal');
      
      const data = await response.json();
      setSignal(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return { signal, loading, error, generateSignal };
}
```

## Componentes UI Sugeridos

### 1. Signal Status Badge
```tsx
<Badge color={signal.tw_regime === 'STABLE' ? 'green' : 
               signal.tw_regime === 'CRITICAL' ? 'yellow' : 'red'}>
  {signal.tw_regime}
</Badge>
```

### 2. Bias Meter
```tsx
<Progress value={signal.bias_score * 100} />
<Text>{signal.bias_label}</Text>
```

### 3. Confidence Indicator
```tsx
<CircularProgress value={signal.confidence * 100} />
```

### 4. Kindra Distribution Chart
```tsx
<BarChart data={Object.entries(signal.kindra_distribution)} />
```

## Mock Data para Desenvolvimento

Usar `mock_data/sample_signals.json` para desenvolvimento local sem backend.

## Próximos Passos

1. Implementar API Gateway no `kaldra_api`
2. Adicionar autenticação e rate limiting
3. Criar componentes React para visualização
4. Integrar com dashboard 4iam.ai
5. Adicionar testes E2E
