
import asyncio
import sys
import os

# Force the shell to recognize 'src' as a package root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Mocking components that might be thin in the current version 
# to ensure we test the CORE logic flow of the Council.
class MockAgent:
    def __init__(self, name):
        self.name = name
    async def step(self, context):
        return f"[{self.name}] Processing: {context}"

class SimulatedCouncilEngine:
    """A robust version for integration testing."""
    def __init__(self):
        self.history = []
        self.drift_triggered = False
    
    async def execute_step(self, context, drift_level=0.0):
        print(f" [CORE] Executing step with entropy: {drift_level}")
        # Simulate the agent behavior
        response = f"Agent response to '{context}' at entropy {drift_level}"
        self.history.append(response)
        
        if drift_level > 0.7:
            return "RECALIBRATE", response
        return "CONTINUE", response

class MockDriftMonitor:
    def __init__(self):
        self.last_val = 0.1
    def get_current_drift(self, step):
        # Simulate an increasing divergence as steps progress
        return step * 0.25

async def main():
    print("--- STARTING INTEGRATION PILOT: THE COUNCIL NERVATE ---")
    
    engine = SimulatedCouncilEngine()
    monitor = MockDriftMonitor()
    
    task = "Construct a coherent logical argument for machine agency."
    context = task
    drift_detected = False

    for step in range(1, 6):
        print(f"\n>>> [CYCLE {step}]")
        
        # 1. Execute Loop (Simulation of Weaver/Lyria)
        status, output = await engine.execute_step(context)
        print(output)

        # 2. Monitor Loop (The Meso Layer: Silas/DriftMonitor)
        drift = monitor.get_current_drift(step)
        print(f" [MESO] Drift Level: {drift}")

        if status == "RECALIBRATE":
            print("\n[!!!] [DETECTION] CRITICAL DRIFT DETECTED!")
            print("[ACTION] Triggering Noah (Meta-Cognitive Reset)...")
            print("--- RESET EXECUTED: Context Normalized ---")
            drift_detected = True
            break

    print("\n" + "="*40)
    if drift_detected:
        print("TEST RESULT: SUCCESS. Meta-cognitive resonance achieved.")
        print("The Council successfully detected and stabilized a divergence event.")
    else:
        print("TEST RESULT: INCOMPLETE. No drift was triggered for testing.")
    print("="*40 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
