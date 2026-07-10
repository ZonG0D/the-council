import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import re
import os

class TopologyAwareRouter:
    """Implements Manifest-Aligned Meso-Scale Routing with Deterministic Anchoring and Adaptive Manifold Feedback.
    
    Ensures that semantic dispatching is grounded in stable archetypal subspaces while 
    dynamically adjusting to systemic entropy (volatility) to prevent agent drift 
    during complex orchestration transitions.
    """
    def __init__(self, manifest_path: str, archetype_embeddings: Optional[Dict[str, np.ndarray]] = None):
        """
        Initializes routing based on the formal Relational Topology and stable anchors.
        
        Args:
            manifest_path: Absolute path to the COUNCIL_MANIFEST.md.
            archetype_embeddings: A dictionary mapping node names to their fixed 
                                  mathematical center (e.g., learned or pre-computed).
        """
        self.manifest_path = os.path.abspath(manifest_path)
        self.topology = self._parse_manifest()
        
        if not self.topology:
            raise ValueError(f"Failed to extract archetypal topology from {self.manifest_path}.")

        # Dimension of the semantic manifold (ensuring parity with AgentContext/attention.py)
        self.embedding_dim = 8 

        # ARCHITECTURAL INJECTION: Deterministic Anchoring vs Random Noise
        if archetype_embeddings:
            # Use provided high-fidelity mathematical anchors
            self._initialize_anchors(archetype_embeddings)
        else:
            # Fallback to deterministic seeded initialization (prevents session-tosession drift)
            self._initialize_deterministic_anchors()

        self.node_to_archetype = {entry['node']: entry['archetype'] for entry in self.topology}

    def _initialize_anchors(self, embeddings: Dict[str, np.ndarray]):
        """Anchors the router to provided high-fidelity manifold coordinates."""
        self.node_centroids = {}
        for node, arch in self.node_to_archetype.items():
            if arch in embeddings and embeddings[arch].shape[0] == self.embedding_dim:
                # Assign actual semantic centroid from the embedding space
                self.node_centroids[node] = np.array(embeddings[arch], copy=True)
            else:
                # Fallback to deterministic but fixed-for-session value if arch not found
                self.node_centroids[node] = self._get_deterministic_fallback(node)

    def _initialize_deterministic_anchors(self):
        """Ensures session-to-session stability via a stable seed."""
        # Using a fixed seed ensures that even in the absence of learned embeddings, 
          # our "topology" remains isomorphic across restarts.
        rng = np.random.default_rng(seed=42) 
        self.node_centroids = {
            node: rng.standard_normal(self.embedding_dim) for node in self.node_to_archetype.keys()
        }

    def _get_deterministic_fallback(self, node_id: str) -> np.ndarray:
        """Generates a coordinate based on the hash of the node name to ensure stability."""
        # Use salt/seed-based generation for naming consistency without full neural weights
        import hashlib
        h = hashlib.md5(node_id.encode()).hexdigest()
        noise = np.array([int(h[i:i+2], 16) / 255.0 for i in range(0, 16, 2)])[:self.embedding_dim]
        # Pad if necessary (unlikely with the step above)
        if len(noise) < self.embedding_dim:
            noise = np.pad(noise, (0, self.embedding_dim - len(noise)), constant_values=0.5)
        return noise

    def _parse_manifest(self) -> List[Dict[str, str]]:
        mapping = []
        try:
            with open(self.manifest_path, 'r') as f:
                for line in f:
                    # Robustly handle Markdown table patterns for Archetype and Node columns
                    match = re.search(r"\|\s+\*\*([^|]+)\*\*\s*\|[^|]*\|[^|]*\s*\*\*([^|]+)\*\*\s*\|", line)
                    if match:
                        archetype = match.group(1).strip()
                        node = match.group(2).strip()
                        mapping.append({'archetype': archetype, 'node': node})
        except Exception as e:
            print(f"Error reading manifest: {e}")
        return mapping

    def route(self, semantic_vector: np.ndarray, entropy_factor: float = 1.0) -> List[Dict[str, Any]]:
        """
        Hierarchical routing logic with Adaptive Thresholding (AMF).
        
        Args:
            semantic_vector: The incoming signal in the embedding space.
            entropy_factor: Dynamic multiplier derived from systemic volatility (H).
                            Higher entropy = higher threshold for activation to prevent 
                            misaligned assignments during macro-scale transitions.
        """
        routed_assignments = []
        v_norm = np.linalg.norm(semantic_vector)
        if v_norm == 0: return []

        # --- ARCHITECTURAL INJECTION: Adaptive Manifold Feedback (AMF) ---
        # We implement a non-linear threshold modulation: T_active = 0.4 * (1 + max(0, H - 1))
        # This ensures that when systemic entropy is high (e.g., during a 'Recalibration' event), 
        # the requirements for agent activation are tightened to prevent semantic noise spread.
        base_threshold = 0.4
        dynamic_adjustment = max(0, entropy_factor - 1.0)
        activation_threshold = base_threshold * (1.0 + dynamic_adjustment)

        for node, centroid in self.node_centroids.items():
            c_norm = np.linalg.norm(centroid)
            # Cosine Similarity on normalized vectors
            sim = float(np.dot(semantic_vector, centroid) / (v_norm * c_norm))

            if sim > activation_threshold:
                archetype = self.node_to_archetype.get(node, "Unknown")
                routed_assignments.append({
                    "agent": archetype,
                    "node": node,
                    "confidence": round(sim, 3)
                })

        return sorted(routed_assignments, key=lambda x: x['confidence'], reverse=True)[:5]

    def verify_alignment(self, semantic_vector: np.ndarray) -> bool:
        """Verifies if a signal is within the manifold of known Council archetypes."""
        return len(self.route(semantic_vector)) > 0
