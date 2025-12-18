"""
Adaptive State-Plane Mapping for TW369.

This module provides context-aware plane weight calculation without modifying
the core TW369 mathematics.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Literal, Optional


DomainType = Literal["ALPHA", "GEO", "PRODUCT", "SAFEGUARD", "DEFAULT"]


@dataclass
class AdaptiveMappingContext:
    """
    Context used for adaptive state-plane mapping.

    This context is intentionally generic and independent of TW369 internals.
    """
    domain: DomainType = "DEFAULT"
    severity: float = 0.0  # [0, 1], as computed by TW369
    instability_index: float = 0.0  # any non-negative float
    time_horizon: Literal["short", "medium", "long"] = "medium"
    narrative_type: Optional[str] = None   # e.g., 'crisis', 'optimistic', 'policy'
    country: Optional[str] = None
    sector: Optional[str] = None


@dataclass
class PlaneWeights:
    """
    Normalized weights for planes 3, 6, 9.
    They always satisfy:
        w3 >= 0, w6 >= 0, w9 >= 0
        w3 + w6 + w9 = 1
    """
    plane3: float
    plane6: float
    plane9: float


@dataclass
class PlaneMappingResult:
    """
    Result of adaptive mapping:
    - layer_primary_plane: primary assignment for each Kindra layer
    - plane_weights: global weights applied to planes 3, 6, 9
    """
    layer_primary_plane: Dict[int, int]  # {1: 3, 2: 6, 3: 9} by default
    plane_weights: PlaneWeights
    metadata: Dict[str, Any]


class AdaptiveStatePlaneMapper:
    """
    Adaptive state-plane mapper for TW369.

    It starts from a domain-specific baseline (config) and then shifts weight
    between planes as a function of severity, time horizon and narrative type.

    IMPORTANT:
    - It does NOT change the TWState structure.
    - It does NOT modify TW369 math: it only provides weights and metadata.
    """

    def __init__(
        self,
        config: Dict[str, Any],
    ) -> None:
        self._config = config
        self._severity_thresholds = config.get("severity_thresholds", {})
        self._max_shift = float(config.get("max_shift", 0.3))
        self._domains = config.get("domains", {})

    def _get_baseline_for_domain(self, domain: DomainType) -> PlaneWeights:
        key = domain if domain in self._domains else "DEFAULT"
        d = self._domains.get(key, self._domains.get("DEFAULT", {}))

        p3 = float(d.get("plane3", 0.4))
        p6 = float(d.get("plane6", 0.35))
        p9 = float(d.get("plane9", 0.25))
        return self._normalize_weights(PlaneWeights(p3, p6, p9))

    @staticmethod
    def _normalize_weights(w: PlaneWeights) -> PlaneWeights:
        total = max(1e-9, w.plane3 + w.plane6 + w.plane9)
        return PlaneWeights(
            plane3=w.plane3 / total,
            plane6=w.plane6 / total,
            plane9=w.plane9 / total,
        )

    def _classify_severity(self, severity: float) -> str:
        low = float(self._severity_thresholds.get("low", 0.3))
        med = float(self._severity_thresholds.get("medium", 0.6))
        high = float(self._severity_thresholds.get("high", 0.8))

        if severity < low:
            return "low"
        if severity < med:
            return "medium"
        if severity < high:
            return "high"
        return "extreme"

    def _compute_shift_factor(self, severity: float) -> float:
        """
        Maps severity in [0,1] to a shift factor in [0, max_shift].

        Idea:
        - Below low: near 0 shift
        - Around medium: ~0.5 * max_shift
        - Above high: close to max_shift
        """
        sev = max(0.0, min(1.0, severity))
        return self._max_shift * sev  # linear for now, can be changed in future

    def infer_mapping(self, ctx: AdaptiveMappingContext) -> PlaneMappingResult:
        """
        Compute adaptive plane weights and primary mapping given context.

        Primary mapping remains:
            Layer 1 -> Plane 3
            Layer 2 -> Plane 6
            Layer 3 -> Plane 9

        Adaptation happens through plane_weights.
        """
        baseline = self._get_baseline_for_domain(ctx.domain)
        sev_class = self._classify_severity(ctx.severity)
        shift_factor = self._compute_shift_factor(ctx.severity)

        w3, w6, w9 = baseline.plane3, baseline.plane6, baseline.plane9

        # RULES:
        # - ALPHA: crises puxam mais plano 6 (tensão) e 9 (estrutura), tirando peso de 3
        # - GEO: alta severidade / horizonte longo puxam forte para plano 9
        # - PRODUCT: curto prazo enfatiza 3/6 (experiência + discurso)
        # - SAFEGUARD: estados mais críticos puxam 6/9 (risco / governança)
        # - DEFAULT: leve bias para plane 6 quando severidade alta

        if ctx.domain == "ALPHA":
            if sev_class in ("high", "extreme"):
                # até shift_factor, movendo parte de w3 -> w6 e w9
                delta = shift_factor
                take_from_3 = min(delta, w3)
                w3 -= take_from_3 * 0.7
                w6 += take_from_3 * 0.5
                w9 += take_from_3 * 0.2

        elif ctx.domain == "GEO":
            if sev_class in ("medium", "high", "extreme") or ctx.time_horizon == "long":
                delta = shift_factor
                # mover de 3 e 6 para 9
                take = min(delta, (w3 + w6) * 0.5)
                w3 -= take * 0.4
                w6 -= take * 0.6
                w9 += take

        elif ctx.domain == "PRODUCT":
            if ctx.time_horizon == "short" and sev_class in ("medium", "high"):
                # foco em superfície (3) e tensão (6)
                delta = shift_factor
                take_from_9 = min(delta, w9)
                w9 -= take_from_9
                w3 += take_from_9 * 0.6
                w6 += take_from_9 * 0.4

        elif ctx.domain == "SAFEGUARD":
            if sev_class in ("high", "extreme") or ctx.narrative_type == "crisis":
                # reforço em 6 (tensão / risco) + 9 (estrutura)
                delta = shift_factor
                take_from_3 = min(delta, w3)
                w3 -= take_from_3
                w6 += take_from_3 * 0.5
                w9 += take_from_3 * 0.5

        else:  # DEFAULT
            if sev_class in ("high", "extreme"):
                delta = shift_factor
                take_from_3 = min(delta, w3)
                w3 -= take_from_3 * 0.5
                w6 += take_from_3 * 0.5

        # Clamp and normalize
        w3 = max(0.0, w3)
        w6 = max(0.0, w6)
        w9 = max(0.0, w9)
        weights = self._normalize_weights(PlaneWeights(w3, w6, w9))

        # Primary mapping remains static for now (future: truly dynamic reassignment)
        primary = {1: 3, 2: 6, 3: 9}

        meta: Dict[str, Any] = {
            "domain": ctx.domain,
            "severity": ctx.severity,
            "instability_index": ctx.instability_index,
            "time_horizon": ctx.time_horizon,
            "narrative_type": ctx.narrative_type,
            "country": ctx.country,
            "sector": ctx.sector,
            "severity_class": sev_class,
            "shift_factor": shift_factor,
            "baseline": {
                "plane3": baseline.plane3,
                "plane6": baseline.plane6,
                "plane9": baseline.plane9,
            },
        }

        return PlaneMappingResult(
            layer_primary_plane=primary,
            plane_weights=weights,
            metadata=meta,
        )
