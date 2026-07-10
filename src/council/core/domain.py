from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
import time
import hashlib

@dataclass(frozen=True)
class CouncilSignal:
    """Base signal class enforcing CP-1 Header requirements."""
    type: str
    origin_id: str      # Archetype name
    target_id: str      # Archetype name or 'SYSTEM'
    sequence_id: int
    timestamp: float = field(default_factory=time.time)
    reason: str = ""     # Standardized descriptive field for all signals

@dataclass(frozen=True)
class ObservationSignal(CouncilSignal):
    """Structured observation payload for Meso/Micro scale perception."""
    intent_vector: List[float] = field(default_factory=lambda: [0.0]*8)
    perceived_entropy: float = 0.0
    observation_vector: List[float] = field(default_factory=list)

@dataclass(frozen=True)
class AuditSignal(CouncilSignal):
    """High-priority signal for anomaly detection and error tracking."""
    severity: str = "low"  # low, medium, high, critical
    checksum: Optional[str] = None

@dataclass(frozen=True)
class ControlSignal(CouncilSignal):
    """Command signal to trigger architectural recalibration."""
    action: str = ""
    validation_token: str = ""

@dataclass(frozen=True)
class LoopState(CouncilSignal):
    """Real-time representation of the current orchestration scale."""
    loop_level: int = 1  # 1: Inner (Execution), 2: Middle (Stability), 3: Outer (Meta-Cognitive)
    drift_magnitude: float = 0.0
    convergence_score: float = 1.0

@dataclass(frozen=True)
@dataclass # Using dataclass for mutable state if needed later, though frozen is safer
class AgentContext:
    """The situational state of an active agent within the hierarchy."""
    raw_input: str
    intent_vector: List[float] = field(default_factory=lambda: [0.0]*8)
    memory_buffer: List[str] = field(default_factory=list)
    active_tasks: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    entropy: float = 0.0
    is_aborted: bool = False
