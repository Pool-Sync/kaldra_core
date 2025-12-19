"""
Meta-Engine Module for KALDRA v2.5.
"""

from .aurelius import AureliusProfile
from .aurelius import analyze_meta as analyze_aurelius
from .campbell import HERO_JOURNEY_STAGES, CampbellEngine
from .meta_engine_base import MetaEngineBase, MetaSignal
from .meta_router import MetaRouter, RoutingDecision, decide_route
from .nietzsche import (
    MetaEngineResult,
    NietzscheProfile,
)
from .nietzsche import (
    analyze_meta as analyze_nietzsche,
)

__all__ = [
    "MetaEngineBase",
    "MetaSignal",
    "analyze_nietzsche",
    "NietzscheProfile",
    "CampbellEngine",
    "HERO_JOURNEY_STAGES",
    "analyze_aurelius",
    "AureliusProfile",
    "MetaEngineResult",
    "MetaRouter",
    "RoutingDecision",
    "decide_route",
]
