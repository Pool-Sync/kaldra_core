"""
Tests for MetaRouter routing decisions.
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from meta.meta_router import MetaRouter, RoutingDecision, decide_route
from meta.meta_engine_base import MetaSignal


def test_meta_router_evaluate():
    """Test that MetaRouter evaluates all engines."""
    router = MetaRouter()
    
    # Minimal signal
    signal = {
        "delta12": None,
        "delta144": None,
        "tw_state": None,
        "bias_score": 0.0,
        "drift_history": []
    }
    
    results = router.evaluate(signal)
    
    # Should have results from all 3 engines
    assert "nietzsche" in results
    assert "campbell" in results
    assert "aurelius" in results
    
    # All should be MetaSignals
    for signal_result in results.values():
        assert isinstance(signal_result, MetaSignal)


def test_routing_decision_ordeal_to_safeguard():
    """Test that ordeal stage routes to Safeguard."""
    meta_signals = {
        "campbell": MetaSignal(
            name="campbell",
            score=0.8,
            label="ordeal",
            details={}
        ),
        "nietzsche": MetaSignal(name="nietzsche", score=0.5, label="will_to_power_moderate", details={}),
        "aurelius": MetaSignal(name="aurelius", score=0.5, label="on_the_edge", details={})
    }
    
    decision = decide_route(meta_signals)
    
    assert isinstance(decision, RoutingDecision)
    assert decision.dominant_app == "safeguard"
    assert decision.confidence > 0.6


def test_routing_decision_high_will_to_alpha():
    """Test that high will to power routes to Alpha."""
    meta_signals = {
        "nietzsche": MetaSignal(
            name="nietzsche",
            score=0.9,
            label="will_to_power_high",
            details={}
        ),
        "campbell": MetaSignal(name="campbell", score=0.5, label="ordinary_world", details={}),
        "aurelius": MetaSignal(name="aurelius", score=0.6, label="on_the_edge", details={})
    }
    
    decision = decide_route(meta_signals)
    
    assert decision.dominant_app == "alpha"
    assert decision.confidence > 0.7


def test_routing_decision_regulated_to_geo():
    """Test that regulated state routes to Geo."""
    meta_signals = {
        "aurelius": MetaSignal(
            name="aurelius",
            score=0.85,
            label="regulated",
            details={}
        ),
        "nietzsche": MetaSignal(name="nietzsche", score=0.5, label="will_to_power_moderate", details={}),
        "campbell": MetaSignal(name="campbell", score=0.5, label="ordinary_world", details={})
    }
    
    decision = decide_route(meta_signals)
    
    assert decision.dominant_app == "geo"
    assert decision.confidence > 0.7


def test_routing_decision_default_kaldra():
    """Test that ambiguous signals default to KALDRA."""
    meta_signals = {
        "nietzsche": MetaSignal(name="nietzsche", score=0.5, label="will_to_power_moderate", details={}),
        "campbell": MetaSignal(name="campbell", score=0.5, label="ordinary_world", details={}),
        "aurelius": MetaSignal(name="aurelius", score=0.5, label="on_the_edge", details={})
    }
    
    decision = decide_route(meta_signals)
    
    assert decision.dominant_app == "kaldra"


def test_meta_router_fail_safe():
    """Test that MetaRouter fails safely on engine errors."""
    router = MetaRouter()
    
    # Signal that might cause errors
    signal = {"bad": "data"}
    
    results = router.evaluate(signal)
    
    # Should still return results for all engines
    assert len(results) == 3
    
    # All should be valid MetaSignals (even if error)
    for signal_result in results.values():
        assert isinstance(signal_result, MetaSignal)
        assert 0.0 <= signal_result.score <= 1.0
