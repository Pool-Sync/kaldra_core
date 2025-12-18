"""
Meta-Engine Module for KALDRA v2.5.
"""

from .meta_engine_base import MetaEngineBase, MetaSignal
from .nietzsche import analyze_meta as analyze_nietzsche, NietzscheProfile, MetaEngineResult
from .campbell import CampbellEngine, HERO_JOURNEY_STAGES
from .aurelius import analyze_meta as analyze_aurelius, AureliusProfile
from .meta_router import MetaRouter, RoutingDecision, decide_route

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
