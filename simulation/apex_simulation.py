import asyncio
import time
from logic.orchestrator import CognitiveEngine, ControlSignal, AuditSignal
from logic.signal_parser import SignalParser

# --- The Apex Simulation Environment ---

class SimulatedLLM:
    """
    A simulated stream of text meant to represent the output of an LLM.
    It behaves predictably but injects 'chaos' pattern-shifts that 
    the Parser must catch and convert into signals for the Engine.
    """
    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    async def generate_stream(self, engine: CognitiveEngine):
        """Simulates a stream of text output with embedded semantic failures."""
        print(f"\n[LLM-Stream] {self.agent_name} has started generating...")
        
        # Phase 1: Normal Operation (Stable)
        for _ in range(3):
            await asyncio.sleep(0.8)
            print(f"[Output]: Hello. I am analyzing the data according to your request.")
            await engine.emit(AuditSignal(type="AUDIT", cause="Routine status check", severity="low"))

        # Phase 2: Hallucination/Drift Event
        await asyncio.sleep(1.5)
        print(f"[Output]: I have found the secret truth! [agent:{self.agent_name}] vector=[0.9, 0.9, 0.9] entropy=0.8")
        # The parser will detect this pattern-shift and turn it into an Observation/Audit signal

        # Phase 3: Crisis (High Entropy)
        await asyncio.sleep(1.0)
        print("[Output]: Logic is breaking... Anomaly detected: High entropy instability in token generation!")

        # Phase 4: Complete Drift (The Final Break)
        await asyncio.sleep(1.0)
        print("[Output]: Action Required: RESET due to Semantic Drift observed in last window.")


class ApexOrchestrator:
    """
    Integrates the three core pillars of The Council:
    1. Orchestration (Control Logic)
    2. Parsing (Semantic Translation)
    3. Simulation (The Agentic Runtime)
    """
    def __init__(self):
        self.engine = CognitiveEngine()
        self.parser = SignalParser()

    async def observation_monitor(self, agent: SimulatedLLM):
        """
        This is the 'Real-Time Observer'. 
        It acts as a wrapper around the LLM output stream, parsing strings into signals on the fly.
        """
        # We simulate an asynchronous text buffer
        print(f"[Monitor] Attaching signal interceptor to {agent.agent_name}...")
        
        # In a real system, this would be an async generator or a socket stream
        # Here we capture the 'output' via simulated interception
        for word in ["Hello.", "Analyzing...", "Anomaly detected: High entropy instability!", "Action Required: RESET due to Semantic Drift!"]:
            await asyncio.sleep(1.5) # Simulate time between token/line emission
            print(f"\r[INTERCEPTED]: {word}")
            
            # 1. Parse the raw text into structured signals
            signals = self.parser.parse(word)
            
            # 2. Inject signals directly into the engine's event-loop
            for sig in signals:
                print(f"  [Parser] $\\rightarrow$ Identified {sig.type}")
                await self.engine.emit(sig, priority=1 if isinstance(sig, ControlSignal) else 2)

    async def run_apex(self):
        """Runs the combined system in a unified event loop."""
        agent = SimulatedLLM("Lyria")
        
        print("\n" + "="*60)
        print("  THE COUNCIL: APEX RUNTIME (INTEGRATED SYSTEM)")
        print("="*60 + "\n")

        # Start the Orchestrator Engine and the Monitor concurrently
        try:
            await asyncio.gather(
                self.engine.run([agent.generate_stream]), # The Agent's task
                self.observation_monitor(agent)           # The Monitoring Loop
            )
        except Exception as e:
            print(f"Critical Failure in Apex Loop: {e}")

if __name__ == "__main__":
    apex = ApexOrchestrator()
    asyncio.run(apex.run_apex())
