"""
Safeguard Integration Helpers.

Bridge functions for connecting Safeguard to the core pipeline.
"""
from typing import Dict, Any
from .safeguard_engine import SafeguardSignal

def format_safeguard_output(signal: SafeguardSignal) -> Dict[str, Any]:
    """
    Format the Safeguard signal for the final JSON output.
    """
    return {
        "safeguard": signal.to_dict(),
        "risk_summary": signal.final_risk
    }
