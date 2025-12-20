"""
KALDRA v3.0 — Unification Layer

The Unification Layer transforms KALDRA from multiple independent modules
into a single coherent, modular, and extensible system.

Codename: "One Engine, Many Minds"
"""

__version__ = "3.0.0"
__codename__ = "One Engine, Many Minds"

from .adapters.unified_api import UnifiedKaldra
from .kernel import UnifiedKernel

__all__ = [
    "UnifiedKernel",
    "UnifiedKaldra",
]
