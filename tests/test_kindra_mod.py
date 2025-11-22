import torch
import pytest
from src.kindras.kindra_cultural_mod import KaldraKindraCulturalMod

def test_kindra_mod_initialization():
    mod = KaldraKindraCulturalMod(d_ctx=128)
    assert mod.ctx_norm.normalized_shape == (128,)
    assert len(mod.W) == 3
    assert len(mod.M) == 3

def test_kindra_mod_forward_shape():
    mod = KaldraKindraCulturalMod(d_ctx=64)
    batch_size = 2
    
    # Fake inputs
    probs = torch.softmax(torch.randn(batch_size, 144), dim=-1)
    ctx = torch.randn(batch_size, 64)
    
    out = mod(probs, ctx)
    
    assert out.shape == (batch_size, 144)
    # Check if it sums to 1 (softmax applied)
    assert torch.allclose(out.sum(dim=-1), torch.ones(batch_size), atol=1e-5)

def test_kindra_mod_values():
    mod = KaldraKindraCulturalMod(d_ctx=64)
    probs = torch.ones(1, 144) / 144.0
    ctx = torch.zeros(1, 64) # Contexto zero
    
    out = mod(probs, ctx)
    # Mesmo com contexto zero, os pesos e bias internos geram alguma modulação,
    # mas não deve quebrar.
    assert not torch.isnan(out).any()
