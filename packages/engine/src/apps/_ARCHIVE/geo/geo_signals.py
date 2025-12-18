"""Geopolitical signal structures for KALDRA-GEO."""

from dataclasses import dataclass, field
from typing import Optional, Any
import numpy as np


@dataclass
class GeoSignalInput:
    """Input for geopolitical signal analysis."""
    text: str
    region: Optional[str] = None
    source: Optional[str] = None  # e.g., "news", "social", "report"
    metadata: Optional[dict] = None


@dataclass
class GeoSignal:
    """Geopolitical signal output from KALDRA-GEO."""
    story_id: Optional[str] = None
    top_archetypes: list = field(default_factory=list)  # List of (index, prob) tuples
    tw_triggered: bool = False
    tw_severity: Optional[float] = None
    risk_level: str = "low"  # "low" | "medium" | "high" | "critical"
    domain: str = "GEO"
    extras: dict = field(default_factory=dict)


def build_geo_signal_from_kaldra(
    signal: Any,
    region: Optional[str] = None,
    source: Optional[str] = None,
    top_k: int = 3
) -> GeoSignal:
    """
    Convert a KaldraSignal to a GeoSignal.
    
    Args:
        signal: KaldraSignal from Master Engine
        region: Geographic region identifier
        source: Source type (news, social, etc.)
        top_k: Number of top archetypes to extract
    
    Returns:
        GeoSignal with domain-specific fields
    """
    # Extract top archetypes
    if hasattr(signal, "archetype_probs"):
        probs = np.array(signal.archetype_probs)
        top_indices = probs.argsort()[-top_k:][::-1]
        top_archetypes = [
            (int(idx), float(probs[idx])) 
            for idx in top_indices
        ]
    else:
        top_archetypes = []
    
    # Determine risk level based on max probability and TW trigger
    tw_triggered = getattr(signal, "tw_trigger", False)
    max_prob = max([p for _, p in top_archetypes]) if top_archetypes else 0.0
    
    if tw_triggered:
        risk_level = "critical" if max_prob > 0.7 else "high"
    elif max_prob > 0.6:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    # Extract TW severity if available
    tw_severity = None
    if hasattr(signal, "tw_state") and signal.tw_state:
        tw_severity = float(getattr(signal.tw_state, "severity", 0.0))
    
    return GeoSignal(
        story_id=None,  # Placeholder for future Story integration
        top_archetypes=top_archetypes,
        tw_triggered=tw_triggered,
        tw_severity=tw_severity,
        risk_level=risk_level,
        domain="GEO",
        extras={
            "region": region,
            "source": source,
            "epistemic_status": getattr(signal.epistemic, "status", "UNKNOWN") if hasattr(signal, "epistemic") else "UNKNOWN"
        }
    )
