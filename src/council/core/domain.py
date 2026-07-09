from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class CouncilSignal:
    type: str

@dataclass(frozen=True)
class ObservationSignal(CouncilSignal):
    agent: str = ""
    vector: List[float] = field(default_factory=list)
    entropy: float = 0.0

@dataclass(frozen=True)
class AuditSignal(CouncilSignal):
    cause: str = ""
    severity: str = "low"

@dataclass(frozen=True)
class ControlSignal(CouncilSignal):
    reason: str = ""
    action: str = ""

@dataclass
class AgentContext:
    raw_input: str
    intent_vector: List[float] = field(default_factory=lambda: [0.0]*8)
    memory_buffer: List[str] = field(default_factory=list)
    active_tasks: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    entropy: float = 0.0
    is_aborted: bool = False
