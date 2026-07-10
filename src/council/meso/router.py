import os
from typing import Dict, List, Any, Tuple, Optional, Callable, Awaitable
import numpy as np
import re
import hashlib
import asyncio

class TopologyAwareRouter:
    """Implements Manifest-Aligned Meso-Scale Routing with Deterministic Anchoring and Adaptive Manifold Feedback.
    
    Ensures that semantic dispatching is grounded in stable archetypal subspaces while 
    dynamically adjusting to systemic entropy (volatility) to prevent agent drift.
    """
    def __init__(self, manifest_path: str, archetype_embeddings: Optional[Dict[str, np.ndarray]] = None, alpha: float = 0.1, damping: float = 0.9):
        self.manifest_path = os.path.abspath(manifest_path)
        
        # 1. Define mapping FIRST to prevent initialization order errors
        self.topology = self._parse_manifest()
        if not self.topology:
            raise ValueError(f"Failed to extract archetypal topology from {self.manifest_path}.")
        
        self.node_to_archetype = {entry['node']: entry['archetype'] for entry in self.topology}
        self.embedding_dim = 8 
        
        # 2. Initialize Centroids based on mapping
        if archetype_embeddings:
             self._initialize_anchors(archetype_embeddings)
        else:
            self._initialize_deterministic_anchors()
        
        # ACE Parameters
        self.alpha = alpha
        self.damping = damping
        
        # --- [ACE FEEDBACK INTERFACE] ---
        self._observers: List[Callable[[Any], Awaitable[None]]] = []

    def register_observer(self, callback: Callable[[Any], Awaitable[None]]):
        if not asyncio.iscoroutinefunction(callback):
            raise ValueError("Observer must be a coroutine function.")
        self._observers.append(callback)

    async def _notify_observers(self, signal: Any):
        for callback in self._observers:
            try:
                await callback(signal)
            except Exception as e:
                print(f"Observer Notification Error: {e}")

    def _initialize_anchors(self, embeddings: Dict[str, np.ndarray]):
        self.node_centroids = {}
        for node, arch in self.node_to_archetype.items():
            if arch in embeddings and len(embeddings[arch]) == self.embedding_dim:
                self.node_centroids[node] = np.array(embeddings[arch], copy=True)
            else:
                self.node_centroids[node] = self._get_deterministic_fallback(node, hashlib)

    def _initialize_deterministic_anchors(self):
        rng = np.random.default_rng(seed=42) 
        self.node_centroids = {
            node: rng.standard_normal(self.embedding_dim) for node in self.node_to_archetype.keys()
        }

    def _get_deterministic_fallback(self, node_id: str, hashlib) -> np.ndarray:
        h = hashlib.md5(node_id.encode()).hexdigest()
        noise = np.array([int(h[i:i+2], 16) / 255.0 for i in range(0, 16, 2)])[:self.embedding_dim]
        if len(noise) < self.embedding_dim:
            import numpy as np
            noise = np.pad(noise, (0, self.embedding_dim - len(noise)), constant_values=0.5)
        return noise

    def _parse_manifest(self) -> List[Dict[str, str]]:
        mapping = []
        try:
            with open(self.manifest_path, 'r') as f:
                for line in f:
                    match = re.search(r"\|\s+\*\*([^|]+)\*\*\s*\|[^|]*\|[^|]*\*\*([^|]+)\*\*\s*\|", line)
                    if match:
                        archetype = match.group(1).strip()
                        node = match.group(2).strip()
                        mapping.append({'archetype': archetype, 'node': node})
        except Exception as e:
            print(f"Error reading manifest: {e}")
        return mapping

    def route(self, semantic_vector: np.ndarray, entropy_factor: float = 1.0) -> List[Dict[str, Any]]:
        routed_assignments = []
        v_norm = np.linalg.norm(semantic_vector)
        if v_norm == 0: return []

        base_threshold = 0.4
        dynamic_adjustment = max(0, entropy_factor - 1.0)
        activation_threshold = base_threshold * (1.0 + dynamic_adjustment)

        for node, centroid in self.node_centroids.items():
            c_norm = np.linalg.norm(centroid)
            sim = float(np.dot(semantic_vector, centroid) / (v_norm * c_norm))

            if sim > activation_threshold:
                archetype = self.node_to_archetype.get(node, "Unknown")
                routed_assignments.append({
                    "agent": archetype,
                    "node": node,
                    "confidence": round(sim, 3)
                })

        return sorted(routed_assignments, key=lambda x: x['confidence'], reverse=True)[:5]

    async def update_manifold(self, node: str, signal_vector: np.ndarray, confidence: float):
        import numpy as np
        if node not in self.node_centroids: return
        current_centroid = self.node_centroids[node]
        v_norm = np.linalg.norm(signal_vector)
        normalized_signal = signal_vector / v_norm if v_norm > 1e-9 else signal_vector
        movement = normalized_signal - current_centroid
        self.node_centroids[node] = current_centroid + (self.alpha * movement * self.damping * confidence)

    def verify_alignment(self, semantic_vector: np.ndarray) -> bool:
        return len(self.route(semantic_vector)) > 0
