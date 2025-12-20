"""
Unit tests for Router (KALDRA v3.0).
"""

import sys

import pytest

sys.path.insert(0, "/Users/niki/Desktop/kaldra_core")

from kaldra_engine.unification.router import UnifiedRouter


def test_router_signal_mode():
    """Test signal mode routing."""
    router = UnifiedRouter()
    config = router.route("test", "signal", {})

    assert config.mode == "signal"
    assert config.skip_story
    assert "story" not in config.stages


def test_router_full_mode():
    """Test full mode routing."""
    router = UnifiedRouter()
    config = router.route("test", "full", {})

    assert config.mode == "full"
    assert len(config.stages) == 6


def test_router_safety_first_mode():
    """Test safety-first mode routing."""
    router = UnifiedRouter()
    config = router.route("test", "safety-first", {})

    assert config.mode == "safety-first"
    assert config.strict_safety


def test_router_exploratory_mode():
    """Test exploratory mode routing."""
    router = UnifiedRouter()
    config = router.route("test", "exploratory", {})

    assert config.mode == "exploratory"
    assert config.max_depth


def test_router_invalid_mode():
    """Test invalid mode defaults to full."""
    router = UnifiedRouter()
    config = router.route("test", "invalid", {})

    assert config.mode == "full"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
