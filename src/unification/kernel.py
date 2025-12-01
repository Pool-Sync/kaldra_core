"""
Unified Kernel for KALDRA v3.0.

The kernel is the main entry point for all KALDRA operations.
It loads all v2.9 engines and provides a single, unified interface.
"""
from typing import Optional, Dict, Any
import logging

from .registry import ModuleRegistry, get_global_registry
from .states.unified_state import UnifiedContext
from .states.unified_context import ContextManager

# v2.9 engine imports
from src.core.embedding_generator import EmbeddingGenerator, EmbeddingConfig
from src.archetypes.delta144_engine import Delta144Engine
from src.bias.detector import BiasDetector
from src.tau.tau_layer import TauLayer
from src.safeguard.safeguard_engine import SafeguardEngine
from src.config import (
    KALDRA_EMBEDDINGS_MODE,
    KALDRA_EMBEDDINGS_API_KEY,
    KALDRA_EMBEDDINGS_MODEL
)

logger = logging.getLogger(__name__)


class UnifiedKernel:
    """
    Unified Kernel for KALDRA v3.0.
    
    The kernel is the main entry point that:
    1. Loads all v2.9 engines
    2. Provides a single unified interface
    3. Maintains backward compatibility
    4. Handles errors gracefully
    
    Usage:
        kernel = UnifiedKernel()
        result = kernel.run("Your text here", mode="full")
    """
    
    def __init__(
        self,
        registry: Optional[ModuleRegistry] = None,
        auto_load: bool = True
    ):
        """
        Initialize the Unified Kernel.
        
        Args:
            registry: Module registry (uses global if not provided)
            auto_load: Automatically load v2.9 engines
        """
        self.registry = registry or get_global_registry()
        self.loaded = False
        
        if auto_load:
            self.load_engines()
    
    def load_engines(self) -> None:
        """
        Load all v2.9 engines into the registry.
        
        This method initializes all core KALDRA engines and registers them
        for use by the pipeline.
        """
        if self.loaded:
            logger.warning("Engines already loaded, skipping")
            return
        
        logger.info("Loading KALDRA v2.9 engines...")
        
        try:
            # 1. Embedding Generator
            embedding_config = EmbeddingConfig(
                provider=KALDRA_EMBEDDINGS_MODE.lower(),
                model_name=KALDRA_EMBEDDINGS_MODEL,
                api_key=KALDRA_EMBEDDINGS_API_KEY,
                dim=256
            )
            if embedding_config.provider == "real":
                embedding_config.provider = "openai"
            
            embedding_gen = EmbeddingGenerator(config=embedding_config)
            self.registry.register(
                "embeddings",
                embedding_gen,
                version="2.3",
                description="Semantic embedding generation"
            )
            
            # 2. Delta144 Engine (Archetypes)
            delta144 = Delta144Engine.from_schema()
            self.registry.register(
                "archetypes",
                delta144,
                version="2.7",
                description="Archetypal analysis (Δ12, Δ144, Polarities)"
            )
            
            # 3. Bias Detector
            bias_detector = BiasDetector()
            self.registry.register(
                "bias",
                bias_detector,
                version="2.3",
                description="Bias detection and scoring"
            )
            
            # 4. Tau Layer
            tau_layer = TauLayer()
            self.registry.register(
                "tau",
                tau_layer,
                version="2.8",
                description="Epistemic reliability limiter"
            )
            
            # 5. Safeguard Engine
            safeguard = SafeguardEngine()
            self.registry.register(
                "safeguard",
                safeguard,
                version="2.8",
                description="Safety and risk mitigation"
            )
            
            # Mark registry as initialized
            self.registry.mark_initialized()
            self.loaded = True
            
            logger.info(f"Loaded {len(self.registry.list_modules())} engines successfully")
            
        except Exception as e:
            logger.error(f"Failed to load engines: {e}")
            raise
    
    def run(
        self,
        input_text: str,
        mode: str = "full",
        context: Optional[Dict[str, Any]] = None
    ) -> UnifiedContext:
        """
        Run the KALDRA pipeline on input text.
        
        This is the main entry point for all KALDRA operations.
        
        Args:
            input_text: Text to analyze
            mode: Execution mode
                - "signal": Fast, core pipeline only
                - "story": Full temporal analysis
                - "full": Complete analysis (default)
                - "safety-first": Strict safety checks
                - "exploratory": Maximum depth
            context: Optional context dictionary
            
        Returns:
            UnifiedContext with complete analysis results
            
        Raises:
            ValueError: If mode is invalid
            RuntimeError: If engines not loaded
        """
        if not self.loaded:
            raise RuntimeError("Engines not loaded. Call load_engines() first.")
        
        # Validate mode
        valid_modes = ["signal", "story", "full", "safety-first", "exploratory"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode '{mode}'. Must be one of: {valid_modes}")
        
        logger.info(f"Running KALDRA v3.0 (mode={mode})")
        
        # Import orchestrator (lazy import to avoid circular dependency)
        from .orchestrator import PipelineOrchestrator
        
        # Create orchestrator if not exists
        if not hasattr(self, 'orchestrator'):
            self.orchestrator = PipelineOrchestrator(self.registry)
        
        # Execute pipeline
        result = self.orchestrator.execute(input_text, mode=mode, context_dict=context)
        
        return result
    
    def get_module(self, name: str) -> Any:
        """
        Get a loaded module by name.
        
        Args:
            name: Module name
            
        Returns:
            The module instance
        """
        return self.registry.get(name)
    
    def list_modules(self) -> list:
        """List all loaded modules."""
        return self.registry.list_modules()
    
    def __repr__(self) -> str:
        return f"UnifiedKernel(loaded={self.loaded}, modules={len(self.registry.list_modules())})"
