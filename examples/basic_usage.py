import json
from src.archetypes import Delta144Engine

def main():
    # Initialize engine with default schemas
    engine = Delta144Engine.from_default_files()
    print(f"Engine initialized with {len(engine.archetypes)} archetypes, {len(engine.states)} states, and {len(engine.modifiers)} modifiers.")

    # Example inference
    result = engine.infer_state(
        archetype_id="A07_RULER",
        plane_scores={"3": 0.2, "6": 0.6, "9": 0.2},
        profile_scores={"EXPANSIVE": 0.1, "CONTRACTIVE": 0.7, "TRANSCENDENT": 0.2},
        modifier_scores={
            "MOD_DEFENSIVE": 0.8,
            "MOD_SHADOW": 0.4,
            "MOD_INSTITUTIONAL": 0.6,
        },
    )

    print("\nInference Result:")
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
