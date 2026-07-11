import math
from typing import List, Dict
import time

class SilasChaosDetector:
    """
    Archetype implementation based on COUNCIL_SPECIFICATION.md (Silas).
    Performs Entropy and Perplexity Gradient Monitoring to detect 
    distributional shifts ($\Delta S$) in semantic flows.
    """

    def __init__(self, entropy_threshold: float = 0.15):
        # Threshold for triggering a 'Recalibration Signal' (Lexus intervention)
        self.entropy_threshold = entropy_threshold
        self.history: List[Dict] = []
        self.drift_log: List[float] = []

    def calculate_shannon_entropy(self, probabilities: List[float]) -> float:
        """Calculates Shannon Entropy $H(P) = -\sum p_i \log2(p_i)$."""
        if not all(0 <= p <= 1 for p in probabilities):
            raise ValueError("Probabilities must be between 0 and 1.")
            
        # Filter out zero-probabilities to avoid log(0) errors.
        eps = 1e-9
        entropy = -sum(p * math.log2(max(p, eps)) for p in probabilities if p > 0)
        return entropy

    def monitor_step(self, token_probs: List[float], timestamp: float = None):
        """Analyzes a single step of semantic flow."""
        if not timestamp:
            timestamp = time.time()
            
        entropy = self.calculate_shannon_entropy(token_probs)
        
        # Track history for gradient monitoring ($\Delta H$)
        self.history.append({
            "ts": timestamp,
            "entropy": entropy
        })

        if len(self.history) > 1:
            prev_e = self.history[-2]["entropy"]
            delta = abs(entropy - prev_e)
            self.drift_log.append(delta)
            return {
                "status": "NORMAL",
                "current_entropy": entropy,
                "entropy_gradient": delta
            } if delta < self.entropy_threshold else {
                "status": "DRIFT_DETECTED",
                "current_entropy": entropy,
                "entropy_gradient": delta
            }
        return {"status": "INITIALIZING", "current_entropy": entropy}

    def get_report(self):
        """Returns the current stability summary."""
        if not self.drift_log:
            return "No drift data captured."
        avg_gradient = sum(self.drift_log) / len(self.drift_log)
        max_spike = max(self.drift_log) if self.drift_log else 0
        status = "STABLE" if avg_gradient < (self.entropy_threshold * 0.5) else "VOLATILE"
        return f"Status: {status} | Avg Gradient: {avg_gradient:.4f} | Max Spike: {max_spike:.4f}"

if __name__ == "__main__":
    # Smoke test for Silas Archetype Implementation
    detector = SilasChaosDetector(entropy_threshold=0.2)
    print("--- SILAS CHAOS DETECTOR SMOKE TEST ---")
    
    # 1. Stable Sequence (Low Entropy/Orderly)
    stable_probs = [0.9, 0.05, 0.03, 0.01, 0.01] 
    print(f"Step 1 (Stable): {detector.monitor_step(stable_probs)}")

    # 2. Transitioning Sequence
    transition_probs = [0.4, 0.3, 0.2, 0.05, 0.05]
    print(f"Step 2 (Transition): {detector.monitor_step(transition_probs)}")

    # 3. High Entropy Spike (Simulating Chaos/Drift)
    chaos_probs = [0.2, 0.2, 0.2, 0.15, 0.15, 0.1] # Uniform distribution increases entropy
    print(f"Step 3 (Chaos): {detector.monitor_step(chaos_probs)}")

    print("\nFinal Summary Report:")
    print(detector.get_report())
