"""
Context-Based Router for KALDRA Engine Variants

Routes inference requests to appropriate engine based on context analysis.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np


@dataclass
class RoutingContext:
    """
    Context information for routing decisions.
    
    Attributes:
        text: Optional text input for keyword analysis
        embedding: Optional embedding vector
        metadata: Optional metadata dictionary
        domain_hints: Optional explicit domain hints (e.g., ["finance", "earnings"])
    """
    text: Optional[str] = None
    embedding: Optional[np.ndarray] = None
    metadata: Optional[Dict[str, Any]] = None
    domain_hints: Optional[List[str]] = None


@dataclass
class RoutingDecision:
    """
    Result of routing analysis.
    
    Attributes:
        primary_engine: Main engine to use ("alpha" | "geo" | "product" | "safeguard" | "default")
        confidence: Confidence score (0.0 to 1.0)
        secondary_engines: Additional engines that may be relevant
        reasoning: Optional explanation of routing decision
    """
    primary_engine: str
    confidence: float
    secondary_engines: List[str] = field(default_factory=list)
    reasoning: Optional[str] = None


class MetaRouter:
    """
    Context-based router for KALDRA engines.
    
    Analyzes input context and determines which engine variant to use:
    - alpha: Financial analysis (earnings, markets, revenue)
    - geo: Geopolitical analysis (diplomacy, conflicts, sanctions)
    - product: UX/Product analysis (user experience, friction, journeys)
    - safeguard: Safety/moderation (harmful content, manipulation)
    - default: General-purpose (fallback)
    """
    
    # Domain-specific keywords for routing
    DOMAIN_KEYWORDS = {
        "alpha": [
            "earnings", "revenue", "profit", "eps", "guidance", "forecast",
            "market", "stock", "investor", "shareholder", "dividend",
            "quarterly", "annual", "financial", "valuation", "growth",
            "margin", "ebitda", "cash flow", "balance sheet", "income statement"
        ],
        "geo": [
            "diplomatic", "diplomacy", "sanctions", "treaty", "conflict",
            "geopolitical", "sovereignty", "territorial", "alliance", "nato",
            "un", "security council", "ambassador", "foreign policy", "bilateral",
            "multilateral", "regime", "government", "state", "nation"
        ],
        "product": [
            "user", "ux", "ui", "interface", "experience", "journey",
            "friction", "usability", "design", "feature", "workflow",
            "onboarding", "conversion", "engagement", "retention", "churn",
            "feedback", "pain point", "customer", "satisfaction", "nps"
        ],
        "safeguard": [
            "harmful", "toxic", "abuse", "harassment", "hate", "violence",
            "manipulation", "misinformation", "disinformation", "propaganda",
            "extremism", "radicalization", "threat", "dangerous", "illegal",
            "inappropriate", "offensive", "explicit", "nsfw", "moderation"
        ]
    }
    
    def __init__(self, confidence_threshold: float = 0.3):
        """
        Initialize router.
        
        Args:
            confidence_threshold: Minimum confidence to route to specific engine
        """
        self.confidence_threshold = confidence_threshold
    
    def route(self, context: RoutingContext) -> RoutingDecision:
        """
        Determine which engine(s) to use based on context.
        
        Args:
            context: Routing context with text, embedding, metadata, or hints
        
        Returns:
            RoutingDecision with primary engine and confidence
        """
        # Priority 1: Explicit domain hints
        if context.domain_hints:
            return self._route_from_hints(context.domain_hints)
        
        # Priority 2: Metadata-based routing
        if context.metadata:
            metadata_scores = self._analyze_metadata(context.metadata)
            if metadata_scores:
                return self._make_decision(metadata_scores, "metadata")
        
        # Priority 3: Keyword-based routing from text
        if context.text:
            keyword_scores = self._analyze_keywords(context.text)
            if keyword_scores:
                return self._make_decision(keyword_scores, "keywords")
        
        # Fallback: Default engine
        return RoutingDecision(
            primary_engine="default",
            confidence=1.0,
            reasoning="No specific domain detected, using default engine"
        )
    
    def _route_from_hints(self, hints: List[str]) -> RoutingDecision:
        """Route based on explicit domain hints."""
        hints_lower = [h.lower() for h in hints]
        
        # Map hints to engines
        for engine in ["alpha", "geo", "product", "safeguard"]:
            if engine in hints_lower or any(kw in hints_lower for kw in self.DOMAIN_KEYWORDS[engine][:5]):
                return RoutingDecision(
                    primary_engine=engine,
                    confidence=1.0,
                    reasoning=f"Explicit domain hint: {hints}"
                )
        
        return RoutingDecision(
            primary_engine="default",
            confidence=0.8,
            reasoning=f"Domain hints provided but not recognized: {hints}"
        )
    
    def _analyze_keywords(self, text: str) -> Dict[str, float]:
        """
        Analyze text for domain-specific keywords.
        
        Returns:
            Dictionary mapping engine names to scores (0.0 to 1.0)
        """
        text_lower = text.lower()
        scores = {}
        
        for engine, keywords in self.DOMAIN_KEYWORDS.items():
            # Count keyword matches
            matches = sum(1 for kw in keywords if kw in text_lower)
            # Normalize by number of keywords
            score = matches / len(keywords) if keywords else 0.0
            scores[engine] = score
        
        return scores
    
    def _analyze_metadata(self, metadata: Dict[str, Any]) -> Dict[str, float]:
        """
        Analyze metadata for routing hints.
        
        Looks for keys like:
        - "domain": "finance" | "geopolitics" | "product" | "safety"
        - "source": "earnings_call" | "diplomatic_statement" | "user_feedback"
        - "category": domain-specific category
        
        Returns:
            Dictionary mapping engine names to scores (0.0 to 1.0)
        """
        scores = {}
        
        # Check for explicit domain field
        domain = metadata.get("domain", "").lower()
        if domain:
            if domain in ["finance", "financial", "market", "earnings"]:
                scores["alpha"] = 1.0
            elif domain in ["geo", "geopolitical", "diplomatic", "foreign policy"]:
                scores["geo"] = 1.0
            elif domain in ["product", "ux", "ui", "user experience"]:
                scores["product"] = 1.0
            elif domain in ["safety", "moderation", "safeguard", "harmful"]:
                scores["safeguard"] = 1.0
        
        # Check for source field
        source = metadata.get("source", "").lower()
        if source:
            if "earnings" in source or "financial" in source or "investor" in source:
                scores["alpha"] = scores.get("alpha", 0.0) + 0.8
            elif "diplomatic" in source or "foreign" in source or "treaty" in source:
                scores["geo"] = scores.get("geo", 0.0) + 0.8
            elif "user" in source or "feedback" in source or "ux" in source:
                scores["product"] = scores.get("product", 0.0) + 0.8
            elif "moderation" in source or "report" in source or "flag" in source:
                scores["safeguard"] = scores.get("safeguard", 0.0) + 0.8
        
        # Normalize scores to [0, 1]
        if scores:
            max_score = max(scores.values())
            if max_score > 1.0:
                scores = {k: v / max_score for k, v in scores.items()}
        
        return scores
    
    def _make_decision(self, scores: Dict[str, float], source: str) -> RoutingDecision:
        """
        Make routing decision from scores.
        
        Args:
            scores: Dictionary mapping engine names to scores
            source: Source of scores ("keywords" | "metadata")
        
        Returns:
            RoutingDecision
        """
        if not scores:
            return RoutingDecision(
                primary_engine="default",
                confidence=1.0,
                reasoning="No domain scores available"
            )
        
        # Find primary engine (highest score)
        primary_engine = max(scores, key=scores.get)
        confidence = scores[primary_engine]
        
        # Find secondary engines (above threshold)
        secondary_engines = [
            engine for engine, score in scores.items()
            if engine != primary_engine and score >= self.confidence_threshold * 0.7
        ]
        
        # If confidence too low, use default
        if confidence < self.confidence_threshold:
            return RoutingDecision(
                primary_engine="default",
                confidence=0.8,
                secondary_engines=secondary_engines,
                reasoning=f"Low confidence ({confidence:.2f}) from {source}, using default"
            )
        
        return RoutingDecision(
            primary_engine=primary_engine,
            confidence=confidence,
            secondary_engines=secondary_engines,
            reasoning=f"Routed via {source} analysis (confidence: {confidence:.2f})"
        )
