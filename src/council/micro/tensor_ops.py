from typing import List, Union
import numpy as np

def normalize_vector(v: Union[List[float], np.ndarray]) -> np.ndarray:
    """Normalizes a vector to the unit hypersphere (L2 norm)."""
    arr = np.array(v, dtype=np.float64)
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr
    return arr / norm

def cosine_similarity(v1: Union[List[float], np.ndarray], v2: Union[List[float], np.ndarray]) -> float:
    """Calculates the cosine similarity between two vectors."""
    a = np.array(v1, dtype=np.float64)
    b = np.array(v2, dtype=np.float64)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))

def calculate_entropy(probs: Union[List[float], np.ndarray]) -> float:
    """Calculates Shannon Entropy (H)."""
    p = np.array(probs, dtype=np.float64)
    # Slice to avoid log(0) issues for zero probabilities
    p_pos = p[p > 0]
    return float(-np.sum(p_pos * np.log2(p_pos)))

def calculate_drift(v1: Union[List[float], np.ndarray], v2: Union[List[float], np.ndarray]) -> float:
    """Returns the cosine distance as a proxy for Semantic Drift."""
    return 1.0 - cosine_similarity(v1, v2)

def kl_divergence(p: Union[List[float], np.ndarray], q: Union[List[float], np.ndarray]) -> float:
    """Calculates Kullback-Leibler divergence between two distributions."""
    p = (np.array(p, dtype=np.float64) + 1e-10) # Epsilon smoothing
    q = (np.array(q, dtype=np.float64) + 1e-10)
    return float(np.sum(p * np.log(p / q)))

def manifold_distance(v1: Union[List[float], np.ndarray], v2: Union[List[float], np.ndarray]) -> float:
    """Calculates the Euclidean distance on the hypersphere embedding."""
    a = normalize_vector(v1)
    b = normalize_vector(v2)
    return float(np.linalg.norm(a - b))
