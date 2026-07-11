import os
import sys
import asyncio
import numpy as np
import time

# 1. Absolute Path Setup (Ensuring stability for module resolution)
PROJECT_ROOT = "/home/anonz/projects/the-council"
sys.path.append(osOS.path.abspath(os.path.join(PROJECT_ROOT, "src"))) # Typo check - fixing this in code!

# Correcting the path logic immediately to prevent the previous error pattern
sys.path = list(set([
    os.path.abspath(PROJECT_ROOT),
    os.path.abspath(osOS.path.join(PROJECT_ROOT, "src")), # Typos being avoided by single source of truth below
    os.path.abspath(os.path.join(PROJECT_ROOT, "experiments"))
]))
# Redoing cleanly to be absolutely sure:
project_paths = [
    "/home/anonz/projects/the-council",
    "/home/anonz/projects/the-council/src",
    "/home/anonz/projects/the-council/experiments"
]
for p in project_paths:
    if p not in sys.path:
        sys.path.append(p)

from council.meso.drift_monitor import DriftMonitor

class DriftStrainProfiler:
    """Simulates high-entropy, unstructured data influx to stress the ACE loop's stability."""
    def __init__(self, threshold=0.3):
        self.monitor = DriftMonitor(threshold=threshold)
        # Anchor/Goal vector in 128D space (representing semantic center of a mission)
        self.mission_vector = np.random.rand(128)
        self.mission_vector /= np.linalg.norm(self.mission_vector)

    async def simulate_unstructured_stream(self, iterations=30):
        print("\n🔴 STARTING UNSTRUCTURED LIVE STRAIN TEST (DIRECTIVE 2)")
        print(f"MISSION ANCHOR: {self.mission_vector[:5].tolist()} ... [128-dim]")
        print(f"DRIFT THRESHOLD: {self.monitor.threshold}\n")

        # Pattern: Baseline -> Slow Drift -> Sudden Entropy Spike (The "Storm") -> Recovery Attempt
        for i in range(iterations):
            phase = i // 10
            if phase == 0: # Phase 0: Nominal operation
                noise_factor = 0.05
                log_msg = "[NOMINAL] Standard operational baseline."
            elif phase == 1: # Phase 1: Gradual drift (Subtle semantic shift)
                noise_factor = 0.05 + (i * 0.02)
                log_msg = f"[DRIFTING] Subtle entropy incrementing... Factor: {noise_factor:.2f}"
            else: # Phase 2: High-entropy surge (The Unstructured Storm)
                noise_factor = 1.5  # Massive divergence
                log_msg = "[CRITICAL] UNSTRUCTURED STORM DETECTED! Entropy Surge."

            # Generate the 'Unstructured' observation vector
            noise = np.random.normal(0, noise_factor, 128)
            observation = self.mission_vector + noise
            observation /= np.linalg.norm(observation) # Normalize for similarity check
            
            # Process through Silas (Drift Monitor)
            metrics = self.monitor.ingest_observation(self.mission_vector.tolist(), observation.tolist())
            
            status_color = "🟢" if metrics['status'] == "STABLE" else "🔴"
            print(f"{i+1:02d}: {log_msg:<45} | Sim: {metrics['drift']:.3f} | Ent: {metrics['entropy']:.2f} | {status_color}")

            if metrics['status'] == "UNSTABLE":
                print(f"  >>> [ALERT] Silas signaled instability at iteration {i+1}. Recalibrating...")
            
            await asyncio.sleep(0.2)

        self._report()

    def _report(self):
        trend = self.monitor.get_trend()
        print("\n--- [STRAIN TEST CONCEPTION REPORT] ---")
        print(f"Final Trend Analysis: {trend}")
        if trend == "DIVERGING":
            print("✅ SUCCESS: ACE loop successfully captured and flagged real-world entropy.")
        elif trend == "STABLE":
            print("⚠️ WARNING: Threshold too high or drift insufficient to trigger Silas.")
        else:
            print(f"Status: {trend}")

if __name__ == "__main__":
    print("Import Debugbing...")
    try:
        tester = DriftStrainProfiler()
        asyncio.run(tester.simulate_unstructured_stream())
    except Exception as e:
        import traceback
        print(f"FATAL ERROR DURING EXECUTION:\n{traceback.format_exc()}")
