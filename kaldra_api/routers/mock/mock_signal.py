"""
Mock signal endpoint for frontend prototyping.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/signal")
def get_mock_signal():
    """
    Return static mock signal for frontend development.
    
    This endpoint provides a complete v3.1 signal structure
    with realistic sample data for UI prototyping.
    """
    return {
        "version": "3.1.0",
        "request_id": "mock-request-123",
        "timestamp": 1701234567.89,
        "mode": "full",
        "degraded": False,
        
        # v3.1 Enhanced fields
        "preset_used": "alpha",
        "preset_config": {
            "mode": "full",
            "emphasis": {
                "kindra.layer1": 1.0,
                "meta.nietzsche": 1.0,
                "core.archetypes": 1.0
            },
            "thresholds": {
                "risk": 0.30,
                "confidence_min": 0.60
            },
            "output_format": "financial_brief"
        },
        
        # Meta engines
        "meta": {
            "nietzsche": {
                "will_to_power": 0.75,
                "ressentiment": 0.23,
                "master_slave_dynamic": "master",
                "amor_fati": 0.68,
                "perspectivism_score": 0.82
            },
            "aurelius": {
                "stoic_acceptance": 0.82,
                "control_dichotomy": "external",
                "virtue_alignment": 0.71,
                "tranquility_index": 0.65
            },
            "campbell": {
                "journey_stage": "ordeal",
                "hero_archetype": "reluctant_hero",
                "transformation_score": 0.64,
                "mythic_resonance": 0.78
            }
        },
        
        # Kindra 3×48
        "kindra": {
            "layer1": {
                "E01": 0.23, "E02": 0.45, "E03": 0.67, "E04": 0.34,
                "E05": 0.89, "E06": 0.12, "E07": 0.56, "E08": 0.78,
                "M01": 0.43, "M02": 0.65, "M03": 0.21, "M04": 0.87
            },
            "layer2": {
                "E01": 0.34, "E02": 0.56, "E03": 0.78, "E04": 0.23,
                "M01": 0.67, "M02": 0.45, "M03": 0.89, "M04": 0.12
            },
            "layer3": {
                "E01": 0.56, "E02": 0.34, "E03": 0.12, "E04": 0.89,
                "M01": 0.78, "M02": 0.23, "M03": 0.45, "M04": 0.67
            },
            "tw_plane_distribution": {
                "3": 0.33,
                "6": 0.34,
                "9": 0.33
            },
            "top_vectors": [
                {"layer": 1, "vector_id": "E05", "score": 0.89},
                {"layer": 2, "vector_id": "M03", "score": 0.89},
                {"layer": 1, "vector_id": "M04", "score": 0.87}
            ]
        },
        
        # Archetypes (Δ144)
        "archetypes": {
            "delta144_state": {
                "archetype": "Hero",
                "state": "Transformation",
                "score": 0.85
            },
            "polarities": {
                "order_chaos": 0.65,
                "tradition_novelty": 0.72,
                "individual_collective": 0.48
            }
        },
        
        # Drift & TW369
        "drift": {
            "tw_state": {
                "3": 0.35,
                "6": 0.40,
                "9": 0.25
            },
            "drift_magnitude": 0.15,
            "drift_direction": "progressive"
        },
        
        # Risk
        "risk": {
            "final_risk": 0.28,
            "risk_score": 0.30,
            "safeguard": {
                "toxicity": 0.12,
                "bias": 0.15
            }
        },
        
        # Summary
        "summary": {
            "confidence": 0.87,
            "routing": "full",
            "degraded": False
        }
    }


@router.get("/signal/minimal")
def get_mock_signal_minimal():
    """Return minimal mock signal (signal mode)."""
    return {
        "version": "3.1.0",
        "request_id": "mock-minimal-456",
        "timestamp": 1701234567.89,
        "mode": "signal",
        "degraded": False,
        "archetypes": {
            "delta144_state": {
                "archetype": "Sage",
                "state": "Reflection"
            }
        },
        "risk": {
            "final_risk": 0.15
        }
    }
