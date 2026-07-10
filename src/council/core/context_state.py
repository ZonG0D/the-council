import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import numpy as np

@dataclass
class ImmutableCore:
    """The fixed semantic foundation of the Council's identity."""
    system_directives: str = "Maintain structural integrity and operational persona."
    identity_anchors: List[str] = field(default_factory=lambda: ["Elis", "Sage", "Lyria", "Lexus", "Silas", "Weaver"])
    timestamp: float = field(default_factory=time.time)

@dataclass
class FluidContext:
    """The high-entropy, task-specific semantic workspace."""
    task_intent: str = ""
    interaction_history: List[Dict[str, Any]] = field(default_factory=list)
    semantic_vector: Optional[np.ndarray] = None

class CognitiveContext:
    """The complete state-space representing the Council's mental workspace."""
    def __init__(self, core: Optional[ImmutableCore] = None):
        self.core = core or ImmutableCore()
        self.fluid = FluidContext()
        self.entropy_levels = []

    def update_state(self, intent: str, vector: np.ndarray):
        """Updates the fluid context with new task-specific vectors."""
        if self.fluid.semantic_vector is None:
            self.fluid.semantic_vector = np.zeros_like(vector)
        
        self.fluid.task_intent = intent
        self    .fluid.semantic_vector = vector
        
        # Shannon Entropy calculation for observability
        if len(vector) > 0:
            prob_dist = np.abs(vector) / np.sum(np.abs(vector))
            entropy = -np.sum(prob_dist * np.log2(prob_dist + 1e-9))
        else:
            entropy = 0.0

        self.fluid.interaction_history.append({
            "ts": time.time(),
            "intent": intent,
            "entropy": float(entropy)
        })
        self.entropy_levels.append(float(entropy))

    def get_summary(self):
        return {
            "core_directives": self.core.system_directives,
            "current_task": self.fluid.task_intent,
            "semantic_center": (self.fluid.semantic_vector.tolist() if self.fluid.semantic_vector is not None else None),
            "history_depth": len(self.fluid.interaction_history)
        }
