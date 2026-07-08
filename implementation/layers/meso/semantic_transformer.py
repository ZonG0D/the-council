import numpy as np
from typing import List, Dict

class SemanticTransformer:
    """Implements the mathematical bridge between Macro Intent and MoE Routing."""
    def __init__(self, embedding_dim: int = 8):
        # Prototype vectors for each of the 12 nodes (normalized)
        self.prototypes = {
            'Lexicon': np.array([0.1, 0.9, -0.2, 0.4, 0.8, -0.5, 0.1, 0.3]),
            'Rosetta': np.array([-0.5, 0.1, 0.7, -0.3, 0.1, 0.9, 0.2, -0.4]),
            'Euclid':  np.array([0.8, -0.1, 0.3, 0.6, -0.9, 0.2, 0.5, 0.1]),
            'Turing':  np.array([-0.2, 0.4, 0.8, 0.9, -0.1, 0.3, -0.7, 0.5]),
            'Alexandria': np.array([0.4, -0.4, 0.1, 0.6, 0.2, 0.7, 0.8, -0.3]),
            'Weaver':  np.array([0.1, 0.5, -0.5, 0.2, 0.9, -0.1, 0.4, 0.6]),
            'Ariadne': np.array([0.7, 0.2, -0.3, -0.8, 0.1, 0.3, 0.6, -0.5]),
            'Prism':   np.array([-0.1, -0.5, 0.9, -0.2, 0.4, 0.7, -0.8, 0.1]),
            'Kepler':  np.array([0.3, 0.6, 0.1, -0.4, 0.5, -0.1, 0.2, 0.9]),
            'Lyria':   np.array([-0.8, 0.8, -0.1, 0.3, 0.5, -0.6, 0.1, 0.4]),
            'Aegis':   np.array([0.2, -0.7, 0.9, -0.4, 0.1, 0.8, 0.3, -0.1]),
            'Apex':    np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        }

    def transform_intent(self, intent_vector: List[float]) -> Dict[str, float]:
        """Translates Macro-scale agentic action into Meso-scale routing logits."""
        v = np.array(intent_vector)
        scores = {}
        norm_v = np.linalg.norm(v) + 1e-9
        for node, proto in self.prototypes.items():
            # Cosine Similarity implementation of Meso scale semantic transformation
            score = np.dot(v, proto) / (norm_v * np.linalg.norm(proto) + 1e-09)
            scores[node] = float(score)
        return scores