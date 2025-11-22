from src.archetypes import Delta144Engine

def test_delta144_engine_loads_default_schemas():
    engine = Delta144Engine.from_default_files()
    assert engine is not None
    assert len(engine.archetypes) == 12
    assert len(engine.states) == 144
    assert len(engine.modifiers) == 61
