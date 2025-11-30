"""
Unified API for KALDRA v3.0.

Provides a simple, public-facing API for KALDRA operations.
"""
from typing import Dict, List, Optional, Any

from ..kernel import UnifiedKernel
from ..states.unified_state import UnifiedContext


class UnifiedKaldra:
    """
    Unified API for KALDRA v3.0.
    
    This is the main public interface for KALDRA operations.
    It provides a simple, consistent API that abstracts away
    the complexity of the underlying pipeline.
    
    Usage:
        kaldra = UnifiedKaldra()
        result = kaldra.analyze("Your text here")
    """
    
    def __init__(self, auto_load: bool = True):
        """
        Initialize the Unified KALDRA API.
        
        Args:
            auto_load: Automatically load engines on initialization
        """
        self.kernel = UnifiedKernel(auto_load=auto_load)
    
    def analyze(
        self,
        text: str,
        mode: str = "full",
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze text using the complete KALDRA pipeline.
        
        Args:
            text: Text to analyze
            mode: Execution mode ("signal", "story", "full", "safety-first", "exploratory")
            options: Optional configuration options
            
        Returns:
            Dictionary with complete analysis results
        """
        # Import signal adapter
        from .signal_adapter import SignalAdapter
        
        # Run kernel
        context = self.kernel.run(text, mode=mode, context=options)
        
        # Convert to signal format
        result = SignalAdapter.to_signal(context)
        
        return result
    
    def analyze_batch(
        self,
        texts: List[str],
        mode: str = "full",
        options: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Analyze multiple texts in batch.
        
        Args:
            texts: List of texts to analyze
            mode: Execution mode
            options: Optional configuration options
            
        Returns:
            List of analysis results
        """
        results = []
        for text in texts:
            result = self.analyze(text, mode=mode, options=options)
            results.append(result)
        return results
    
    def get_version(self) -> str:
        """Get KALDRA version."""
        return "3.0.0"
    
    def list_modules(self) -> List[str]:
        """List loaded modules."""
        return self.kernel.list_modules()
    
    def __repr__(self) -> str:
        return f"UnifiedKaldra(version=3.0.0, modules={len(self.kernel.list_modules())})"
