"""
LLM Client Base Interface.

Defines the contract for all LLM clients used by Kindra scorers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMClientBase(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def generate(self, prompt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a response from the LLM based on the prompt.

        Args:
            prompt: Dictionary containing the prompt structure (instruction, context, text, vectors).

        Returns:
            Dictionary containing the parsed response (e.g., {"scores": {...}}).
        """
        pass
