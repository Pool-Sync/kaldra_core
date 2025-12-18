"""Geopolitical risk analysis engine for KALDRA-GEO."""

from dataclasses import dataclass
from typing import Optional
import logging

import numpy as np

from src.core.kaldra_master_engine import KaldraMasterEngineV2
from kaldra_data.transformation.embedding_router import EmbeddingRouter, EmbeddingRouterConfig
from src.apps.geo.geo_signals import GeoSignal, GeoSignalInput, build_geo_signal_from_kaldra

logger = logging.getLogger(__name__)


@dataclass
class GeoRiskEngineConfig:
    """Configuration for GeoRiskEngine."""
    d_ctx: int = 256
    top_k_archetypes: int = 3
    use_story_tracker: bool = False


class GeoRiskEngine:
    """
    Geopolitical risk analysis engine.
    
    Analyzes text for geopolitical narrative signals and risk levels.
    """
    
    def __init__(self, config: Optional[GeoRiskEngineConfig] = None):
        self.config = config or GeoRiskEngineConfig()
        self._engine = KaldraMasterEngineV2(d_ctx=self.config.d_ctx)
        
        # Configure embedding router with fallback
        self._router_config = EmbeddingRouterConfig(
            provider="fallback",
            dim=self.config.d_ctx,
            use_fallback=True
        )
        self._router = EmbeddingRouter(config=self._router_config)
    
    def analyze_text(
        self,
        text: str,
        region: Optional[str] = None,
        source: Optional[str] = None,
    ) -> GeoSignal:
        """
        Analyze text for geopolitical signals.
        
        Args:
            text: Input text to analyze
            region: Geographic region identifier
            source: Source type (news, social, report, etc.)
        
        Returns:
            GeoSignal with risk assessment
        
        Raises:
            ValueError: If text is empty
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")
        
        # 1. Generate embedding
        embedding_array = self._router.get_embedding(text.strip())
        
        # Ensure 1D for engine
        if embedding_array.ndim > 1:
            embedding_array = embedding_array[0]
        
        # 2. Infer signal from Master Engine
        kaldra_signal = self._engine.infer_from_embedding(embedding_array)
        
        # 3. Convert to GeoSignal
        geo_signal = build_geo_signal_from_kaldra(
            signal=kaldra_signal,
            region=region,
            source=source,
            top_k=self.config.top_k_archetypes
        )
        
        logger.info(
            f"GEO analysis complete: risk_level={geo_signal.risk_level}, "
            f"tw_triggered={geo_signal.tw_triggered}, region={region}"
        )
        
        return geo_signal
