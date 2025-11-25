import pytest
from unittest.mock import MagicMock, patch
from src.tw369.tw369_integration import TW369Integrator, TWState

class TestTW369WithPainleve:
    def test_integration_disabled_by_default(self):
        integrator = TW369Integrator()
        # Mock config to ensure it's disabled or empty
        integrator.config = {}
        
        # Create a state with some tension
        state = TWState(
            plane3_cultural_macro={"a": 1.0},
            plane6_semiotic_media={"b": 1.0},
            plane9_structural_systemic={"c": 1.0}
        )
        
        # Compute severity
        severity = integrator._compute_severity_factor(state)
        assert 0.0 <= severity <= 1.0
        
        # With default config, filter should NOT be called.
        # We can't easily check if it was called without mocking, 
        # but we can check if it runs without error.

    def test_integration_enabled(self):
        integrator = TW369Integrator()
        # Enable filter
        integrator.config = {"use_painleve_filter": True}
        
        state = TWState(
            plane3_cultural_macro={"a": 1.0},
            plane6_semiotic_media={"b": 1.0},
            plane9_structural_systemic={"c": 1.0}
        )
        
        # Compute severity
        # This triggers _compute_severity_factor -> _apply_painleve_filter
        severity = integrator._compute_severity_factor(state)
        assert 0.0 <= severity <= 1.0

    @patch('src.tw369.tw369_integration.painleve_filter')
    def test_filter_is_called(self, mock_filter):
        integrator = TW369Integrator()
        integrator.config = {"use_painleve_filter": True}
        
        mock_filter.return_value = 0.5
        
        state = TWState(
            plane3_cultural_macro={"a": 1.0},
            plane6_semiotic_media={"b": 1.0},
            plane9_structural_systemic={"c": 1.0}
        )
        
        integrator._compute_severity_factor(state)
        
        # Check if filter was called
        mock_filter.assert_called_once()

    @patch('src.tw369.tw369_integration.painleve_filter')
    def test_filter_is_not_called_when_disabled(self, mock_filter):
        integrator = TW369Integrator()
        integrator.config = {"use_painleve_filter": False}
        
        state = TWState(
            plane3_cultural_macro={"a": 1.0},
            plane6_semiotic_media={"b": 1.0},
            plane9_structural_systemic={"c": 1.0}
        )
        
        integrator._compute_severity_factor(state)
        
        # Check if filter was NOT called
        mock_filter.assert_not_called()
