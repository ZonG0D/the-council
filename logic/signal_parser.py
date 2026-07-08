import re
from typing import List
try:
    from logic.domain import CouncilSignal, ObservationSignal, AuditSignal, ControlSignal
except ImportError:
    from logic.domain import CouncilSignal, ObservationSignal, AuditSignal, ControlSignal

class SignalParser:
    def __init__(self):
        # Patterns allow for flexible extraction across different agent outputs
        self._patterns = {
            "OBS": [r"\\[agent:(?P<agent>\\\\w+)\\] vector=\\[(?P<vec>[^\\\\]]+)\\] entropy=(?P<ent>[\\\\d\\\\.]+)",
                    r"Observation from (?P<agent>\\\\w+): (?P<msg>[^.!?]*)"],
            "AUDIT": [r"\\[(?P<severity>high|medium|low)\\] Warning - (?P<cause>[^.!?]+)",
                      r"(?:Anomaly|Error|Warning) detected: (?P<cause>[^.!?]+)"],
            "CONTROL": [r"Action Required: (?P<action>\\\\w+) due to (?P<reason>[^.!\\n]+)",
                        r"(?P<action>RESET|HALT) Command: .*"]
        }

    def parse(self, text: str) -> List[CouncilSignal]:
        signals = []
        for line in text.strip().split('\\n'):
            line = line.strip()
            if not line: continue
            found = False
            # Try Control Signals (Highest priority/interrupts)
            for p in self._patterns["CONTROL"]:
                m = re.search(p, line, re.IGNORECASE)
                if m:
                    d = m.groupdict()
                    signals.append(ControlSignal(type="CTRL", action=d['action'].upper(), reason=d.get('reason', 'unknown')))
                    found = True; break
            if found: continue

            # Try Audit Signals
            for p in self._patterns["AUDIT"]:
                m = re.search(p, line, re.IGNORECASE)
                if m:
                    d = m.groupdict()
                    signals.append(AuditSignal(type="AUDIT", cause=d['cause'].strip(), severity=d.get('severity', 'low').lower()))
                    found = True; break
            if found: continue

            # Try Observation Signals
            for p in self._patterns["OBS"]:
                m = re.search(p, line, re.IGNORECASE)
                if m:
                    d = m.groupdict()
                    vec_list = []
                    if 'vec' in d and d['vec']:
                        try: vec_list = [float(x.strip()) for x in d['vec'].replace('[','').replace(']','').split(',')]
                        except ValueError: pass
                    signals.append(ObservationSignal(type="OBS", agent=d.get('agent', 'unknown'), vector=vec_list, entropy=float(d.get('ent', 0.0)) if 'ent' in d else 0.0))
        return signals
