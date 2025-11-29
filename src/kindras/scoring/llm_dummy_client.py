"""
Dummy LLM Client.

A placeholder client that returns zero scores. Used for testing and fallback.
"""

from typing import Dict, Any
from .llm_client_base import LLMClientBase

class DummyLLMClient(LLMClientBase):
    """
    Dummy LLM client that returns neutral/zero scores.
    Useful for testing or when no API key is configured.
    """

    def generate(self, prompt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Return a dummy response with 0.0 scores for all requested vectors.
        """
        vectors = prompt.get("vectors", [])
        scores = {v: 0.0 for v in vectors}
        return {"scores": scores}
