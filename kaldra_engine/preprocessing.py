"""
KALDRA CORE — Preprocessing utilities.
"""
from __future__ import annotations

from typing import List


def simple_tokenize(text: str) -> List[str]:
    """
    Very simple whitespace tokenizer placeholder.

    Args:
        text: Input text to tokenize

    Returns:
        List of tokens (whitespace-separated)
    """
    return text.split()
