"""
Meta-Engine Orchestrator for KALDRA

Coordinates execution across multiple KALDRA engine variants.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np

from src.core.kaldra_master_engine import KaldraMasterEngineV2, KaldraSignal
from src.meta.engine_router import RoutingContext, RoutingDecision, MetaRouter


@dataclass
class OrchestrationConfig:
    """
    Configuration for orchestration.
    
    Attributes:
        parallel_execution: Whether to execute engines in parallel (not yet implemented)
        timeout_seconds: Optional timeout for execution
        fallback_to_default: Whether to use default engine if routing fails
    """
    parallel_execution: bool = False
    timeout_seconds: Optional[float] = None
    fallback_to_default: bool = True


@dataclass
class EngineResult:
    """
    Result from a single engine execution.
    
    Attributes:
        engine_name: Name of the engine variant
        signal: KaldraSignal output from engine
        execution_time: Time taken to execute (seconds)
        success: Whether execution succeeded
        error: Optional error message if failed
    """
    engine_name: str
    signal: Optional[KaldraSignal]
    execution_time: float
    success: bool
    error: Optional[str] = None


@dataclass
class OrchestrationResult:
    """
    Combined result from orchestration.
    
    Attributes:
        primary_result: Result from primary engine
        secondary_results: Results from secondary engines (if any)
        routing_decision: The routing decision that was made
        total_time: Total time for orchestration (seconds)
    """
    primary_result: EngineResult
    secondary_results: List[EngineResult] = field(default_factory=list)
    routing_decision: Optional[RoutingDecision] = None
    total_time: float = 0.0


class MetaOrchestrator:
    """
    Orchestrates execution across multiple KALDRA engine variants.
    
    Manages routing and execution for:
    - alpha: Financial analysis
    - geo: Geopolitical analysis
    - product: UX/Product analysis
    - safeguard: Safety/moderation
    - default: General-purpose
    """
    
    def __init__(self, config: Optional[OrchestrationConfig] = None):
        """
        Initialize orchestrator.
        
        Args:
            config: Optional orchestration configuration
        """
        self.config = config or OrchestrationConfig()
        self.router = MetaRouter()
        self.engines = self._initialize_engines()
    
    def _initialize_engines(self) -> Dict[str, KaldraMasterEngineV2]:
        """
        Initialize all engine variants.
        
        For now, all variants use the same underlying engine with different metadata.
        In the future, variants may have different configurations (tau, tw_config, etc.)
        
        Returns:
            Dictionary mapping engine names to instances
        """
        engines = {}
        
        # Default engine
        engines["default"] = KaldraMasterEngineV2(d_ctx=256, tau=0.65)
        
        # Alpha: Financial analysis (slightly higher tau for more certainty)
        engines["alpha"] = KaldraMasterEngineV2(d_ctx=256, tau=0.70)
        
        # GEO: Geopolitical analysis (standard tau)
        engines["geo"] = KaldraMasterEngineV2(d_ctx=256, tau=0.65)
        
        # Product: UX/Product analysis (lower tau for more exploration)
        engines["product"] = KaldraMasterEngineV2(d_ctx=256, tau=0.60)
        
        # Safeguard: Safety/moderation (higher tau for more conservative decisions)
        engines["safeguard"] = KaldraMasterEngineV2(d_ctx=256, tau=0.75)
        
        return engines
    
    def execute(
        self,
        embedding: np.ndarray,
        context: Optional[RoutingContext] = None,
        routing_decision: Optional[RoutingDecision] = None,
        tw_window: Optional[np.ndarray] = None,
    ) -> OrchestrationResult:
        """
        Execute inference using routed engine(s).
        
        Args:
            embedding: Input embedding vector
            context: Optional routing context (if routing_decision not provided)
            routing_decision: Optional pre-computed routing decision
            tw_window: Optional TW window for inference
        
        Returns:
            OrchestrationResult with primary and optional secondary results
        """
        start_time = time.time()
        
        # Step 1: Route if needed
        if routing_decision is None:
            if context is None:
                # No context provided, use default engine
                routing_decision = RoutingDecision(
                    primary_engine="default",
                    confidence=1.0,
                    reasoning="No context provided"
                )
            else:
                routing_decision = self.router.route(context)
        
        # Step 2: Execute primary engine
        primary_result = self._execute_engine(
            routing_decision.primary_engine,
            embedding,
            tw_window
        )
        
        # Step 3: Execute secondary engines (if any)
        secondary_results = []
        if routing_decision.secondary_engines:
            for engine_name in routing_decision.secondary_engines:
                result = self._execute_engine(engine_name, embedding, tw_window)
                secondary_results.append(result)
        
        # Step 4: Handle fallback if primary failed
        if not primary_result.success and self.config.fallback_to_default:
            if routing_decision.primary_engine != "default":
                fallback_result = self._execute_engine("default", embedding, tw_window)
                if fallback_result.success:
                    primary_result = fallback_result
        
        total_time = time.time() - start_time
        
        return OrchestrationResult(
            primary_result=primary_result,
            secondary_results=secondary_results,
            routing_decision=routing_decision,
            total_time=total_time
        )
    
    def _execute_engine(
        self,
        engine_name: str,
        embedding: np.ndarray,
        tw_window: Optional[np.ndarray] = None,
    ) -> EngineResult:
        """
        Execute a single engine.
        
        Args:
            engine_name: Name of engine to execute
            embedding: Input embedding
            tw_window: Optional TW window
        
        Returns:
            EngineResult with execution details
        """
        start_time = time.time()
        
        try:
            # Get engine instance
            engine = self.engines.get(engine_name)
            if engine is None:
                return EngineResult(
                    engine_name=engine_name,
                    signal=None,
                    execution_time=0.0,
                    success=False,
                    error=f"Engine '{engine_name}' not found"
                )
            
            # Execute inference
            signal = engine.infer_from_embedding(embedding, tw_window=tw_window)
            
            execution_time = time.time() - start_time
            
            return EngineResult(
                engine_name=engine_name,
                signal=signal,
                execution_time=execution_time,
                success=True
            )
        
        except Exception as e:
            execution_time = time.time() - start_time
            return EngineResult(
                engine_name=engine_name,
                signal=None,
                execution_time=execution_time,
                success=False,
                error=str(e)
            )
