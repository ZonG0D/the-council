import numpy as np
from typing import List, Dict, Any
import time

try:
    from council.micro.tensor_ops import calculate_entropy, calculate_similarity
except ImportError:
    # Fallback for development if micro-scale is not in path
    def calculate_entropy(p): 
        p = np.array(p)
        return -np.sum(p * np.log2(p + 1e-15))
    def calculate_similarity(v1, v2): 
        v1, v2 = np.array(v1), np.array(v2)
        norm = np.linalg.norm(v1) * np.linalg.norm(v2)
        return float(np.dot(v1, v2) / norm) if norm > 0 else 0.0

class DriftMonitor:
    """
    The Sentinel of Semantic Stability.
    Calculates Information Entropy and Cosine Similarity to detect 'Conceptual Drift'
    between the User Intent (Goal) and the Agentic Manifestation (State).
    Now utilizes high-precision Micro-scale primitives via CP-1 protocols.
    """
    def __init__(self, threshold: float = 0.2):
        self.threshold = threshold
        self.history = []

    def ingest_observation(self, intent_vec: List[float], response_vec: List[float]) -> Dict[str, Any]:
        """Processes a single step in the loop and returns drift metrics."""
        v_i = np.array(intent_vec)
        v_r = np.array(response_vec)

        if v_i.shape != v_r.shape:
            raise ValueError("Vector dimensionality mismatch in DriftMonitor")

        # Precision mapping to Micro-scale tensor ops
        similarity = calculate_similarity(v_i, v_r)
        entropy = calculate_entropy(v_r)
        
        drift = 1.0 - max(0.0, min(1.0, similarity))
        is_unstable = drift > self.threshold or entropy > 2.5

        entry = {
            "timestamp": time.time(),
            "similarity": float(similarity),
            "entropy": float(entropy),
            "drift": float(drift),
            "status": "UNSTABLE" if is_unstable else "STABLE",
            "metadata": {"precision_mode": "tensor_ops"}
        }
        self.history.append(entry)
        return entry

    def get_trend(self) -> str:
        """Analyzes the history to detect rapid divergence."""
        if len(self.history) < 3:
            return "INSUFFICIENT_DATA"
        
        recent = self.history[-3:]
        drift_gradient = recent[-1]['drift'] - recent[0]['drift']
        
        if drift_gradient > 0.1:
            return "DIVERGING"
        elif drift_gradient < -0.1:
            return "CONVERGING"
        else:
            return "STABLE"

if __name__ == "__main__":
    # Quick test to ensure the fix is syntax-correct and importable
    dm = DriftMonitor(threshold=0.2)
    v1 = [1.0, 0.0, 0.0]
    v2 = [0.95, 0.04, 0.01]
    print("In-code Test (Precise):", dm.ingest_observation(v1, v2))
