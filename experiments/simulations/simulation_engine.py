import asyncio
import json
import os
import time
from typing import List, Dict, Any
import sys

# Dynamically fix the path for execution in this environment
sys.path.append(os.path.abspath("/home/anonz/projects/the-council"))
sys.path.append(os.path.abspath("/home/anonz/projects/the-council/the-council"))

try:
    from src.council.meso.drift_monitor import DriftMonitor
except ImportError:
    import sys
    sys.path.append(os.path.abspath("/home/anonz/projects/the-council/src"))
    from council.meso.drift_monitor import DriftMonitor

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
            response_vec = [val * 0.9 + (i * 0.01) for val in intent] 
            
            if i == 2:
                response_vec = [v * 0.5 for v in response_vec]

            print(f"[Step {i}] Agent: {step.agent_id} | Action: {step.action}")
            
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

        abs_output_path = os.path.abspath(output_path)
        os_dir = os.path.dirname(abs_output_path)
        if not os.path.exists(os_dir):
            os.makedirs(os_dir, exist_ok=True)

        with open(abs_output_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"✅ Simulation complete. Report saved to {abs_output_path}")

async def main():
    # Use absolute path for ensuring correct environment execution
    base_dir = os.path.abspath("/home/anonz/projects/the-council/the-council")
    report_file = os.path.join(base_dir, "benchmarks", "simulation_report.json")

    steps = [
        SimulationStep("Sage", "Retrieve Context", [1.0, 0.0, 0.0]),
        SimulationStep("Weaver", "Decompose Graph", [1.0, 0.0, 0.0]),
        SimulationStep("Lyria", "Generate Response", [1.0, 0.0, 0.0]), 
    ]
    
    dm = DriftMonitor(threshold=0.2)
    engine = SimulationEngine(dm)
    await engine.run_simulation(steps, report_file)

if __name__ == "__main__":
    asyncio.run(main())
