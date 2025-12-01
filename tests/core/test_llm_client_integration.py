"""
Tests for LLM Client Integration.
"""

import unittest
from unittest.mock import MagicMock, patch
from src.kindras.scoring.llm_openai_client import OpenAILLMClient
from src.kindras.scoring.llm_dummy_client import DummyLLMClient

class TestLLMClientIntegration(unittest.TestCase):

    def test_dummy_client(self):
        client = DummyLLMClient()
        prompt = {"vectors": ["V1", "V2"]}
        response = client.generate(prompt)
        self.assertEqual(response["scores"]["V1"], 0.0)
        self.assertEqual(response["scores"]["V2"], 0.0)

    @patch("requests.post")
    def test_openai_client_success(self, mock_post):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"scores": {"V1": 0.8, "V2": -0.5}}'
                }
            }]
        }
        mock_post.return_value = mock_response

        client = OpenAILLMClient(api_key="test-key")
        prompt = {
            "instruction": "Score",
            "context": {"country": "BR"},
            "text": "Test text",
            "vectors": ["V1", "V2"]
        }
        
        response = client.generate(prompt)
        self.assertEqual(response["scores"]["V1"], 0.8)
        self.assertEqual(response["scores"]["V2"], -0.5)

    @patch("requests.post")
    def test_openai_client_failure(self, mock_post):
        # Mock failure
        mock_post.side_effect = Exception("API Error")

        client = OpenAILLMClient(api_key="test-key")
        prompt = {"vectors": ["V1"]}
        
        response = client.generate(prompt)
        self.assertEqual(response, {"scores": {}})

if __name__ == "__main__":
    unittest.main()
