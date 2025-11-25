"""
Unit tests for adaptive state-plane mapping.
"""

import pytest
from src.tw369.state_plane_mapping import (
    AdaptiveStatePlaneMapper,
    AdaptiveMappingContext,
    PlaneWeights,
)
from src.tw369.state_plane_mapping_utils import apply_plane_weights_to_tensions


def _make_default_config():
    return {
        "enabled": True,
        "domains": {
            "ALPHA":   {"plane3": 0.50, "plane6": 0.35, "plane9": 0.15},
            "GEO":     {"plane3": 0.20, "plane6": 0.30, "plane9": 0.50},
            "PRODUCT": {"plane3": 0.55, "plane6": 0.30, "plane9": 0.15},
            "SAFEGUARD": {"plane3": 0.30, "plane6": 0.30, "plane9": 0.40},
            "DEFAULT": {"plane3": 0.40, "plane6": 0.35, "plane9": 0.25},
        },
        "severity_thresholds": {"low": 0.3, "medium": 0.6, "high": 0.8},
        "max_shift": 0.3,
    }


class TestAdaptiveStatePlaneMapping:
    def test_baseline_weights_sum_to_one(self):
        cfg = _make_default_config()
        mapper = AdaptiveStatePlaneMapper(cfg)

        ctx = AdaptiveMappingContext(domain="ALPHA", severity=0.0)
        res = mapper.infer_mapping(ctx)

        w = res.plane_weights
        total = w.plane3 + w.plane6 + w.plane9
        assert abs(total - 1.0) < 1e-6

    def test_geo_high_severity_increases_plane9_weight(self):
        cfg = _make_default_config()
        mapper = AdaptiveStatePlaneMapper(cfg)

        # baseline (for domain GEO)
        baseline_ctx = AdaptiveMappingContext(domain="GEO", severity=0.0, time_horizon="medium")
        baseline = mapper.infer_mapping(baseline_ctx).plane_weights

        # high severity + long horizon
        ctx = AdaptiveMappingContext(
            domain="GEO",
            severity=0.9,
            time_horizon="long",
            narrative_type="crisis",
        )
        res = mapper.infer_mapping(ctx)
        w = res.plane_weights

        assert w.plane9 > baseline.plane9
        # weights still sum to ~1
        assert abs(w.plane3 + w.plane6 + w.plane9 - 1.0) < 1e-6

    def test_alpha_extreme_severity_reduces_plane3_weight(self):
        cfg = _make_default_config()
        mapper = AdaptiveStatePlaneMapper(cfg)

        # baseline
        bctx = AdaptiveMappingContext(domain="ALPHA", severity=0.0)
        baseline = mapper.infer_mapping(bctx).plane_weights

        # extreme severity
        ctx = AdaptiveMappingContext(domain="ALPHA", severity=1.0)
        res = mapper.infer_mapping(ctx)
        w = res.plane_weights

        assert w.plane3 < baseline.plane3
        assert abs(w.plane3 + w.plane6 + w.plane9 - 1.0) < 1e-6

    def test_apply_plane_weights_to_tensions_scales_values(self):
        mapping_cfg = _make_default_config()
        mapper = AdaptiveStatePlaneMapper(mapping_cfg)

        ctx = AdaptiveMappingContext(domain="PRODUCT", severity=0.5, time_horizon="short")
        mapping = mapper.infer_mapping(ctx)

        tensions = {3: 1.0, 6: 2.0, 9: 3.0}
        weighted = apply_plane_weights_to_tensions(tensions, mapping)

        # Check keys and scaling
        assert set(weighted.keys()) == {3, 6, 9}
        assert weighted[3] == tensions[3] * mapping.plane_weights.plane3
        assert weighted[6] == tensions[6] * mapping.plane_weights.plane6
        assert weighted[9] == tensions[9] * mapping.plane_weights.plane9

    def test_all_domains_produce_valid_weights(self):
        cfg = _make_default_config()
        mapper = AdaptiveStatePlaneMapper(cfg)

        domains = ["ALPHA", "GEO", "PRODUCT", "SAFEGUARD", "DEFAULT"]
        
        for domain in domains:
            ctx = AdaptiveMappingContext(domain=domain, severity=0.5)
            res = mapper.infer_mapping(ctx)
            w = res.plane_weights
            
            # All weights non-negative
            assert w.plane3 >= 0.0
            assert w.plane6 >= 0.0
            assert w.plane9 >= 0.0
            
            # Sum to 1
            assert abs(w.plane3 + w.plane6 + w.plane9 - 1.0) < 1e-6

    def test_metadata_contains_expected_fields(self):
        cfg = _make_default_config()
        mapper = AdaptiveStatePlaneMapper(cfg)

        ctx = AdaptiveMappingContext(
            domain="SAFEGUARD",
            severity=0.7,
            time_horizon="long",
            narrative_type="crisis",
            country="BR",
            sector="energy"
        )
        res = mapper.infer_mapping(ctx)

        meta = res.metadata
        assert meta["domain"] == "SAFEGUARD"
        assert meta["severity"] == 0.7
        assert meta["time_horizon"] == "long"
        assert meta["narrative_type"] == "crisis"
        assert meta["country"] == "BR"
        assert meta["sector"] == "energy"
        assert "severity_class" in meta
        assert "shift_factor" in meta
        assert "baseline" in meta
