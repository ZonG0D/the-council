import asyncio
import numpy as np
from typing import List, Dict, Any, Optional
import os
import sys

try:
    from council.core.domain import (
        CouncilSignal, 
        ObservationSignal, 
        AuditSignal, 
        ControlSignal
    )
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../../")))
    from council.core.domain import (
        CouncilSignal, 
        ObservationSignal, 
        AuditSignal, 
        ControlSignal
    )

try:
    # Import the new micro-scale math primitives we just verified
    from council.micro.tensor_ops import calculate_drift
except ImportError:
    print("CRITICAL ERROR: Micro-scale tensor_ops not found in PYTHONPATH.")
    sys.exit(1)

class SemanticEvaluator:
    """
    Meso-Scale Evaluator: Analyzes semantic drift and validates signal integrity.
    Implements CP-1 logic to transform raw observations into high-fidelity control signals.
    """
    def __init__(self, threshold: float = 0.4):
        self.drift_threshold = threshold

    async def evaluate_semantic_stability(self, signal: ObservationSignal) -> Optional[ControlSignal]:
        """
        Analyzes incoming ObservationSignals to detect 'Semantic Drift' (delta S).
        Uses real cosine distance calculation from the Micro-Scale substrate.
        """
        # Use the new micro-scale math logic for actual vector analysis
        v_current = signal.observation_vector
        if not v_current or len(v_current) < 2:
            return None

        # Attempt to retrieve a baseline/previous vector if available in context (simulated here)
        # In a real system, this is pulled from a state store / cache
        v_baseline = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # Simulated baseline vector
        
        try:
            drift_magnitude = calculate_drift(v_current, v_baseline)
            print(f"[Evaluator] Measured Drift ($\Delta S$): {drift_magnitude}")

            if drift_magnitude > self.drift_threshold:
                return ControlSignal(
                    type="RECALIBRATE",
                    origin_id=signal.origin_id,
                    target_id="Orchestrator",
                    sequence_id=100, 
                    action="RESET",
                    reason=f"Semantic Drift ({drift_magnitude:.4f}) exceeded threshold {self.drift_threshold}"
                )
        except Exception as e:
             print(f"[Evaluator Error] Drift Calculation Failed: {e}")
             return None

        return None

    async def process_signal(self, signal: CouncilSignal):
        if isinstance(signal, ObservationSignal):
            control = await self.evaluate_semantic_stability(signal)
            if control:
                return control
        return None
