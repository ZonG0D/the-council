import re
from typing import List, Optional, Union

# Note: In the actual system, these are imported from logic.orchestrator
# For standalone parsing/testing within this file script, we use local definitions
try:
    from logic.orchestrator import AuditSignal, ControlSignal, ObservationSignal
except ImportError:
    from dataclasses import dataclass
    @dataclass(frozen=True)
    class CouncilSignal: type: str
    @dataclass(frozen=True)
    class ObservationSignal(CouncilSignal): agent: str = ""; vector: list = None; entropy: float = 0.0
    @dataclass(frozen=True)
    class AuditSignal(CouncilSignal): cause: str = ""; severity: str = "low"
    @dataclass(frozen=True)
    class ControlSignal(CouncilSignal): reason: str = ""; action: str = ""

class SignalParser:
    """
    The bridge between unstructured language and CP-1 structured signals.
    Uses pattern matching to extract semantic 'intent' from agent text streams.
    """

    def __init__(self):
        # Patterns for the three main signal types
        self._patterns = {
            "OBS": [
                r"\[agent:(?P<agent>\w+)\] vector=\[(?P<vec>[^\]]+)\] entropy=(?P<ent>[\d\.]+)",
                r"Observation from (?P<agent>\w+): (?P<msg>[^.!?]*)",
            ],
            "AUDIT": [
                r"(?:Anomaly|Error|Warning|Spike|Violation|Failure) detected: (?P<cause>[^.!?]+)",
                r"\[(?P<severity>high|medium|low)\] Warning - (?P<cause>[^.!?]+)",
            ],
            "CONTROL": [
                r"(?:RESET|HALT|RECALIBRATE) Command: (?P<action>\w+) \(Reason: (?P<reason>[^)\)]+)\)",
                r"Action Required: (?P<action>\w+) due to (?P<reason>[^.!?]+)"
            ]
        }

    def parse(self, text: str) -> List[CouncilSignal]:
        signals = []
        lines = text.strip().split("\n")
        
        for line in lines:
            # 1. Try Control Signals first (Highest priority/interrupts)
            control_found = False
            for pattern in self._patterns["CONTROL"]:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    d = match.groupdict()
                    signals.append(ControlSignal(
                        type="CTRL",
                        action=d['action'].upper(),
                        reason=d['reason']
                    ))
                    control_found = True
                    break # One control signal per line max

            # 2. Try Audit Signals
            if not control_found:
                for pattern in self._patterns["AUDIT"]:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        d = match.groupdict()
                        signals.append(AuditSignal(
                            type="AUDIT",
                            cause=d['cause'].strip(),
                            severity=d.get('severity', 'low').lower()
                        ))
                        break

            # 3. Try Observation Signals
            if not control_found:
                for pattern in self._patterns["OBS"]:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        d = match.groupdict()
                        vec_list = []
                        if 'vec' in d and d['vec']:
                            try:
                                vec_list = [float(x.strip()) for x in d['vec'].split(',')]
                            except ValueError:
                                pass
                        
                        signals.append(ObservationSignal(
                            type="OBS",
                            agent=d['agent'],
                            vector=vec_list,
                            entropy=float(d.get('ent', 0.0)) if 'ent' in d else 0.0
                        ))
                        break
                    
        return signals

if __name__ == "__main__":
    parser = SignalParser()
    test_corpus = """
[agent:Lyria] vector=[0.8, 0.1, 0.5] entropy=0.2
Anomaly detected: High entropy instability in token generation!
Action Required: RESET due to Semantic Drift observed in last window.
[high] Warning - Loss of goal alignment in agent state.
Observation from Sage: The history has been synchronized with the current context.
    """
    print(f"Parsing corpus:\n{test_corpus}")
    results = parser.parse(test_corpus)
    for r in results:
        print(f"  > Found {r}")
