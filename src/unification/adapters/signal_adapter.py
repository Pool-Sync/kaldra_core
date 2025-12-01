"""
Signal Adapter for KALDRA v3.0.

Converts UnifiedContext to standardized signal format.
"""
from typing import Dict, Any
import logging

from ..states.unified_state import UnifiedContext

logger = logging.getLogger(__name__)


class SignalAdapter:
    """
    Adapter for converting UnifiedContext to standardized signal format.
    
    Produces a consistent JSON-serializable output regardless of
    which stages were executed or which failed.
    """
    
    @staticmethod
    def to_signal(context: UnifiedContext) -> Dict[str, Any]:
        """
        Convert UnifiedContext to standardized signal format.
        
        Args:
            context: Unified context from pipeline
            
        Returns:
            Dictionary in standardized signal format
        """
        signal = {
            "version": context.global_ctx.version,
            "request_id": context.global_ctx.request_id,
            "timestamp": context.global_ctx.timestamp,
            "mode": context.global_ctx.mode,
        }
        
        # Input
        if context.input_ctx:
            signal["input"] = {
                "text": context.input_ctx.text,
                "bias_score": context.input_ctx.bias_score,
                "tau_input": context.input_ctx.tau_input.to_dict() if context.input_ctx.tau_input else None
            }
        
        # Kindra
        if context.kindra_ctx:
            signal["kindra"] = context.kindra_ctx.to_dict()
        
        # Archetypes
        if context.archetype_ctx:
            signal["archetypes"] = context.archetype_ctx.to_dict()
        
        # Drift
        if context.drift_ctx:
            signal["drift"] = context.drift_ctx.to_dict()
        
        # Meta
        if context.meta_ctx:
            signal["meta"] = context.meta_ctx.to_dict()
        
        # Story
        if context.story_ctx:
            signal["story"] = context.story_ctx.to_dict()
        
        # Risk
        if context.risk_ctx:
            signal["risk"] = {
                "tau_output": context.risk_ctx.tau_output.to_dict() if context.risk_ctx.tau_output else None,
                "safeguard": context.risk_ctx.safeguard.to_dict() if context.risk_ctx.safeguard else None,
                "final_risk": context.risk_ctx.final_risk,
                "risk_score": context.risk_ctx.risk_score
            }
        
        # Summary
        summary = getattr(context.global_ctx, 'summary', None)
        if summary:
            signal["summary"] = summary
        else:
            signal["summary"] = {
                "confidence": 1.0,
                "routing": context.global_ctx.mode,
                "degraded": context.global_ctx.degraded
            }
        
        return signal
    
    @staticmethod
    def to_compact_signal(context: UnifiedContext) -> Dict[str, Any]:
        """
        Convert to compact signal format (minimal).
        
        Args:
            context: Unified context
            
        Returns:
            Compact signal dictionary
        """
        signal = {
            "version": "3.0",
            "request_id": context.global_ctx.request_id,
            "degraded": context.global_ctx.degraded
        }
        
        # Add only essential fields
        if context.archetype_ctx and context.archetype_ctx.delta144_state:
            signal["archetype"] = context.archetype_ctx.delta144_state.archetype.label
            signal["state"] = context.archetype_ctx.delta144_state.state.label
        
        if context.risk_ctx:
            signal["risk"] = context.risk_ctx.final_risk
        
        return signal
