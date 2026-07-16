import asyncio
import random

class LocalMockProvider:
    """A mockup of an LLM provider to test the framework without requiring a running server."""
    def __init__(self, model_name: str):
        self.model_name = model_name

    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        await asyncio.sleep(0.5)
        return f"Simulated response from {self.model_name} to query: '{prompt[:30]}...'"

    async def stream_generate(self, prompt: str, temperature: float = 0.7):
        tokens = ["This ", "is a ", "streamed ", "response ", "from ", "a ", "local ", "model."]
        for token in tokens:
            yield token
            await asyncio.sleep(0.1)