import asyncio
import json
import os
import time
from typing import List, Dict, Any
from src.council.meso.drift_monitor import DriftMonitor

class SimulationStep:
    def __init__(self, agent_id: str, action: str, expected_intent_vec: List[float]):
        self.agent_id = agent_id
        self.action = action
        self.expected_intent_vec = expected_intent_vec

class SimulationEngine:
    def __init__(self, drift_monitor: DriftMonitor):
        self.drift_monitor = drift_monitor
        self.results = []
        self.start_time = 0.0

    async def run_simulation(self, steps: List[SimulationStep], output_path: str):
        self.start_time = time.time()
        print("🚀 Starting Simulation Engine...")
        
        for i, step in enumerate(steps):
            intent = step.expected_intent_vec
            # Simulate a response vector (with some noise/drift)
            # In a real scenario, this would come from an agent call
            response_vec = [val * 0.9 + (i * 0.01) for val in intent] 
            
            # Inject drift if it's step 2 to test detection
            if i == 2:
                response_vec = [v * 0.5 for v in response_vec]

            print(f"[Step {i}] Agent: {step.agent_id} | Action: {step.action}")
            
            # Perform monitoring
            metrics = self.drift_monitor.ingest_observation(intent, response_vec)
            metrics["step"] = i + 1
            metrics["agent_id"] = step.agent_id
            metrics["action"] = step.action
            
            self.results.append(metrics)
            print(f"  -> Drift: {metrics['drift']:.4f} | Status: {metrics['status']}")

        duration = time.time() - self.start_time
        report = {
            "metadata": {
                "timestamp": time.ctime(),
                "total_steps": len(steps),
                "total_duration_s": round(duration, 2)
            },
            "simulation_trace": self.results
        }

        # Ensure directory exists
        os.makedirs(os._path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"✅ Simulation complete. Report saved to {output_path}")

async def main():
    from unittest.mock import MagicMock
    # Using a dummy vector for intent [1.0, 0.0, 0.0]
    intent = [1.0, 0.0, 0.0]
    steps = [
        SimulationStep("Sage", "Retrieve Context", intent),
        SimulationStep("Weaver", "Decompose Graph", intent),
        SimulationStep("Lyria", "Generate Response", intent), # This will trigger drift in our simulation code above
    ]
    
    dm = DriftMonitor(threshold=0.2)
    engine = SimulationEngine(dm)
    await engine.run_simulation(steps, "benchmarks/simulation_report.json")

if __name__ == "__main__":
    asyncio.run(main())
