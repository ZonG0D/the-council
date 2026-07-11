import math
from typing import List, Dict, Any

class LexusArbiter:
    def __init__(self, constraint_strength: float = 0.8):
        self.constraint_strength = constraint_strength

    def evaluate_compliance(self, divergence: float) -> dict:
        is_violation = divergence > (1.0 - self.constraint_strength)
        return {
            "status": "COMPLIANT" if not is_violation else "VIOLATION",
            "severity": round(divergence, 4),
            "signal_issued": True if is_violation else False
        }

if __name__ == "__main__":
    lexis = LexusArbiter(constraint_strength=0.5)
    print("Compliance (Low Drift - 0.2):", lexis.evaluate_compliance(0.1))
    print("Violation  (High Drift - 0.8):", lexis.evaluate_compliance(0.9))
