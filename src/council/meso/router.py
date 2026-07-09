import os
import sys
sys.path.append("/home/anonz/the-council")

import numpy as np

from council.meso.semantic_transformer import SemanticTransformer

class CouncilRouter:
    """The Council MoE Router (Model-based Routing) Refactored."""
    def __init__(self, threshold=0.4):
        self.transformer = SemanticTransformer()
        self.threshold = threshold

    def route_signal(self, input_text: str) -> list[str]:
        # Simulate a semantic vector from the 'input_text'
        # In real use, this is the encoded embedding of the user prompt.
        np.random.seed(42) 
        intent_vector = np.random.uniform(-1, 1, 8).tolist()

        scores = self.transformer.transform_intent(intent_vector)
        
        activated_nodes = []
        for node, score in scores.items():
            if score >= self.threshold:
                activated_nodes.append(node)

        # Semantic Fallback (Apex inclusion for stability)
        if not activated_nodes:
            return ["Apex"]
        if "Apex" not in activated_nodes:
            activated_nodes.append("Apex")
            
        return sorted(list(set(activated_nodes)))

if __name__ == "__main__":
    print("Starting Router Test...")
    router = CouncilRouter()
    result = router.route_signal("Test input string for semantic routing activation.")
    print(f"Routing Results: {result}")