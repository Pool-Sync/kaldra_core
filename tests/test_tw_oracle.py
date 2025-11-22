import numpy as np
import pytest
from src.tw369.oracle_tw_painleve import TWPainleveOracle, TWConfig

def test_tw_oracle_initialization():
    config = TWConfig(window_size=50, alpha=0.95)
    oracle = TWPainleveOracle(config)
    assert oracle.config.window_size == 50
    assert oracle.config.alpha == 0.95

def test_compute_covariance():
    oracle = TWPainleveOracle()
    # Matrix (T=10, N=5)
    window = np.random.randn(10, 5)
    cov = oracle.compute_covariance(window)
    assert cov.shape == (5, 5)
    # Covariance matrix should be symmetric
    assert np.allclose(cov, cov.T)

def test_tracy_widom_threshold():
    oracle = TWPainleveOracle()
    lower, upper = oracle.tracy_widom_threshold(m=100, alpha=0.99)
    assert lower < upper
    assert lower > 0

def test_detect_anomaly():
    oracle = TWPainleveOracle()
    # Normal noise
    window = np.random.randn(100, 20)
    trigger, stats = oracle.detect(window)
    
    # With random noise, it shouldn't trigger usually, but it's probabilistic.
    # We just check the structure of the output.
    assert isinstance(trigger, bool)
    assert stats is not None
    assert stats.lambda_max > 0
