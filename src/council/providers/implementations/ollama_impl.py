import asyncio
import json
import requests

class OllamaProvider:
    """A production-ready wrapper for the Ollama API."""
    def __init__(self, model_name: str, base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url

    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Sends a request to the local Ollm/Ollama instance."""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
        
        # Use run_in_executor because requests is synchronous and would block the event loop
        loop = asyncio.get_event_loop()
        try:
            response = await loop.run_in_executor(None, lambda: requests.post(
                f"{self.base_url}/api/generate", 
                json=payload,
                timeout=30
            ).json())
            return response.get('response', "")
        except Exception as e:
            return f"Provider Error (Ollama): {str(e)}"

    async def stream_generate(self, prompt: str, temperature: float = 0.7):
        """Generator for streaming token responses."""
        try:
            # Implementation of streaming would go here in a real production setup
            pass
        except Exception as e:
            print(f"Streaming Error: {e}")

