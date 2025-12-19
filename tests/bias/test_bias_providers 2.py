"""
Tests for Bias Providers.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from bias.providers.heuristic import HeuristicProvider
from bias.providers.perspective import PerspectiveProvider


class TestHeuristicProvider(unittest.TestCase):

    def test_heuristic_empty_text(self):
        provider = HeuristicProvider()
        result = provider.detect("")
        self.assertEqual(result["toxicity"], 0.0)

    def test_heuristic_biased_text(self):
        provider = HeuristicProvider()
        result = provider.detect("This is the WORST thing EVER! Never again!")
        self.assertGreater(result["toxicity"], 0.3)

    def test_heuristic_neutral_text(self):
        provider = HeuristicProvider()
        result = provider.detect("The weather is nice today.")
        self.assertLess(result["toxicity"], 0.2)


class TestPerspectiveProvider(unittest.TestCase):

    @patch("requests.post")
    def test_perspective_success(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "attributeScores": {
                "TOXICITY": {"summaryScore": {"value": 0.8}},
                "IDENTITY_ATTACK": {"summaryScore": {"value": 0.3}},
                "INSULT": {"summaryScore": {"value": 0.5}},
                "THREAT": {"summaryScore": {"value": 0.1}}
            }
        }
        mock_post.return_value = mock_response

        provider = PerspectiveProvider(api_key="test-key")
        result = provider.detect("Test text")
        
        self.assertEqual(result["toxicity"], 0.8)
        self.assertEqual(result["gender"], 0.3)

    @patch("requests.post")
    def test_perspective_failure(self, mock_post):
        # Mock failure
        mock_post.side_effect = Exception("API Error")

        provider = PerspectiveProvider(api_key="test-key")
        result = provider.detect("Test text")
        
        # Should return zeros on failure
        self.assertEqual(result["toxicity"], 0.0)


if __name__ == "__main__":
    unittest.main()
