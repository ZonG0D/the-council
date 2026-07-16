"""
Drift Monitor: Part of the Meso Scale.
Continuously monitors semantic drift to signal stability transitions.
"""
from .semantic_evaluator import SemanticEvaluator

class DriftMonitor:
    def __init__(self, evaluator: SemanticEvaluator):
        self.evaluator = evaluator
        self.history = []

    def check(self, intent: str, output: str) -> float:
        score = self.evaluator.calculate_drift(intent, output)
        self.history.append(score)
        return score
