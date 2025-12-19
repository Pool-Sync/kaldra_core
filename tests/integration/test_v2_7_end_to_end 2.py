"""
End-to-End Integration Test for KALDRA v2.7.

Verifies the complete flow:
1. Text Input
2. Embedding Generation (Mocked)
3. Delta144 Inference (with Modifier Auto-Inference)
4. Meta-Analysis (Nietzsche/Aurelius) -> Polarity Extraction
5. Polarity Modulation (Delta12/TW369)
6. Story Engine Integration (Event Storage)
"""
import pytest
import numpy as np
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.kaldra_master_engine import KaldraMasterEngineV2
from src.archetypes.delta144_engine import Delta144Engine
from src.story.story_buffer import StoryBuffer
from src.story.story_aggregator import aggregate_story
from src.config import KALDRA_DELTA12_POLARITY_ENABLED

def test_v2_7_end_to_end_flow():
    """Test the full v2.7 pipeline."""
    
    # 1. Setup Engine with Mocks
    mock_embedding = np.random.rand(256)
    
    # Mock Delta144Engine
    mock_delta = MagicMock(spec=Delta144Engine)
    # Setup return value for infer_from_vector
    mock_result = MagicMock()
    mock_result.probs = np.ones(144) / 144.0
    mock_result.to_dict.return_value = {
        "state": {"id": "S03_WARRIOR_ACTIVE"},
        "active_modifiers": [{"id": "MOD_WOUNDED"}]
    }
    mock_delta.infer_from_vector.return_value = mock_result
    
    # Initialize Engine with mock
    engine = KaldraMasterEngineV2(
        delta_engine=mock_delta,
        d_ctx=256
    )
    
    # 2. Run Inference with Text
    text_input = "The warrior fights with honor but feels deep resentment towards the king."
    
    # We need to mock the meta-analysis functions if they are not available or slow
    # But since we imported them, let's assume they work or we can mock them too if needed.
    # For now, let's try running them. If they fail, we can mock.
    
    signal = engine.infer_from_embedding(
        embedding=mock_embedding,
        text=text_input
    )
    
    # 3. Verify Polarity Extraction
    assert signal.polarity_scores is not None
    # "resentment" keyword should trigger POL_RESENTMENT_AFFIRMATION
    # "warrior" might trigger POL_COURAGE_FEAR via Delta144 -> Nietzsche adjustment
    
    # 4. Verify Delta144 State
    assert signal.delta_state is not None
    assert "active_modifiers" in signal.delta_state
    
    # 5. Story Engine Integration
    story_buffer = StoryBuffer()
    
    # Add event with captured signal data
    story_buffer.add_event(
        text=text_input,
        delta144_state=signal.delta_state["state"]["id"],
        polarity_scores=signal.polarity_scores,
        metadata={"signal_id": "test_1"}
    )
    
    # Add a second event to test motion
    story_buffer.add_event(
        text="The warrior finds peace.",
        polarity_scores={"POL_RESENTMENT_AFFIRMATION": 0.9}, # High Affirmation
        metadata={"signal_id": "test_2"}
    )
    
    # 6. Verify Story Aggregation
    aggregation = aggregate_story(story_buffer)
    assert len(aggregation.motion_vectors) == 1
    motion = aggregation.motion_vectors[0]
    
    # Check if polarity delta was captured
    # First event had high resentment (low Affirmation?), second has high Affirmation.
    # Should see a delta.
    assert "POL_RESENTMENT_AFFIRMATION" in motion.polarity_deltas
