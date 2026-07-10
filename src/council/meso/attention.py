import numpy as np
from typing import List, Dict, Any

class ArchetypeAttention:
    """
    Implements a Meso-Scale Attention mechanism where Agent Roles act as 'Keys' and 'Values',
    and the incoming semantic signal acts as the 'Query'.
    """
    def __init__(self, embedding_dim: int = 8):
        self.embedding_dim = embedding_dim
        # Archetype prototypes (the 'Key/Value' space)
        self.archetypes = {
            'Elis': np.array([0.1, -0.5, 0.3, 0.9, -0.1, 0.2, 0.4, -0.2]),
            'Lyria': np.array([-0.8, 0.8, -0.1, 0.3, 0.5, -0.6, 0.1, 0.4]),
            'Sage': np.array([0.2, 0.2, 0.9, -0.3, 0.1, 0.8, -0.5, 0.2]),
            'Lexus': np.array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]), # Strict constraint focus
            'Silas': np.array([-0.2, -0.2, -0.4, 0.5, -0.9, 0.8, 0.3, 0.1]),
            'Weaver': np.array([0.6, 0.4, -0.2, 0.2, 0.3, -0.1, 0.9, 0.5])
        }
    
    def compute_attention(self, query: float16_or_float_arr, context_vectors: Dict[str, np.ndarray]) -> Dict[str, float]:
        """Computes attention weights for the given query across all archetypes."""
        query = np.array(query).reshape(-1, 1) # (dim, 1)
        weights = {}
        
        # Scaled Dot-Product Attention approximation: Score(Q, K_i) = dot(Q, K_i) / sqrt(d)
        scores = []
        keys = []

        for name, key_vec in context_vectors.items():
            score = np.dot(query.T, key_vec.reshape(-1, 1))[0, 0]
            weights[name] = float(score)
            scores.append(score)
            keys.append(key_vec)

        if not scores:
            return {}

        # Softmax over the dot products to get weights
        exp_scores = np.exp(np.array(scores))
        softmax_weights = exp_scores / np.sum(exp_scores)
        
        # Map back to names
        name_keys = list(context_vectors.keys())
        return {name_keys[i]: float(softmax_weights[i]) for i in range(len(name_keys))}

    def weighted_aggregation(self, query: np.ndarray, attention_weights: Dict[str, float], context_vectors: Dict[str, np.ndarray]) -> np.ndarray:
        """Aggregates archetypes into a single 'Meso-Scale Response Vector'."""
        aggregated = np.zeros(self.embedding_dim)
        for name, weight in attention_weights.items():
            if name in context_vectors:
                aggregated += weight * context_vectors[name]
        return aggregated

def test_attention():
    attn = ArchetypeAttention()
    query = np.random.rand(8).tolist()
    # Use the internal archetypes as the context
    weights = attn.compute_attention(query, attn.archetypes)
    assert len(weights) == len(attn.archetypes)
    assert sum(weights.values()) == pytest.approx(1.0)

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
