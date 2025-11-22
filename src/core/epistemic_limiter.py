from dataclasses import dataclass
import numpy as np
import torch
from typing import Optional

@dataclass
class EpistemicDecision:
    status: str            # "OK" | "INCONCLUSIVO"
    delegate: bool
    archetype_idx: Optional[int] = None
    confidence: Optional[float] = None

class EpistemicLimiter:
    """
    Camada τ (Tau): Limitador Epistêmico.
    
    Decide se o sistema está confiante o suficiente para 'manifestar'
    um arquétipo como diagnóstico final, ou se deve delegar para revisão humana
    ou marcar como inconclusivo.
    
    O parâmetro tau (τ) define o limiar de corte de confiança (entropia inversa).
    """

    def __init__(self, tau: float = 0.65):
        self.tau = float(tau)

    def from_probs(self, probs: np.ndarray) -> EpistemicDecision:
        """
        Avalia um vetor de probabilidades (numpy).
        """
        probs = np.asarray(probs, dtype=float)
        idx = int(probs.argmax())
        conf = float(probs[idx])
        
        if conf < self.tau:
            return EpistemicDecision(status="INCONCLUSIVO", delegate=True)
            
        return EpistemicDecision(
            status="OK",
            delegate=False,
            archetype_idx=idx,
            confidence=conf,
        )

    def from_tensor(self, probs: torch.Tensor) -> EpistemicDecision:
        """
        Avalia um tensor de probabilidades (pytorch).
        """
        with torch.no_grad():
            # Se for batch, pega o primeiro ou assume input single
            if probs.dim() > 1:
                probs = probs[0]
                
            return self.from_probs(probs.cpu().numpy())
