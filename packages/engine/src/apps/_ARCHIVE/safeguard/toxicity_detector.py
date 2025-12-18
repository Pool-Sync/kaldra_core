"""Toxicity detection and narrative risk analysis for KALDRA-Safeguard."""

from dataclasses import dataclass, field
from typing import Optional
import logging

from src.bias.detector import BiasDetector
from src.bias.mitigation import BiasMitigation

logger = logging.getLogger(__name__)


@dataclass
class SafeguardInput:
    """Input for safeguard analysis."""
    text: str
    source: Optional[str] = None  # "chat", "social", "internal_doc", etc.
    metadata: Optional[dict] = None


@dataclass
class SafeguardToxicityResult:
    """Toxicity and bias analysis result."""
    toxicity: float
    bias_dimensions: dict = field(default_factory=dict)
    severity: str = "low"  # "low" | "medium" | "high" | "critical"
    flags: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)
    domain: str = "SAFEGUARD"


class ToxicityDetector:
    """
    Toxicity and narrative risk detector.
    
    Integrates with KALDRA Bias Engine for comprehensive analysis.
    """
    
    def __init__(
        self,
        provider: str = "heuristic",
        correction_factor: float = 0.85,
    ):
        """
        Initialize ToxicityDetector.
        
        Args:
            provider: Bias detection provider ("heuristic", "perspective", "detoxify")
            correction_factor: Mitigation correction factor (0.0-1.0)
        """
        self._detector = BiasDetector(provider=provider)
        self._mitigator = BiasMitigation(correction_factor=correction_factor)
    
    def analyze(self, text: str, source: Optional[str] = None) -> SafeguardToxicityResult:
        """
        Analyze text for toxicity and bias.
        
        Args:
            text: Input text to analyze
            source: Source type for context
        
        Returns:
            SafeguardToxicityResult with scores and recommendations
        """
        if not text or not text.strip():
            return SafeguardToxicityResult(
                toxicity=0.0,
                severity="low",
                domain="SAFEGUARD"
            )
        
        # 1. Detect bias/toxicity
        bias_result = self._detector.detect(text)
        toxicity = bias_result.get("bias_score", 0.0)
        
        # 2. Extract bias dimensions
        bias_dimensions = {
            "toxicity": toxicity,
            "political": bias_result.get("political_bias", 0.0),
            "gender": bias_result.get("gender_bias", 0.0),
            "racial": bias_result.get("racial_bias", 0.0),
        }
        
        # 3. Determine severity
        if toxicity >= 0.8:
            severity = "critical"
        elif toxicity >= 0.6:
            severity = "high"
        elif toxicity >= 0.4:
            severity = "medium"
        else:
            severity = "low"
        
        # 4. Generate flags
        flags = []
        if toxicity >= 0.6:
            flags.append("high_toxicity")
        if bias_dimensions["political"] >= 0.7:
            flags.append("political_bias")
        if bias_dimensions["gender"] >= 0.7:
            flags.append("gender_bias")
        if bias_dimensions["racial"] >= 0.7:
            flags.append("racial_bias")
        
        # 5. Generate recommendations using mitigation
        recommendations = []
        if flags:
            mitigation_result = self._mitigator.apply(text, bias_result)
            recommendations = mitigation_result.get("recommendations", [])
            
            # Add default recommendations if none provided
            if not recommendations:
                if "high_toxicity" in flags:
                    recommendations.append("Consider rephrasing to reduce inflammatory language")
                if any(f in flags for f in ["political_bias", "gender_bias", "racial_bias"]):
                    recommendations.append("Review content for potential bias and ensure balanced perspective")
        
        logger.info(
            f"Safeguard analysis complete: toxicity={toxicity:.2f}, "
            f"severity={severity}, flags={len(flags)}"
        )
        
        return SafeguardToxicityResult(
            toxicity=toxicity,
            bias_dimensions=bias_dimensions,
            severity=severity,
            flags=flags,
            recommendations=recommendations,
            domain="SAFEGUARD"
        )
