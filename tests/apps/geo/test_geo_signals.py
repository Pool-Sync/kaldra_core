"""Tests for KALDRA-GEO signals."""

import pytest
import numpy as np
from unittest.mock import MagicMock

from src.apps.geo.geo_signals import (
    GeoSignalInput,
    GeoSignal,
    build_geo_signal_from_kaldra
)


def test_build_geo_signal_from_kaldra_basic():
    """Test basic GeoSignal construction from KaldraSignal."""
    # Create mock signal
    mock_signal = MagicMock()
    mock_signal.archetype_probs = np.array([0.1, 0.3, 0.6])  # Top is index 2
    mock_signal.tw_trigger = False
    mock_signal.epistemic.status = "CONFIDENT"
    
    # Build GeoSignal
    geo_signal = build_geo_signal_from_kaldra(mock_signal, region="EU", source="news")
    
    # Assertions
    assert geo_signal.domain == "GEO"
    assert len(geo_signal.top_archetypes) == 3
    assert geo_signal.top_archetypes[0][0] == 2  # Top index
    assert geo_signal.top_archetypes[0][1] == 0.6  # Top prob
    assert geo_signal.tw_triggered is False
    assert geo_signal.extras["region"] == "EU"
    assert geo_signal.extras["source"] == "news"


def test_build_geo_signal_with_tw_trigger():
    """Test GeoSignal with TW trigger sets high risk."""
    mock_signal = MagicMock()
    mock_signal.archetype_probs = np.array([0.2, 0.8])
    mock_signal.tw_trigger = True
    mock_signal.tw_state = MagicMock(severity=0.9)
    mock_signal.epistemic.status = "CAUTION"
    
    geo_signal = build_geo_signal_from_kaldra(mock_signal)
    
    assert geo_signal.tw_triggered is True
    assert geo_signal.risk_level in ["high", "critical"]
    assert geo_signal.tw_severity == 0.9
