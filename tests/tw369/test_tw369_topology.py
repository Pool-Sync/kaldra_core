"""
Unit tests for TW369 Topological Deepening (v3.2).

Tests topological analysis components:
- Painlevé smoothing
- Tracy-Widom severity
- Volatility computation  
- Regime classification
- Trajectory building
- Turning point detection
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Import using src. prefix like other TW369 tests
from src.tw369.drift_history import DriftHistory, DriftSample
from src.tw369.drift_topology import TW369Topology
from src.unification.states.unified_state import DriftContext, DriftPoint, TurningPoint




class TestPainleveSmoothing:
    """Test Painlevé II smoothing functionality."""
    
    def test_smoothing_reduces_variance(self):
        """Smoothed series should have lower or equal variance."""
        topology = TW369Topology()
        
        # Noisy series
        noisy = [1.0, 0.5, 1.5, 0.8, 1.2, 0.9, 1.4, 0.7]
        
        smoothed = topology.smooth_with_painleve(noisy)
        
        # Compute variance
        def variance(series):
            mean = sum(series) / len(series)
            return sum((x - mean) ** 2 for x in series) / len(series)
        
        var_noisy = variance(noisy)
        var_smoothed = variance(smoothed)
        
        # Smoothed should have lower or equal variance
        assert var_smoothed <= var_noisy + 0.01  # Small tolerance
    
    def test_smoothing_empty_series(self):
        """Empty series should return empty."""
        topology = TW369Topology()
        assert topology.smooth_with_painleve([]) == []
    
    def test_smoothing_preserves_length(self):
        """Smoothed series should have same length as input."""
        topology = TW369Topology()
        series = [1.0, 2.0, 3.0, 4.0, 5.0]
        smoothed = topology.smooth_with_painleve(series)
        assert len(smoothed) == len(series)


class TestTracyWidomSeverity:
    """Test Tracy-Widom severity scoring."""
    
    def test_severity_monotonic_in_lambda(self):
        """Higher lambda_max should yield higher severity."""
        topology = TW369Topology()
        
        lambdas = [0.5, 1.0, 2.0, 5.0]
        severities = [
            topology.compute_tracy_widom_severity(lam, mean=0.0, std=1.0)
            for lam in lambdas
        ]
        
        # Check monotonicity
        for i in range(len(severities) - 1):
            assert severities[i] < severities[i + 1], \
                f"Severity not monotonic: {severities[i]} >= {severities[i+1]}"
    
    def test_severity_bounds(self):
        """Severity should be in [0, 1]."""
        topology = TW369Topology()
        
        test_lambdas = [-2.0, -1.0, 0.0, 0.5, 1.0, 2.0, 5.0, 10.0]
        
        for lam in test_lambdas:
            severity = topology.compute_tracy_widom_severity(lam, mean=0.0, std=1.0)
            assert 0.0 <= severity <= 1.0, f"Severity {severity} out of bounds for lambda={lam}"
    
    def test_severity_zero_std_returns_zero(self):
        """Zero std should return severity of 0."""
        topology = TW369Topology()
        severity = topology.compute_tracy_widom_severity(5.0, mean=0.0, std=0.0)
        assert severity == 0.0


class TestVolatility:
    """Test volatility computation."""
    
    def test_volatility_zero_for_constant(self):
        """Constant series should have zero volatility."""
        topology = TW369Topology()
        
        constant = [1.0, 1.0, 1.0, 1.0, 1.0]
        volatility = topology.compute_volatility(constant)
        
        assert abs(volatility) < 1e-6, f"Expected ~0, got {volatility}"
    
    def test_volatility_increases_with_variance(self):
        """Higher variance should yield higher volatility."""
        topology = TW369Topology()
        
        low_var = [1.0, 1.1, 0.9, 1.05, 0.95]
        high_var = [1.0, 3.0, 0.5, 2.5, 0.8]
        
        vol_low = topology.compute_volatility(low_var)
        vol_high = topology.compute_volatility(high_var)
        
        assert vol_high > vol_low
    
    def test_volatility_empty_or_single(self):
        """Empty or single-element series should return 0."""
        topology = TW369Topology()
        
        assert topology.compute_volatility([]) == 0.0
        assert topology.compute_volatility([5.0]) == 0.0


class TestRegimeClassification:
    """Test regime classification logic."""
    
    def test_classify_stable(self):
        """Low severity + low volatility = STABLE."""
        topology = TW369Topology()
        
        regime = topology.classify_regime(severity=0.1, volatility=0.05)
        assert regime == "STABLE"
    
    def test_classify_volatile(self):
        """High severity (but < critical) = VOLATILE."""
        topology = TW369Topology(severe_threshold=0.85, critical_threshold=0.95)
        
        regime = topology.classify_regime(severity=0.90, volatility=0.2)
        assert regime == "VOLATILE"
    
    def test_classify_critical(self):
        """Very high severity = CRITICAL."""
        topology = TW369Topology(critical_threshold=0.95)
        
        regime = topology.classify_regime(severity=0.98, volatility=0.5)
        assert regime == "CRITICAL"
    
    def test_classify_transition(self):
        """Low severity but high volatility = TRANSITION."""
        topology = TW369Topology()
        
        regime = topology.classify_regime(severity=0.5, volatility=0.5)
        assert regime == "TRANSITION"


class TestDriftContext:
    """Test DriftContext building from history."""
    
    def test_build_creates_trajectory(self):
        """DriftContext should have trajectory with all samples."""
        topology = TW369Topology()
        history = DriftHistory(max_len=100)
        
        # Add 10 samples
        for i in range(10):
            history.add_sample(
                drift_value=float(i) * 0.1,
                tracy_widom_severity=0.5,
                regime="STABLE"
            )
        
        ctx = topology.build_drift_context(
            history=history,
            latest_lambda_max=1.0
        )
        
        assert len(ctx.trajectory) == 10
        assert all(isinstance(p, DriftPoint) for p in ctx.trajectory)
    
    def test_build_detects_turning_points(self):
        """DriftContext should detect regime transitions."""
        topology = TW369Topology()
        history = DriftHistory(max_len=100)
        
        # Sequence with regime changes
        regimes = ["STABLE", "STABLE", "VOLATILE", "VOLATILE", "CRITICAL"]
        
        for i, regime in enumerate(regimes):
            history.add_sample(
                drift_value=float(i) * 0.2,
                tracy_widom_severity=0.5,
                regime=regime
            )
        
        ctx = topology.build_drift_context(
            history=history,
            latest_lambda_max=2.0
        )
        
        # Should detect STABLE→VOLATILE and VOLATILE→CRITICAL
        assert len(ctx.turning_points) >= 2
        assert all(isinstance(tp, TurningPoint) for tp in ctx.turning_points)
        
        # Check first transition
        assert ctx.turning_points[0].from_regime == "STABLE"
        assert ctx.turning_points[0].to_regime == "VOLATILE"
    
    def test_build_empty_history(self):
        """Empty history should return minimal context."""
        topology = TW369Topology()
        history = DriftHistory(max_len=100)
        
        ctx = topology.build_drift_context(
            history=history,
            latest_lambda_max=0.0
        )
        
        assert ctx.drift_metric == 0.0
        assert ctx.regime == "UNKNOWN"
        assert len(ctx.trajectory) == 0
        assert len(ctx.turning_points) == 0
    
    def test_build_populates_all_fields(self):
        """DriftContext should have all topological fields set."""
        topology = TW369Topology()
        history = DriftHistory(max_len=100)
        
        # Add diverse samples
        for i in range(20):
            history.add_sample(
                drift_value=float(i) * 0.05,
                tracy_widom_severity=0.3 + i * 0.02,
                regime="STABLE" if i < 10 else "VOLATILE"
            )
        
        ctx = topology.build_drift_context(
            history=history,
            latest_lambda_max=1.5
        )
        
        # Check all fields populated
        assert isinstance(ctx.drift_metric, float)
        assert isinstance(ctx.regime, str)
        assert isinstance(ctx.volatility, float)
        assert isinstance(ctx.tracy_widom_severity, float)
        assert isinstance(ctx.painleve_smoothed, bool)
        assert isinstance(ctx.trajectory, list)
        assert isinstance(ctx.turning_points, list)


class TestDriftHistory:
    """Test DriftHistory storage."""
    
    def test_add_and_retrieve_samples(self):
        """Should store and retrieve samples correctly."""
        history = DriftHistory(max_len=10)
        
        history.add_sample(1.0, 0.5, "STABLE")
        history.add_sample(1.5, 0.6, "VOLATILE")
        
        samples = history.get_samples()
        assert len(samples) == 2
        assert samples[0].drift_value == 1.0
        assert samples[1].drift_value == 1.5
    
    def test_max_length_enforcement(self):
        """Should respect max_len and drop oldest."""
        history = DriftHistory(max_len=5)
        
        # Add 10 samples
        for i in range(10):
            history.add_sample(float(i), 0.5, "STABLE")
        
        samples = history.get_samples()
        assert len(samples) == 5
        # Should keep last 5 (values 5, 6, 7, 8, 9)
        assert samples[0].drift_value == 5.0
        assert samples[-1].drift_value == 9.0
    
    def test_is_empty(self):
        """is_empty should work correctly."""
        history = DriftHistory()
        
        assert history.is_empty()
        
        history.add_sample(1.0, 0.5, "STABLE")
        assert not history.is_empty()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
