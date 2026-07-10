import pytest
import numpy as np
from typing import List
from council.core.domain import AgentContext
from semantic_transformer import SemanticTransformer

def test_semantic_transformer_routing():
    # Initialize transformer with default dim 8
    st = SemanticTransformer(embedding_dim=8)
    
    # Test vector: High similarity to 'Lyria' (based on prototypes in code)
    # Lyria prototype: [-0.8, 0.8, -0.1, 0.3, 0.5, -0.6, 0.1, 0.4]
    lyria_vec = np.array([-0.8, 0.8, -0.1, 0.3, 0.5, -0.6, 0.1, 0.4])
    scores = st.transform_intent(lyria_vec.tolist())
    
    # Check if Lyria has a high score (close to 1.0)
    assert scores['Lyria'] > 0.9

def test_semantic_transformer_zero_vector():
    st = SemanticTransformer(embedding_dim=8)
    zero_vec = [0.0] * 8
    scores = st.transform_intent(zero_vec)
    
    for score in scores.values():
        assert isinstance(score, float)

def test_semantic_transformer_normalization():
    st = SemanticTransformer(embedding_dim=8)
    # Large vector to check normalization/stability
    large_vec = [10.0] * 8
    scores = st.transform_intent(large_vec.tolist())
    
    for node, score in scores.items():
        # Scores should be within [-1, 1] because of cosine similarity logic inside transformer
        assert -1.0 <= score <= 1.0

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__]))
