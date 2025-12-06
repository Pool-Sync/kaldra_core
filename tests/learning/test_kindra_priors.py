"""
Unit tests for Kindra Priors (v3.5 Phase 2).
"""
import pytest
import json
import tempfile
import os
from src.learning.kindra_priors import KindraPriors


class TestKindraPriors:
    """Test suite for Kindra priors."""
    
    def test_load_from_config(self):
        """Test loading priors from config file."""
        # Create temp config
        config_data = {
            "priors": {
                "k1": {"threshold": 0.5, "emergence": 0.5},
                "k2": {"integration": 0.8, "transformation": 0.2}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            priors = KindraPriors.from_config(config_path)
            
            assert "k1" in priors.priors
            assert priors.priors["k1"]["threshold"] == 0.5
            assert priors.priors["k2"]["integration"] == 0.8
        finally:
            os.unlink(config_path)
    
    def test_get_prior_existing_kindra(self):
        """Test getting prior for existing Kindra."""
        priors = KindraPriors(priors={
            "k1": {"threshold": 0.6, "emergence": 0.4}
        })
        
        prior = priors.get_prior("k1")
        
        assert prior["threshold"] == 0.6
        assert prior["emergence"] == 0.4
    
    def test_get_prior_unknown_kindra_returns_empty(self):
        """Test that unknown Kindra returns empty dict."""
        priors = KindraPriors(priors={"k1": {"threshold": 1.0}})
        
        prior = priors.get_prior("unknown")
        
        assert prior == {}
