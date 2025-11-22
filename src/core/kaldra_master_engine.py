from dataclasses import dataclass
from typing import Any, Optional

import numpy as np
import torch

from src.archetypes.delta144_engine import Delta144Engine
from src.kindras.kindra_cultural_mod import KaldraKindraCulturalMod
from src.tw369.oracle_tw_painleve import TWPainleveOracle, TWConfig, TWStats
from src.core.epistemic_limiter import EpistemicLimiter, EpistemicDecision

@dataclass
class KaldraSignal:
    """Sinal final do KALDRA Master Engine."""
    archetype_probs: np.ndarray
    tw_trigger: bool
    tw_stats: Optional[TWStats]
    epistemic: EpistemicDecision

class KaldraMasterEngineV2:
    """
    Orquestrador mínimo do KALDRA v2.0:
    - recebe texto ou vetor de contexto
    - roda Δ144 (Base)
    - aplica Kindra 3×48 (Modulação Cultural)
    - passa pelo oracle TW (Detecção de Anomalia)
    - aplica τ / EpistemicLimiter (Segurança Epistêmica)
    """

    def __init__(
        self,
        delta_engine: Optional[Delta144Engine] = None,
        d_ctx: int = 256,
        tau: float = 0.65,
        tw_config: Optional[TWConfig] = None,
    ):
        self.delta = delta_engine or Delta144Engine.from_default_files()
        self.kindra_mod = KaldraKindraCulturalMod(d_ctx=d_ctx)
        self.tau_layer = EpistemicLimiter(tau=tau)
        self.tw_oracle = TWPainleveOracle(config=tw_config or TWConfig())

    def infer_from_embedding(
        self,
        embedding: np.ndarray,
        tw_window: Optional[np.ndarray] = None,
    ) -> KaldraSignal:
        """
        Realiza a inferência completa.
        
        embedding: vetor de contexto (d_ctx)
        tw_window: janela opcional de sinais para o oracle TW (T, m)
        """
        # 1) Δ144 — get base archetype distribution
        # Usa o método infer_from_vector que adicionamos ao Delta144Engine
        result = self.delta.infer_from_vector(embedding)
        
        # Se result.probs for None (caso antigo), cria uniforme
        if result.probs is None:
            base_probs = np.ones(144) / 144.0
        else:
            base_probs = np.asarray(result.probs, dtype=float)

        # 2) Kindra modulation (usa torch internamente)
        ctx = torch.tensor(embedding, dtype=torch.float32).unsqueeze(0)
        probs_t = torch.tensor(base_probs, dtype=torch.float32).unsqueeze(0)
        
        # Aplica modulação cultural
        modulated = self.kindra_mod(probs_t, ctx, apply_softmax=True)[0]
        modulated_np = modulated.detach().cpu().numpy()

        # 3) TW oracle (se janela fornecida)
        tw_trigger = False
        tw_stats = None
        if tw_window is not None:
            tw_trigger, tw_stats = self.tw_oracle.detect(tw_window)

        # 4) τ layer (Epistemic Limiter)
        epistemic = self.tau_layer.from_probs(modulated_np)

        return KaldraSignal(
            archetype_probs=modulated_np,
            tw_trigger=tw_trigger,
            tw_stats=tw_stats,
            epistemic=epistemic,
        )
