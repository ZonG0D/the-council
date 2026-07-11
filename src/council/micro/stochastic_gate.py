from typing import List
import math

class StochasticGate:
    def __init__(self, strength: float = 1e6):
        self.strength = strength

    def apply_mask(self, logits: List[float], allowed_indices: List[int]) -> List[float]:
        return [v if i in allowed_indices else (v - self.strength) for i, v in enumerate(logits)]

    def calculate_divergence(self, original: List[float], masked: List[float]) -> float:
        return math.sqrt(sum((o - m)**2 for o, m in zip(original, masked)))

if __name__ == "__main__":
    gate = StochasticGate()
    test_logits = [0.1, 0.5, 0.8, 0.4]
    allowed = [0, 2]
    masked = gate.apply_mask(test_logits, allowed)
    drift = gate.calculate_divergence(test_logits, masked)
    print(f"Masked: {masked}")
    print(f"Drift: {drift:.4f}")

