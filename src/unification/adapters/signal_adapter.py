"""
Signal Adapter for KALDRA v3.0.

Converts UnifiedContext to standardized signal format.
"""
from typing import Dict, Any, Optional, List
import logging
import uuid
from datetime import datetime, timezone

from ..states.unified_state import UnifiedContext

try:
    from src.data.repositories.signal_repository import SignalRepository
except ImportError:
    SignalRepository = None  # Graceful degradation if not available

try:
    from src.data.repositories.story_event_repository import StoryEventRepository
except ImportError:
    StoryEventRepository = None  # Graceful degradation

logger = logging.getLogger(__name__)


class SignalAdapter:
    """
    Adapter for converting UnifiedContext to standardized signal format.
    
    Produces a consistent JSON-serializable output regardless of
    which stages were executed or which failed.
    
    Now includes automatic persistence to Supabase via SignalRepository.
    """
    
    def __init__(
        self,
        signal_repository: Optional[Any] = None,
        story_event_repository: Optional[Any] = None,
        enable_persistence: bool = True,
        enable_story_events_persistence: bool = True,
    ) -> None:
        """
        Initialize SignalAdapter.
        
        Args:
            signal_repository: Optional SignalRepository instance for testing
            story_event_repository: Optional StoryEventRepository for testing
            enable_persistence: Whether to persist signals to database
            enable_story_events_persistence: Whether to persist story events
        """
        # Signal persistence
        self.enable_persistence = enable_persistence and SignalRepository is not None
        self.signal_repository = signal_repository
        
        if self.enable_persistence and self.signal_repository is None:
            try:
                self.signal_repository = SignalRepository()
                logger.info("SignalAdapter: Signal persistence enabled")
            except Exception as e:
                logger.warning(f"SignalAdapter: Could not initialize SignalRepository: {e}")
                self.enable_persistence = False
        
        # Story events persistence
        self.enable_story_events_persistence = (
            enable_story_events_persistence and 
            StoryEventRepository is not None and
            self.enable_persistence  # Require signal persistence too
        )
        self.story_event_repository = story_event_repository
        
        if self.enable_story_events_persistence and self.story_event_repository is None:
            try:
                self.story_event_repository = StoryEventRepository()
                logger.info("SignalAdapter: Story events persistence enabled")
            except Exception as e:
                logger.warning(f"SignalAdapter: Could not initialize StoryEventRepository: {e}")
                self.enable_story_events_persistence = False
    
    def to_signal(self, context: UnifiedContext) -> Dict[str, Any]:
        """
        Convert UnifiedContext to standardized signal format.
        
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
        }
        
        # Input
        if context.input_ctx:
            signal["input"] = {
                "text": context.input_ctx.text,
                "bias_score": context.input_ctx.bias_score,
                "tau_input": context.input_ctx.tau_input.to_dict() if context.input_ctx.tau_input else None
            }
        
        # Kindra
        if context.kindra_ctx:
            signal["kindra"] = context.kindra_ctx.to_dict()
        
        # Archetypes
        if context.archetype_ctx:
            signal["archetypes"] = context.archetype_ctx.to_dict()
        
        # Drift
        if context.drift_ctx:
            signal["drift"] = context.drift_ctx.to_dict()
        
        # Meta
        if context.meta_ctx:
            signal["meta"] = context.meta_ctx.to_dict()
        
        # Story
        if context.story_ctx:
            signal["story"] = context.story_ctx.to_dict()
        
        # Risk
        if context.risk_ctx:
            signal["risk"] = {
                "tau_output": context.risk_ctx.tau_output.to_dict() if context.risk_ctx.tau_output else None,
                "safeguard": context.risk_ctx.safeguard.to_dict() if context.risk_ctx.safeguard else None,
                "final_risk": context.risk_ctx.final_risk,
                "risk_score": context.risk_ctx.risk_score
            }
        
        # Summary
        summary = getattr(context.global_ctx, 'summary', None)
        if summary:
            signal["summary"] = summary
        else:
            signal["summary"] = {
                "confidence": 1.0,
                "routing": context.global_ctx.mode,
                "degraded": context.global_ctx.degraded
            }
        
        # Persist to database
        persisted_signal_id = None
        if self.enable_persistence:
            result = self._persist_signal(context, signal)
            # Extract signal_id from persisted result if available
            if isinstance(result, list) and len(result) > 0:
                persisted_signal_id = result[0].get('id')
            elif isinstance(result, dict) and 'id' in result:
                persisted_signal_id = result.get('id')
        
        # Persist story events if enabled
        if self.enable_story_events_persistence:
            self._persist_story_events(context, persisted_signal_id)
        
        return signal
    
    def _persist_signal(self, context: UnifiedContext, signal_dict: Dict[str, Any]) -> Any:
        """
        Persist signal to Supabase.
        
        Errors are logged but never raise to prevent breaking the pipeline.
        
        Args:
            context: UnifiedContext from pipeline
            signal_dict: Generated signal dictionary
        
        Returns:
            Created signal result or None
        """
        try:
            payload = self._build_signal_payload(context, signal_dict)
            result = self.signal_repository.create_signal(payload)
            
            if isinstance(result, dict) and "error" in result:
                logger.warning(f"SignalAdapter: Failed to persist signal: {result}")
                return None
            else:
                logger.debug(f"SignalAdapter: Signal persisted with ID: {payload.get('id')}")
                return result
        
        except Exception as e:
            # Critical rule: persistence failures NEVER break the pipeline
            logger.error(f"SignalAdapter: Unexpected error persisting signal: {repr(e)}")
            return None
    
    def _persist_story_events(self, context: UnifiedContext, signal_id: Optional[str]) -> None:
        """
        Persist story events to Supabase.
        
        Errors are logged but never raise to prevent breaking the pipeline.
        
        Args:
            context: UnifiedContext from pipeline
            signal_id: Parent signal ID (optional)
        """
        # Skip if persistence is disabled
        if not self.enable_story_events_persistence:
            return
        
        try:
            events = self._extract_story_events(context, signal_id)
            
            if not events:
                logger.debug("SignalAdapter: No story events to persist")
                return
            
            # Use bulk create if multiple events
            if len(events) > 1:
                result = self.story_event_repository.bulk_create_events(events)
            else:
                result = self.story_event_repository.create_event(events[0])
            
            if isinstance(result, dict) and "error" in result:
                logger.warning(f"SignalAdapter: Failed to persist story events: {result}")
            else:
                logger.debug(f"SignalAdapter: Persisted {len(events)} story events")
        
        except Exception as e:
            # Critical rule: persistence failures NEVER break the pipeline
            logger.error(f"SignalAdapter: Unexpected error persisting story events: {repr(e)}")
    
    @staticmethod
    def _extract_story_events(context: UnifiedContext, signal_id: Optional[str]) -> List[Dict[str, Any]]:
        """
        Extract story events from UnifiedContext.
        
        Args:
            context: UnifiedContext from pipeline
            signal_id: Parent signal ID
        
        Returns:
            List of event payloads
        """
        events = []
        
        # Try to find events in story_ctx
        if context.story_ctx and hasattr(context.story_ctx, 'events'):
            story_events = context.story_ctx.events
            
            if story_events and isinstance(story_events, list):
                for ev in story_events:
                    # Build payload from event
                    if isinstance(ev, dict):
                        payload = {
                            "signal_id": signal_id,
                            "stream_id": ev.get("stream_id"),
                            "text": ev.get("text") or ev.get("description"),
                            "delta144_state": ev.get("delta144_state") or ev.get("state"),
                            "polarities": ev.get("polarities"),
                            "meta": {
                                "stage": ev.get("stage"),
                                "kind": ev.get("kind"),
                                "source": "kaldra_pipeline",
                            }
                        }
                    else:
                        # Handle event objects with attributes
                        payload = {
                            "signal_id": signal_id,
                            "stream_id": getattr(ev, 'stream_id', None),
                            "text": getattr(ev, 'text', None) or getattr(ev, 'description', None),
                            "delta144_state": getattr(ev, 'delta144_state', None) or getattr(ev, 'state', None),
                            "polarities": getattr(ev, 'polarities', None),
                            "meta": {
                                "stage": getattr(ev, 'stage', None),
                                "kind": getattr(ev, 'kind', None),
                                "source": "kaldra_pipeline",
                            }
                        }
                    
                    events.append(payload)
        
        return events
    
    @staticmethod
    def _build_signal_payload(context: UnifiedContext, signal_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert UnifiedContext to Supabase signals table format.
        
        Args:
            context: UnifiedContext from pipeline
            signal_dict: Full signal dictionary
        
        Returns:
            Dictionary matching signals table schema
        """
        signal_id = str(uuid.uuid4())
        
        # Extract domain
        domain = "alpha"  # Default
        if context.meta_ctx and hasattr(context.meta_ctx, 'domain'):
            domain = context.meta_ctx.domain
        
        # Extract title and summary
        title = "KALDRA Signal"
        summary = ""
        if context.input_ctx:
            # Use first 100 chars of text as title
            text = getattr(context.input_ctx, 'text', '')
            if text:
                title = text[:100] + ("..." if len(text) > 100 else "")
                summary = text[:500]
        
        # Extract Delta144 state
        delta144_state = None
        dominant_archetype = None
        if context.archetype_ctx:
            if hasattr(context.archetype_ctx, 'delta144_state') and context.archetype_ctx.delta144_state:
                delta144_state = getattr(context.archetype_ctx.delta144_state, 'state_id', None)
            if hasattr(context.archetype_ctx, 'delta12') and context.archetype_ctx.delta12:
                # Find dominant archetype
                delta12_dict = context.archetype_ctx.delta12.to_dict() if hasattr(context.archetype_ctx.delta12, 'to_dict') else {}
                if delta12_dict:
                    dominant_archetype = max(delta12_dict.items(), key=lambda x: x[1])[0] if delta12_dict else None
       
        # Extract polarities
        dominant_polarity = None
        if context.archetype_ctx and hasattr(context.archetype_ctx, 'polarity_scores'):
            polarities = context.archetype_ctx.polarity_scores or {}
            if polarities:
                dominant_polarity = max(polarities.items(), key=lambda x: x[1])[0] if polarities else None
        
        # Extract TW regime
        tw_regime = None
        if context.drift_ctx and hasattr(context.drift_ctx, 'regime'):
            tw_regime = context.drift_ctx.regime
        
        # Extract story stage
        journey_stage = None
        if context.story_ctx and hasattr(context.story_ctx, 'journey_stage'):
            journey_stage = context.story_ctx.journey_stage
        
        # Calculate importance (basic heuristic)
        importance = 0.5  # Default
        if context.meta_ctx and hasattr(context.meta_ctx, 'importance'):
            importance = context.meta_ctx.importance
        
        # Confidence (from summary or default)
        confidence = signal_dict.get('summary', {}).get('confidence', 0.8)
        
        return {
            "id": signal_id,
            "domain": domain,
            "title": title,
            "summary": summary,
            "delta144_state": delta144_state,
            "dominant_archetype": dominant_archetype,
            "dominant_polarity": dominant_polarity,
            "tw_regime": tw_regime,
            "journey_stage": journey_stage,
            "importance": importance,
            "confidence": confidence,
            "raw_payload": signal_dict,  # Store full signal as JSONB
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    
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
