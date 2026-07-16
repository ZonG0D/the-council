from abc import ABC, abstractmethod

class BaseProvider(ABC):
    """Base interface for all Council model providers."""
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        pass

    @abstractmethod
    async def stream_generate(self, prompt: str, temperature: float = 0.7):
        pass