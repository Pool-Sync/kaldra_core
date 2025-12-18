"""
Signal Adapter for KALDRA v3.1.

Converts UnifiedContext to standardized signal format with v3.1 enhancements.
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
        Convert UnifiedContext to standardized signal format (v3.1 enhanced).
        
        v3.1 Enhancements:
        - Enhanced meta output with individual engine signals
        - Detailed kindra 3×48 layer structure
        - Preset configuration metadata
        
        Backward Compatibility:
        - All v2.x/v3.0 fields preserved
        - New fields added only
        - No field removal or renaming
        
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
            "degraded": context.global_ctx.degraded
        }
        
        # Input
        if context.input_ctx:
            signal["input"] = {
                "text": context.input_ctx.text,
                "bias_score": context.input_ctx.bias_score,
                "tau_input": context.input_ctx.tau_input.to_dict() if context.input_ctx.tau_input else None
            }
        
        # Kindra (enhanced for v3.1)
        if context.kindra_ctx:
            signal["kindra"] = context.kindra_ctx.to_dict()
        
        # Archetypes (backward compatible)
        if context.archetype_ctx:
            signal["archetypes"] = context.archetype_ctx.to_dict()
        
        # Drift (backward compatible)
        if context.drift_ctx:
            signal["drift"] = context.drift_ctx.to_dict()
        
        # Meta (enhanced for v3.1 with individual engine outputs)
        if context.meta_ctx:
            meta_dict = context.meta_ctx.to_dict()
            
            # Enhanced v3.1: Include individual engine outputs
            if meta_dict:
                signal["meta"] = meta_dict
            else:
                # Safe fallback
                signal["meta"] = {}
        
        # Story (backward compatible)
        if context.story_ctx:
            signal["story"] = context.story_ctx.to_dict()
        
        # Risk (backward compatible)
        if context.risk_ctx:
            signal["risk"] = {
                "tau_output": context.risk_ctx.tau_output.to_dict() if context.risk_ctx.tau_output else None,
                "safeguard": context.risk_ctx.safeguard.to_dict() if context.risk_ctx.safeguard else None,
                "final_risk": context.risk_ctx.final_risk,
                "risk_score": context.risk_ctx.risk_score
            }
        
        # v3.1: Add preset configuration if available
        preset_config = getattr(context.global_ctx, 'preset_config', None)
        if preset_config:
            signal["preset_used"] = getattr(preset_config, 'name', None)
            signal["preset_config"] = {
                "mode": getattr(preset_config, 'mode', None),
                "emphasis": getattr(preset_config, 'emphasis', {}),
                "thresholds": getattr(preset_config, 'thresholds', {}),
                "output_format": getattr(preset_config, 'output_format', None)
            }
        
        # Summary (backward compatible)
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
