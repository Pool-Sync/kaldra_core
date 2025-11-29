"""
OpenAI LLM Client.

Implementation of LLMClientBase for OpenAI API using requests.
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from .llm_client_base import LLMClientBase

class OpenAILLMClient(LLMClientBase):
    """
    Client for OpenAI API.
    """

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview", timeout: int = 10):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def generate(self, prompt: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a response from OpenAI.
        
        Constructs a system message from the instruction and a user message
        from the context and text. Expects JSON output.
        """
        instruction = prompt.get("instruction", "Score the following text.")
        context = prompt.get("context", {})
        text = prompt.get("text", "")
        vectors = prompt.get("vectors", [])

        # Construct the messages
        system_content = f"{instruction}\n\nOutput strictly valid JSON with the format: {{'scores': {{'VECTOR_ID': score, ...}}}}"
        
        user_content = f"""
Context: {json.dumps(context, indent=2)}

Vectors to Score: {', '.join(vectors)}

Text:
{text}
"""

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.0,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=payload, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            # Parse JSON content
            return json.loads(content)

        except Exception as e:
            # Log error (in a real app, use a logger)
            print(f"OpenAI API Error: {e}")
            # Return empty scores on failure, allowing the scorer to fallback or return zeros
            return {"scores": {}}
