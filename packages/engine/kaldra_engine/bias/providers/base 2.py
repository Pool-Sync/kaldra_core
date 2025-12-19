"""
Base interface for Bias Providers.
"""

from abc import ABC, abstractmethod
from typing import Dict


class BiasProvider(ABC):
    """
    Abstract base class for bias detection providers.
    
    All providers must implement the detect method.
    """
    
    @abstractmethod
    def detect(self, text: str) -> Dict[str, float]:
        """
        Detect bias in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with bias scores for each dimension:
                - toxicity: [0.0, 1.0]
                - political: [0.0, 1.0]
                - gender: [0.0, 1.0]
                - racial: [0.0, 1.0]
        """
        pass
