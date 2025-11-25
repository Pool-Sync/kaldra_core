import pytest
from src.tw369.painleve.painleve_filter import painleve_filter

class TestPainleveFilter:
    def test_filter_basic(self):
        # Small input should result in small output
        val = 0.1
        filtered = painleve_filter(val)
        assert isinstance(filtered, float)
        assert abs(filtered) < 1.0

    def test_filter_clamping_positive(self):
        # Large input should be clamped
        val = 100.0
        filtered = painleve_filter(val)
        assert filtered == 1.0

    def test_filter_clamping_negative(self):
        # Large negative input should be clamped
        val = -100.0
        filtered = painleve_filter(val)
        assert filtered == -1.0

    def test_filter_zero(self):
        # Zero input
        val = 0.0
        filtered = painleve_filter(val)
        # If u0=0, v0=0, alpha=0 -> u''=0 -> u(x)=0
        assert filtered == 0.0
