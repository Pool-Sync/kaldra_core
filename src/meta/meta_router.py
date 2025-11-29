"""
MetaRouter - Orchestration and Routing Decision.

Coordinates all meta-engines and produces routing decisions for app selection.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

from .meta_engine_base import MetaEngineBase, MetaSignal
from .nietzsche import analyze_meta as analyze_nietzsche
from .campbell import CampbellEngine, HERO_JOURNEY_STAGES
from .aurelius import analyze_meta as analyze_aurelius


@dataclass
class RoutingDecision:
    """
    Routing decision for app selection.
    
    Attributes:
        dominant_app: Primary app to route to
        secondary_apps: Additional apps that may be relevant
        meta_signals: All meta-engine signals used for decision
        confidence: Overall confidence in routing decision [0, 1]
        reasoning: Human-readable explanation
    """
    dominant_app: str
    secondary_apps: List[str] = field(default_factory=list)
    meta_signals: Dict[str, MetaSignal] = field(default_factory=dict)
    confidence: float = 0.5
    reasoning: str = ""


class MetaRouter:
    """
    Orchestrates meta-engines and produces routing decisions.
    
    Evaluates signals through Nietzsche, Campbell, and Aurelius engines,
    then combines their outputs to determine optimal app routing.
    """
    
    def __init__(self, engines: Optional[List[MetaEngineBase]] = None):
        """
        Initialize MetaRouter with engines.
        
        Args:
            engines: List of meta-engines (defaults to Campbell only for class-based)
        """
        # Only Campbell is class-based now
        # Nietzsche and Aurelius are function-based
        self.engines = engines or [
            CampbellEngine(),
        ]
    
    def evaluate(self, signal: Dict[str, Any]) -> Dict[str, MetaSignal]:
        """
        Run all meta-engines on the signal.
        
        Args:
            signal: Complete KALDRA signal
            
        Returns:
            Dictionary mapping engine name to MetaSignal
        """
        results: Dict[str, MetaSignal] = {}
        
        # Call function-based engines (Nietzsche, Aurelius)
        text = signal.get("text", "")
        
        # Nietzsche
        try:
            nietzsche_result = analyze_nietzsche(
                text,
                delta12=signal.get("delta12"),
                tw_state=signal.get("tw_state"),
                bias_score=signal.get("bias_score")
            )
            # Convert MetaEngineResult to MetaSignal
            results["nietzsche"] = MetaSignal(
                name="nietzsche",
                score=nietzsche_result.severity,
                label=nietzsche_result.dominant_axes[0][0] if nietzsche_result.dominant_axes else "unknown",
                details=nietzsche_result.scores
            )
        except Exception as e:
            results["nietzsche"] = MetaSignal(
                name="nietzsche",
                score=0.5,
                label="error",
                details={"error": str(e)}
            )
        
        # Aurelius
        try:
            aurelius_result = analyze_aurelius(
                text,
                delta12=signal.get("delta12"),
                tw_state=signal.get("tw_state"),
                bias_score=signal.get("bias_score")
            )
            # Convert MetaEngineResult to MetaSignal
            results["aurelius"] = MetaSignal(
                name="aurelius",
                score=aurelius_result.severity,
                label="regulated" if aurelius_result.severity > 0.6 else "on_the_edge" if aurelius_result.severity > 0.4 else "reactive",
                details=aurelius_result.scores
            )
        except Exception as e:
            results["aurelius"] = MetaSignal(
                name="aurelius",
                score=0.5,
                label="error",
                details={"error": str(e)}
            )
        
        # Call class-based engines (Campbell)
        for engine in self.engines:
            try:
                results[engine.name] = engine.run(signal)
            except Exception as e:
                results[engine.name] = MetaSignal(
                    name=engine.name,
                    score=0.5,
                    label="error",
                    details={"error": str(e)}
                )
        
        return results
    
    def decide_route(self, meta_signals: Dict[str, MetaSignal]) -> RoutingDecision:
        """
        Determine routing decision from meta-signals.
        
        Heuristics v1:
        - Ordeal/Approach stages + high drift → Safeguard
        - High Will to Power + Plane 3 → Alpha/Product
        - Regulated + Wisdom archetypes → Geo
        - Ambiguous → KALDRA (default)
        
        Args:
            meta_signals: Results from evaluate()
            
        Returns:
            RoutingDecision with dominant app and reasoning
        """
        nietzsche = meta_signals.get("nietzsche")
        campbell = meta_signals.get("campbell")
        aurelius = meta_signals.get("aurelius")
        
        # Default fallback
        dominant_app = "kaldra"
        secondary_apps = []
        confidence = 0.5
        reasoning = "Default routing (ambiguous signals)"
        
        # Rule 1: Crisis stages → Safeguard
        if campbell and campbell.label in ["ordeal", "approach_to_cave", "tests_allies_enemies"]:
            if campbell.score > 0.6:
                dominant_app = "safeguard"
                secondary_apps = ["kaldra"]
                confidence = campbell.score
                reasoning = f"Hero's Journey stage '{campbell.label}' indicates crisis/challenge"
                return RoutingDecision(dominant_app, secondary_apps, meta_signals, confidence, reasoning)
        
        # Rule 2: High Will to Power + Action → Alpha or Product
        if nietzsche and nietzsche.score > 0.7 and nietzsche.label == "will_to_power_high":
            # Check if it's market/product oriented or pure action
            dominant_app = "alpha"  # Default to Alpha for high energy
            secondary_apps = ["product"]
            confidence = nietzsche.score
            reasoning = "High Will to Power indicates action/expansion mode"
            return RoutingDecision(dominant_app, secondary_apps, meta_signals, confidence, reasoning)
        
        # Rule 3: Regulated + Wisdom → Geo (macro/strategic)
        if aurelius and aurelius.score > 0.7 and aurelius.label == "regulated":
            dominant_app = "geo"
            secondary_apps = ["kaldra"]
            confidence = aurelius.score
            reasoning = "Regulated state with high coherence suggests strategic/macro analysis"
            return RoutingDecision(dominant_app, secondary_apps, meta_signals, confidence, reasoning)
        
        # Rule 4: Reactive/Panic → Safeguard
        if aurelius and aurelius.label == "reactive" and aurelius.score < 0.4:
            dominant_app = "safeguard"
            secondary_apps = ["kaldra"]
            confidence = 1.0 - aurelius.score
            reasoning = "Reactive state with low regulation suggests need for safeguarding"
            return RoutingDecision(dominant_app, secondary_apps, meta_signals, confidence, reasoning)
        
        # Rule 5: Transformative stages → Product/Creator mode
        if campbell and campbell.label in ["reward", "resurrection", "return_with_elixir"]:
            if campbell.score > 0.6:
                dominant_app = "product"
                secondary_apps = ["alpha", "kaldra"]
                confidence = campbell.score
                reasoning = f"Hero's Journey stage '{campbell.label}' indicates creation/integration phase"
                return RoutingDecision(dominant_app, secondary_apps, meta_signals, confidence, reasoning)
        
        # Rule 6: Beginning of journey → Alpha (exploration)
        if campbell and campbell.label in ["call_to_adventure", "crossing_the_threshold"]:
            if campbell.score > 0.6:
                dominant_app = "alpha"
                secondary_apps = ["kaldra"]
                confidence = campbell.score
                reasoning = f"Hero's Journey stage '{campbell.label}' indicates exploration/adventure"
                return RoutingDecision(dominant_app, secondary_apps, meta_signals, confidence, reasoning)
        
        # Default: KALDRA (exploratory/general)
        return RoutingDecision(
            dominant_app="kaldra",
            secondary_apps=[],
            meta_signals=meta_signals,
            confidence=0.5,
            reasoning="No strong signals for specialized routing"
        )


def decide_route(meta_signals: Dict[str, MetaSignal]) -> RoutingDecision:
    """
    Convenience function for routing decision.
    
    Args:
        meta_signals: Results from MetaRouter.evaluate()
        
    Returns:
        RoutingDecision
    """
    router = MetaRouter()
    return router.decide_route(meta_signals)
