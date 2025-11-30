"""
Context Manager for KALDRA v3.0.

Manages the unified context throughout pipeline execution.
"""
from typing import Optional
from .unified_state import UnifiedContext, GlobalContext


class ContextManager:
    """
    Manages the unified context throughout pipeline execution.
    
    Provides utilities for context creation, validation, and transformation.
    """
    
    @staticmethod
    def create_context(
        text: str,
        mode: str = "full",
        request_id: Optional[str] = None
    ) -> UnifiedContext:
        """
        Create a new unified context for pipeline execution.
        
        Args:
            text: Input text
            mode: Execution mode
            request_id: Optional request ID (auto-generated if not provided)
            
        Returns:
            Initialized UnifiedContext
        """
        global_ctx = GlobalContext(mode=mode)
        if request_id:
            global_ctx.request_id = request_id
        
        context = UnifiedContext(global_ctx=global_ctx)
        return context
    
    @staticmethod
    def validate_context(context: UnifiedContext) -> bool:
        """
        Validate that a context is properly formed.
        
        Args:
            context: Context to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(context, UnifiedContext):
            return False
        
        if not context.global_ctx:
            return False
        
        return True
    
    @staticmethod
    def mark_degraded(context: UnifiedContext, reason: str = "") -> None:
        """
        Mark a context as degraded (partial failure).
        
        Args:
            context: Context to mark
            reason: Optional reason for degradation
        """
        context.global_ctx.degraded = True
        if reason and 'degradation_reasons' not in context.global_ctx.__dict__:
            context.global_ctx.__dict__['degradation_reasons'] = []
        if reason:
            context.global_ctx.__dict__['degradation_reasons'].append(reason)
