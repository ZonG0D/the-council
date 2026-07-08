import math
import random
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class AgentContext:
    """The shared state passed between Council members during a reasoning cycle."""
    raw_input: str
    intent_vector: List[float] = field(default_factory=lambda: [0.0]*8)
    memory_buffer: List[str] = field(default_factory=list)
    active_tasks: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    entropy: float = 0.0
    is_aborted: bool = False

class CouncilMember:
    def __init__(self, name: str):
        self.name = name
    def step(self, context: AgentContext) -> None:
        raise NotImplementedError

# --- THE IMPLEMENTATION OF THE ARCHETYPES ---

class Elis(CouncilMember):
    """The Heart (Intent Alignment)"""
    def step(self, context: AgentContext) -> None:
        print(f"[{self.name}] $\to$ Mapping input to latent intent...")
        # Simulating semantic compression into a vector
        context.intent_vector = [random.uniform(-1, 1) for _ in range(8)]

class Lyria(CouncilMember):
    """The Voice (Sampling & Realization)"""
    def step(self, context: AgentContext) -> None:
        print("[Lyria] $\to$ Projecting latent state to vocabulary space...")
        # Simulates the probabilistic sampling of tokens
        pass

class Sage(CouncilMember):
    """The Memory (Knowledge Retrieval)"""
    def step(self, context: AgentContext) -> None:
        print("[Sage] $\to$ Retrieving associative context from vector store...")
        context.memory_buffer.append("Retrieved historical pattern #402")

class Lexus(CouncilMember):
    """The Law (Constraint/Safety)"""
    def step(self, context: AgentContext) -> None:
        print("[Lexus] $\to$ Validating semantic boundaries...")
        # Check for constraints in the input or intended output
        if "illegal" in context.raw_input.lower():
            context.constraints.append("Violation detected")
            context.is_aborted = True

class Silas(CouncilMember):
    """The Sentinel (Observability)"""
    def step(self, context: AgentContext) -> None:
        # Simulate entropy calculation based on intent variance
        entropy = abs(sum(context.intent_vector)) / 8.0
        context.entropy = entropy
        if entropy > 0.8:
            print("[Silas] $\to$ WARNING: High information entropy detected.")

class Weaver(CouncilMember):
    """The Assembly (Orchestration)"""
    def step(self, context: AgentContext) -> None:
        print("[Weaver] $\to$ Decomposing intent into task graph...")
        context.active_tasks = ["Parse Input", "Retrieve Context", "Synthesize Response"]

class Mnemosyne(CouncilMember):
    """The Archive (Memory/Continuity)"""
    def step(self, context: AgentContext) -> None:
        print("[Mnemosyne] $\to$ Ensuring contextual continuity...")
        context.memory_buffer.append("Continuity Check Passed")

class Pythia(CouncilMember):
    """The Oracle (Prediction/Logic)"""
    def step(self, context: AgentContext) -> None:
        print("[Pythia] $\to$ Predicting next logical state...")
        pass

class Argus(CouncilMember):
    """The Observer (Verification/Ontology)"""
    def step(self, context: AgentContext) -> None:
        print("[Argus] $\to$ Monitoring ontological consistency...")
        context.entropy = 0.1  # Stabilize entropy

class Hermes(CouncilMember):
    """The Messenger (Interface/Fluency)"""
    def step(self, context: AgentContext) -> None:
        print("[Hermes] $\to$ Mapping symbols to semantic space...")
        pass

class Eris(CouncilMember):
    """The Chaos (Stochasticity/Variance)"""
    def step(self, context: AgentContext) -> None:
        print("[Eris] $\to$ Injecting stochastic variance...")
        context.entropy += 0.1

class CouncilOrchestrator:
    """The master runtime loop that executes the Council logic."""
    def __init__(self):
        self.members = [
            Elis("Elis"),
            Sage("Sage"),
            Lyria("Lyria"),
            Lexus("Lexus"),
            Silas("Silas"),
            Weaver("Weaver"),
            Mnemosyne("Mnemosyne"),
            Pythia("Pythia"),
            Argus("Argus"),
            Hermes("Hermes"),
            Eris("Eris")
        ]

    def execute(self, user_input: str):
        print(f"\n--- INITIATING COUNCIL CYCLE for: '{user_input}' ---")
        context = AgentContext(raw_input=user_input)
        
        for member in self.members:
            if context.is_aborted:
                print("\n[!!] EXECUTION ABORTED BY LEXUS [!!]")
                break
            member.step(context)

        print("-" * 45)
        print("CYCLE COMPLETE")
        print(f"Final Intent Vector (Head): {context.intent_vector[:3]}...")
        print(f"Memory Buffer: {context.memory_buffer}")
        if context.is_aborted:
            print("STATUS: Aborted due to constraint violation.")
        else:
            print("STATUS: Successful Realization.")
