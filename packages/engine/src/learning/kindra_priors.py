"""
Kindra Priors for Δ144 mapping (v3.5 Phase 2).

Stores base Kindra→Δ144 prior probabilities.
"""
from typing import Dict
from dataclasses import dataclass
import logging
import json

logger = logging.getLogger(__name__)


@dataclass
class KindraPriors:
    """
    Stores Kindra→Δ144 prior mappings.
    
    Attributes:
        priors: kindra_id -> {delta144_state_id: weight}
    """
    priors: Dict[str, Dict[str, float]]
    
    @classmethod
    def from_config(cls, config_path: str) -> "KindraPriors":
        """
        Load priors from config file.
        
        Args:
            config_path: Path to JSON config
        
        Returns:
            KindraPriors instance
        """
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
            return cls(priors=data.get("priors", {}))
        except Exception as e:
            logger.warning(f"Could not load priors from {config_path}: {e}")
            return cls(priors={})
    
    def get_prior(self, kindra_id: str) -> Dict[str, float]:
        """
        Get prior distribution for a Kindra.
        
        Args:
            kindra_id: Kindra identifier
        
        Returns:
            Dictionary of delta144_state_id -> weight
        """
        return self.priors.get(kindra_id, {})
