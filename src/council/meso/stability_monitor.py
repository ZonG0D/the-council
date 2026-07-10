import asyncio
import os
import sys
from typing import Optional

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

class StabilityMonitor:
    """
    Stability Monitoring: Ensures structural and semantic integrity of the feedback loop.
    Implements CP-1 logic for high-fidelity oversight.
    """
    def __init__(self):
        pass

    async def monitor_and_audit(self, signal: CouncilSignal) -> Optional[ControlSignal]:
        # 1. Audit Signal Analysis (High Severity Control)
        if isinstance(signal, AuditSignal):
            if signal.severity in ["high", "critical"]:
                return ControlSignal(
     type="STABILIZE",
     origin_id=signal.origin_id,
     target_id="Orchestrator",
     sequence_id=500,
     action="HALT",
     reason=f"Critical Audit: {signal.reason}"
 )

        # 2. Entropy Spike Detection (Micro-scale Observation Monitoring)
        if isinstance(signal, ObservationSignal):
            # Monitor for rapid 'Entropy Flux' spikes as defined in CP-1
            if signal.perceived_entropy > 0.85:
                return ControlSignal(
                    type="STABILIZE",
                    origin_id=signal.origin_id,
                    target_id="Orchestrator",
                    sequence_id=501,
                    action="RECALIBRATE",
                    reason=f"Unstable Entropy Spike (H={signal.perceived_entropy})"
                )

        return None
