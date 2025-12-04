"""
Explanation Generator for KALDRA v3.4 Phase 1.

Generates natural language explanations for KALDRA signals with LLM support
and deterministic fallback mechanisms.
"""
from typing import Optional, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)


class Explanation:
    """
    Container for a generated explanation.
    
    Attributes:
        summary: High-level summary of the explanation
        details: Detailed breakdown by component
        raw_facts: Raw extracted facts from the signal
    """
    
    def __init__(self, summary: str, details: Dict[str, Any], raw_facts: Dict[str, Any]):
        self.summary = summary
        self.details = details
        self.raw_facts = raw_facts
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "summary": self.summary,
            "details": self.details,
            "raw_facts": self.raw_facts
        }


class ExplanationGenerator:
    """
    Generates natural language explanations for KALDRA signals.
    
    Features:
    - LLM-based generation (when available)
    - Template-based fallback
    - Barebones fallback (always works)
    
    Fallback chain: LLM → Template → Barebones
    
    Example:
        >>> generator = ExplanationGenerator()
        >>> explanation = generator.generate(unified_context)
        >>> print(explanation.summary)
    """
    
    def __init__(self, llm: Optional[Any] = None, templates: Optional[Dict[str, str]] = None):
        """
        Initialize explanation generator.
        
        Args:
            llm: Optional LLM instance for generation (e.g., OpenAI client)
            templates: Optional custom templates (default: loads from templates/)
        """
        self.llm = llm
        self.templates = templates or self._load_default_template()
        logger.info(f"ExplanationGenerator initialized: llm={'present' if llm else 'none'}")
    
    def _load_default_template(self) -> Dict[str, str]:
        """Load the default base template from templates/."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "templates",
            "base_template.md"
        )
        
        try:
            with open(template_path, 'r') as f:
                template_content = f.read()
            return {"base": template_content}
        except Exception as e:
            logger.warning(f"Could not load template: {e}")
            return {"base": "# Explanation\n\n{{summary}}\n\n{{details}}"}
    
    def generate(self, context: Any) -> Explanation:
        """
        Generate explanation from UnifiedContext.
        
        Args:
            context: UnifiedContext from KALDRA pipeline
        
        Returns:
            Explanation object with summary, details, and raw facts
        """
        # Extract facts from context
        facts = self._extract_facts(context)
        
        # Try LLM generation first
        if self.llm:
            try:
                return self._generate_with_llm(facts)
            except Exception as e:
                logger.warning(f"LLM generation failed: {e}, falling back to template")
        
        # Fallback to template
        try:
            return self._generate_with_template(facts)
        except Exception as e:
            logger.warning(f"Template generation failed: {e}, falling back to barebones")
        
        # Final fallback: barebones
        return self._generate_barebones(facts)
    
    def _extract_facts(self, context: Any) -> Dict[str, Any]:
        """
        Extract relevant facts from UnifiedContext.
        
        Args:
            context: UnifiedContext
        
        Returns:
            Dictionary of extracted facts
        """
        facts = {
            "delta144_state": None,
            "polarities": {},
            "journey_stage": None,
            "drift_regime": None,
            "divergence": None,
            "archetypes": {},
            "meta_scores": {}
        }
        
        try:
            # Extract archetype data
            if hasattr(context, 'archetype_ctx') and context.archetype_ctx:
                arch_ctx = context.archetype_ctx
                
                # Delta144 state
                if hasattr(arch_ctx, 'delta144_state') and arch_ctx.delta144_state:
                    state_id = getattr(arch_ctx.delta144_state, 'state_id', None)
                    facts["delta144_state"] = state_id
                
                # Polarities
                if hasattr(arch_ctx, 'polarity_scores'):
                    facts["polarities"] = arch_ctx.polarity_scores or {}
                
                # Delta12 archetypes
                if hasattr(arch_ctx, 'delta12') and arch_ctx.delta12:
                    delta12 = arch_ctx.delta12
                    if hasattr(delta12, 'to_dict'):
                        facts["archetypes"] = delta12.to_dict()
            
            # Extract drift/TW369 data
            if hasattr(context, 'drift_ctx') and context.drift_ctx:
                drift_ctx = context.drift_ctx
                if hasattr(drift_ctx, 'regime'):
                    facts["drift_regime"] = drift_ctx.regime
            
            # Extract meta/journey data
            if hasattr(context, 'meta_ctx') and context.meta_ctx:
                meta_ctx = context.meta_ctx
                if hasattr(meta_ctx, 'campbell') and meta_ctx.campbell:
                    campbell = meta_ctx.campbell
                    if hasattr(campbell, 'label'):
                        facts["journey_stage"] = campbell.label
                
                # Extract meta scores
                meta_scores = {}
                if hasattr(meta_ctx, 'nietzsche') and meta_ctx.nietzsche:
                    meta_scores["nietzsche"] = meta_ctx.nietzsche.score
                if hasattr(meta_ctx, 'aurelius') and meta_ctx.aurelius:
                    meta_scores["aurelius"] = meta_ctx.aurelius.score
                if hasattr(meta_ctx, 'campbell') and meta_ctx.campbell:
                    meta_scores["campbell"] = meta_ctx.campbell.score
                facts["meta_scores"] = meta_scores
            
            # Extract multi-stream divergence (v3.3)
            if hasattr(context, 'multi_stream_ctx') and context.multi_stream_ctx:
                ms_ctx = context.multi_stream_ctx
                if hasattr(ms_ctx, 'max_divergence'):
                    facts["divergence"] = ms_ctx.max_divergence
        
        except Exception as e:
            logger.warning(f"Error extracting facts: {e}")
        
        return facts
    
    def _generate_with_llm(self, facts: Dict[str, Any]) -> Explanation:
        """
        Generate explanation using LLM.
        
        Args:
            facts: Extracted facts
        
        Returns:
            Explanation object
        """
        # Build prompt
        prompt = self._build_llm_prompt(facts)
        
        # Call LLM (this is a placeholder - actual implementation depends on LLM API)
        # For now, raise NotImplementedError to trigger fallback
        if not hasattr(self.llm, 'generate'):
            raise NotImplementedError("LLM does not have generate method")
        
        response = self.llm.generate(prompt)
        
        # Parse response
        summary = response.get("summary", "LLM-generated explanation")
        details = response.get("details", {})
        
        return Explanation(
            summary=summary,
            details=details,
            raw_facts=facts
        )
    
    def _build_llm_prompt(self, facts: Dict[str, Any]) -> str:
        """Build prompt for LLM from facts."""
        prompt = "Generate a natural language explanation for the following KALDRA signal:\n\n"
        prompt += f"- Delta144 State: {facts.get('delta144_state', 'N/A')}\n"
        prompt += f"- Polarities: {facts.get('polarities', {})}\n"
        prompt += f"- Journey Stage: {facts.get('journey_stage', 'N/A')}\n"
        prompt += f"- Drift Regime: {facts.get('drift_regime', 'N/A')}\n"
        prompt += f"- Divergence: {facts.get('divergence', 'N/A')}\n"
        prompt += "\nProvide a concise summary and detailed breakdown."
        return prompt
    
    def _generate_with_template(self, facts: Dict[str, Any]) -> Explanation:
        """
        Generate explanation using template.
        
        Args:
            facts: Extracted facts
        
        Returns:
            Explanation object
        """
        template = self.templates.get("base", "")
        
        # Build sections
        summary = self._build_summary_from_facts(facts)
        drivers = self._build_drivers_section(facts)
        archetypes = self._build_archetypes_section(facts)
        polarities = self._build_polarities_section(facts)
        narrative = self._build_narrative_section(facts)
        
        # Fill template
        explanation_text = template.replace("{{summary}}", summary)
        explanation_text = explanation_text.replace("{{drivers}}", drivers)
        explanation_text = explanation_text.replace("{{archetypes}}", archetypes)
        explanation_text = explanation_text.replace("{{polarities}}", polarities)
        explanation_text = explanation_text.replace("{{narrative}}", narrative)
        
        details = {
            "drivers": drivers,
            "archetypes": archetypes,
            "polarities": polarities,
            "narrative": narrative
        }
        
        return Explanation(
            summary=summary,
            details=details,
            raw_facts=facts
        )
    
    def _build_summary_from_facts(self, facts: Dict[str, Any]) -> str:
        """Build summary from facts."""
        parts = []
        
        if facts.get("delta144_state"):
            parts.append(f"The signal is in the '{facts['delta144_state']}' archetypal state")
        
        if facts.get("journey_stage"):
            parts.append(f"at the '{facts['journey_stage']}' stage of the narrative journey")
        
        if facts.get("drift_regime"):
            parts.append(f"with drift regime '{facts['drift_regime']}'")
        
        if parts:
            return ". ".join(parts) + "."
        else:
            return "The signal indicates notable narrative activity."
    
    def _build_drivers_section(self, facts: Dict[str, Any]) -> str:
        """Build key drivers section."""
        drivers = []
        
        # Meta scores
        meta_scores = facts.get("meta_scores", {})
        for engine, score in meta_scores.items():
            if score > 0.5:
                drivers.append(f"- {engine.capitalize()}: {score:.2f}")
        
        # Divergence
        if facts.get("divergence"):
            drivers.append(f"- Multi-stream divergence: {facts['divergence']:.2f}")
        
        return "\n".join(drivers) if drivers else "- No significant drivers detected"
    
    def _build_archetypes_section(self, facts: Dict[str, Any]) -> str:
        """Build archetypes section."""
        delta144 = facts.get("delta144_state")
        archetypes = facts.get("archetypes", {})
        
        parts = []
        if delta144:
            parts.append(f"Primary archetypal state: **{delta144}**")
        
        if archetypes:
            parts.append("Delta12 archetypes:")
            for arch, score in sorted(archetypes.items(), key=lambda x: x[1], reverse=True)[:3]:
                parts.append(f"- {arch}: {score:.2f}")
        
        return "\n".join(parts) if parts else "No archetypal data available"
    
    def _build_polarities_section(self, facts: Dict[str, Any]) -> str:
        """Build polarities section."""
        polarities = facts.get("polarities", {})
        
        if not polarities:
            return "No polarity data available"
        
        parts = ["Polarity distribution:"]
        for polarity, score in sorted(polarities.items(), key=lambda x: x[1], reverse=True):
            parts.append(f"- {polarity}: {score:.2f}")
        
        return "\n".join(parts)
    
    def _build_narrative_section(self, facts: Dict[str, Any]) -> str:
        """Build narrative dynamics section."""
        journey = facts.get("journey_stage")
        drift = facts.get("drift_regime")
        divergence = facts.get("divergence")
        
        parts = []
        
        if journey:
            parts.append(f"Narrative journey stage: **{journey}**")
        
        if drift:
            parts.append(f"Drift regime: **{drift}**")
        
        if divergence is not None:
            convergent = "convergent" if divergence < 0.7 else "divergent"
            parts.append(f"Multi-stream analysis: **{convergent}** (divergence: {divergence:.2f})")
        
        return "\n".join(parts) if parts else "No narrative dynamics data available"
    
    def _generate_barebones(self, facts: Dict[str, Any]) -> Explanation:
        """
        Generate minimal barebones explanation (always succeeds).
        
        Args:
            facts: Extracted facts
        
        Returns:
            Explanation object
        """
        summary = "The signal indicates notable narrative activity driven by archetypes and polarity dynamics."
        
        details = {
            "note": "This is a barebones explanation generated due to LLM and template failures.",
            "available_data": list(k for k, v in facts.items() if v)
        }
        
        return Explanation(
            summary=summary,
            details=details,
            raw_facts=facts
        )
