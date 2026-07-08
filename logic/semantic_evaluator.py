import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

try:
    from logic.orchestrator import CognitiveEngine, ControlSignal
except ImportError:
    # Fallback for local stand-alone testing
    @dataclass(frozen=True)
    class ControlSignal:
        action: str = ""
        reason: str = ""
    class CognitiveEngine:
        def __init__(self): self.is_running = True
        async def emit(self, s, priority=1): print(f"[Mock] Signal: {s}")

@dataclass
class SemanticState:
    """A quantified representation of the current state vs target intent."""
    description: str
    confidence: float  # 0.0 to 1.0
    drift_score: float # 0.0 (aligned) to 1.0 (hallucinating/deviant)

class SemanticEvaluator:
    """
    The 'Intelligence' layer of the Council.
    Detects semantic drift by comparing observed logs and outcomes against Mission Goals.
    It identifies when an agent is technically working (no exit errors) but is 
    conceptually deviating from its original intent.
    """
    def __init__(self, engine: CognitiveEngine):
        self.engine = engine

    async def evaluate_drift(self, goal_description: str, observation_logs: List[str]) -> Optional[ControlSignal]:
        """
        Analyzes if the logs indicate semantic deviation from the intended goal.
        In a production system, this would call an LLM or a high-dimensional 
        embeddings model to calculate the distance between 'Intent' and 'Observation'.
        """
        print(f"[Evaluator] Analyzing {len(observation_logs)} log entries against intent: '{goal_description}'")
        
        # Heuristic Simulation of heavy semantic reasoning
        await asyncio.sleep(1) 

        drift_detected = False
        reason = ""

        # 1. Pattern-based drift detection (The "Low Level" intelligence)
        for log in observation_logs:
            if "unknown command" in log.lower() or "unexpected" in log.lower():
                print(f"[Evaluator] Found lexical anomaly in logs.")
                drift_detected = True
                reason = f"Lexical drift detected in output: {log}"
                break

        # 2. Scenario-based check (The "High Level" intelligence)
        # We simulate a 'hallucination' where the agent starts repeating 
        # irrelevant content that doesn'0t contribute to the goal.
        if not drift_detected and len(observation_logs) > 3:
            # Check for repetitive/idiosyncratic divergence
            if all(log == observation_logs[0] for log in observation_logs[-3:]):
                drift_detected = True
                reason = "Semantic Loop: Agent is repeating state without goal progression."

        if drift_detected:
            print(f"[Evaluator] 🚨 DRIFT DETECTED: {reason}")
            return ControlSignal(action="RESET", reason=reason)
        
        return None

async def run_drift_test():
    """
    Integration Test: Drifting Agent.
    Simulates an agent that is technically 'running' (no shell error) 
    but is actually spiraling into a semantic loop (Hallucination).
    """
    from logic.orchestrator import CognitiveEngine, ControlSignal
    engine = CognitiveEngine()
    ev = SemanticEvaluator(engine)

    print("=== STARTING SEMANTIC DRIFT TEST ===")
    
    # The agent is performing a 'task' that looks fine to the shell 
    # but is clearly looping/hallucinating semantically.
    observations = [
        "Agent: I am reading data...",
        "Agent: I am reading data...",
        "Agent: I am reading data...",
        "Agent: I am reading data..."
    ]

    print(f"[System] Agent is performing ostensibly valid but repetitive actions.")
    
    # The Evaluator detects the semantic loop
    signal = await ev.evaluate_drift("Process user request to digest log files", observations)

    if signal and signal.action == "RESET":
        print("\n[RESULT] SUCCESS: Semantic loop detected and Reset Signal triggered.")
        return True
    else:
        print("\n[RESULT] FAILED: Agent went into loop but no drift was detected.")
        return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(run_drift_test())
    sys.exit(0 if success else 1)
