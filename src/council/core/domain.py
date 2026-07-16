from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass(frozen=True)
class AgentContext:
    """The shared cognitive state for a cycle."""
    conversation_id: str
    metadata: Dict[str, Any] = None 
    history: List[Dict[str, Any]] = None

class BaseAgent(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    @abstractmethod
    async def process(self, context: AgentContext) -> str:
        pass

    async def _call_model(self, prompt: str) -> str:
        import asyncio
        await asyncio.sleep(0.1)
        return f"[{self.name}] (Model Output): {prompt[:20]}..."

# --- ARCHETYPES ---
class Elis(BaseAgent):
    async def process(self, context: AgentContext) -> str:
        return f"[Elis] Intent check passed for prompt segment."

class Lyria(BaseAgent):
    async def process(self, context: AgentContext) -> str:
        return f"[Lyria] Linguistic resonance achieved."

class Sage(BaseAgent):
    async def process(self, context: AgentContext) -> str:
        return f"[Sage] Context retrieved from semantic memory."

class Lexi(BaseAgent):
    async def process(self, context: AgentContext) -> str:
        return f"[Lexi] Compliance verified via policy constraints."

class Silas(BaseAgent):
    async def process(self, context: AgentContext) -> str:
        return f"[Silas] Entropy level within stable bounds."

class Weaver(BaseAgent):
    async def process(self, context: AgentContext) -> str:
        return f"[Weaver] Orchestrating task sub-components..."