"""
Shim de compatibilidade temporário para Delta144Engine.

Permite:
    from kaldra_core.core.archetypes import Delta144Engine

enquanto migramos para:
    from kaldra_core.src.archetypes import Delta144Engine
"""

from ...src.archetypes import Delta144Engine

__all__ = ["Delta144Engine"]
