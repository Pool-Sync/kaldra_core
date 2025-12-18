"""
Multi-format output support for KALDRA Explainability (v3.4 Phase 3).

Provides Markdown rendering for explanations.
"""
from typing import Optional, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)


class ExplanationMarkdownRenderer:
    """
    Renders Explanation objects to Markdown format.
    
    Supports multiple template variants for different use cases.
    
    Example:
        >>> renderer = ExplanationMarkdownRenderer()
        >>> markdown = renderer.render(explanation, variant="default")
        >>> print(markdown)
    """
    
    def __init__(self, templates: Optional[Dict[str, str]] = None):
        """
        Initialize Markdown renderer.
        
        Args:
            templates: Optional custom templates dict {variant_name: template_content}
        """
        self.templates = templates or self._load_default_templates()
        logger.info(f"ExplanationMarkdownRenderer initialized with {len(self.templates)} templates")
    
    def _load_default_templates(self) -> Dict[str, str]:
        """Load default Markdown templates from templates/ directory."""
        templates = {}
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        
        template_files = {
            "default": "explanation_markdown.md",
            "compact": "explanation_markdown_compact.md"
        }
        
        for variant, filename in template_files.items():
            template_path = os.path.join(template_dir, filename)
            try:
                with open(template_path, 'r') as f:
                    templates[variant] = f.read()
            except Exception as e:
                logger.warning(f"Could not load template '{variant}': {e}")
                # Fallback minimal template
                templates[variant] = "# Explanation\n\n{summary}\n"
        
        return templates
    
    def render(self, explanation: Any, variant: str = "default") -> str:
        """
        Render Explanation to Markdown.
        
        Args:
            explanation: Explanation object to render
            variant: Template variant to use ("default" or "compact")
        
        Returns:
            Markdown string
        """
        template = self.templates.get(variant, self.templates.get("default", ""))
        
        if not template:
            raise ValueError(f"No template available for variant '{variant}'")
        
        # Build template variables
        variables = self._extract_variables(explanation)
        
        # Perform substitution
        try:
            markdown = self._substitute_variables(template, variables)
            return markdown
        except Exception as e:
            logger.error(f"Markdown rendering failed: {e}")
            # Fallback to minimal output
            return f"# Explanation\n\n{explanation.summary}\n"
    
    def _extract_variables(self, explanation: Any) -> Dict[str, str]:
        """Extract variables from Explanation for template substitution."""
        variables = {
            "summary": explanation.summary or "No summary available",
            "confidence_overall": 0.0,
            "confidence_components": "",
            "drivers": "",
            "archetypes": "",
            "polarities": "",
            "narrative": "",
            "decision_trace": "",
            "key_points": ""
        }
        
        # Confidence
        if hasattr(explanation, 'confidence') and explanation.confidence:
            conf = explanation.confidence
            variables["confidence_overall"] = conf.overall
            
            # Components
            if conf.components:
                comp_lines = ["### Component Breakdown\n"]
                for comp in conf.components:
                    comp_lines.append(f"- **{comp.name}**: {comp.score:.2f} — {comp.reason}")
                variables["confidence_components"] = "\n".join(comp_lines)
        
        # Details sections
        if hasattr(explanation, 'details') and explanation.details:
            details = explanation.details
            variables["drivers"] = details.get("drivers", "No key drivers identified")
            variables["archetypes"] = details.get("archetypes", "No archetypal data available")
            variables["polarities"] = details.get("polarities", "No polarity data available")
            variables["narrative"] = details.get("narrative", "No narrative dynamics data available")
        
        # Decision trace
        if hasattr(explanation, 'trace') and explanation.trace:
            trace_lines = ["## Decision Trace\n"]
            for step in explanation.trace:
                trace_lines.append(f"- **{step.step}** (weight: {step.weight:.2f}): {step.description}")
            variables["decision_trace"] = "\n".join(trace_lines)
        
        # Key points for compact view
        key_points = []
        if hasattr(explanation, 'confidence') and explanation.confidence:
            if explanation.confidence.components:
                top_comps = sorted(explanation.confidence.components, key=lambda c: c.score, reverse=True)[:3]
                for comp in top_comps:
                    key_points.append(f"- {comp.name}: {comp.score:.2f}")
        
        if key_points:
            variables["key_points"] = "\n".join(key_points)
        else:
            variables["key_points"] = "- No detailed metrics available"
        
        return variables
    
    def _substitute_variables(self, template: str, variables: Dict[str, Any]) -> str:
        """Substitute variables into template string."""
        result = template
        
        for key, value in variables.items():
            placeholder = f"{{{key}}}"
            
            # Handle format specs like {confidence_overall:.2f}
            if isinstance(value, (int, float)):
                # Replace both with and without format spec
                result = result.replace(f"{{{key}:.2f}}", f"{value:.2f}")
                result = result.replace(placeholder, str(value))
            else:
                result = result.replace(placeholder, str(value))
        
        return result
