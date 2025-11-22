import numpy as np
import torch
import pytest
from src.core.epistemic_limiter import EpistemicLimiter

def test_epistemic_limiter_numpy():
    limiter = EpistemicLimiter(tau=0.8)
    
    # Caso confiante
    probs_high = np.zeros(10)
    probs_high[0] = 0.9
    decision = limiter.from_probs(probs_high)
    assert decision.status == "OK"
    assert decision.delegate is False
    assert decision.archetype_idx == 0
    
    # Caso incerto
    probs_low = np.zeros(10)
    probs_low[0] = 0.5
    probs_low[1] = 0.4
    decision = limiter.from_probs(probs_low)
    assert decision.status == "INCONCLUSIVO"
    assert decision.delegate is True

def test_epistemic_limiter_torch():
    limiter = EpistemicLimiter(tau=0.6)
    
    probs = torch.tensor([0.1, 0.2, 0.7, 0.0])
    decision = limiter.from_tensor(probs)
    
    assert decision.status == "OK"
    assert decision.confidence == pytest.approx(0.7, abs=1e-5)
