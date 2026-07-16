from typing import List, Dict, Any, Optional
import re
import time
import numpy as np

try:
    from council.core.domain import CouncilSignal, ObservationSignal, AuditSignal, ControlSignal
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "projects/the-council/src")))
    from council.core.domain import CouncilSignal, ObservationSignal, AuditSignal, ControlSignal

class TopologyAwareParser:
    def __init__(self, manifest_path: str = None):
        self._valid_archetypes = {"Elis", "Sage", "Lyria", "Lexus", "Silas", "Weaver", 
                                  "Mnemosyne", "Pythia", "Argus", "Messenger", "Eris"}
        self._patterns = {
            "OBS": [
                r"\[agent:(?P<agent>\w+)\] vector=\[(?P<vec>[^\]]+)\] entropy=(?P<ent>[\d\.]+)",
                r"Observation from (?P<agent>\w+): .*?Vector: \[(?P<vec>[^\]]*)\] Entropy: (?P<ent>[\d\.]+)"
            ],
            "AUDIT": [
                r"\[(?P<severity>high|medium|low)\] Warning - (?P<cause>[^.!\n]+)",
                r"(?:Anomaly|Error|Warning) detected: (?P<cause>[^.!\n]+)"
            ],
            "CONTROL": [
                r"Action Required: (?P<action>\w+) due to (?P<reason>[^.!\n ]+)",
                r"(?<action>RESET|HALT) Command: .*",
                r"\[agent:(?P<agent>\w+)\] Control: (?P<action>\w+) Reason: (?P<reason>.*)"
            ]
        }

    def _sanitize_observation(self, vec_list: list, ent_input: float) -> tuple[list, float]:
        if not vec_list:
            return [], 0.0
        try:
            arr = np.array(vec_list, dtype=np.float64)
            norm = np.linalg.norm(arr)
            normalized_v = (arr / norm).tolist() if norm > 1e-9 else [0.0] * len(arr)
            
            p = (np.abs(arr)/norm)**2 if norm > 1e-9 else np.array([1.0])
            entropy_calc = -np.sum(p * np.log2(p + 1e-15))
            
            if abs(entropy_calc - ent_input) > 0.1:
                return normalized_v, -1.0  
            return normalized_v, float(entropy_calc)
        except Exception:
            return [], 0.0

    def parse(self, text: str, orphan_origin: str = "System") -> List[CouncilSignal]:
        signals = []
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line: continue
            found = False

            for p in self._patterns["CONTROL"]:
                m = re.search(p, line, re.IGNORECASE)
                if m:
                    d = m.groupdict()
                    signals.append(ControlSignal(
                        type="CTRL", 
                        origin_id=orphan_origin if not d.get('agent') else d['agent'],
                        target_id="Orchestrator",
                        sequence_id=int(time.time() * 1000) % 10000,
                        action=d['action'].upper(),
                        reason=d.get('reason', 'No reason provided')
                    ))
                    found = True; break
            if found: continue

            for p in self._patterns["AUDIT"]:
                m = re.search(p, line, re.IGNORECASE)
                if m:
                    d = m.groupdict()
                    signals.append(AuditSignal(
                        type="AUDIT", 
                        origin_id=orphan_origin, 
                        target_id="SecurityMonitor",
                        sequence_id=int(time.time() * 1000) % 10000,
                        reason=d['cause'].strip(),
                        severity=d.get('severity', 'low').lower()
                    ))
                    found = True; break
            if found: continue

            for p in self._patterns["OBS"]:
                m = re.search(p, line, re.IGNORECASE)
                if m:
                    d = m.groupdict()
                    agent_name = d.get('agent', orphan_origin).strip()
                    if agent_name not in self._valid_archetypes and agent_name != "UnknownAgent":
                        agent_name = "UnknownAgent"

                    vec_raw = d.get('vec', '[]')
                    try:
                        vec_list = [float(x.strip()) for x in vec_raw.replace('[','').replace(']','').split(',') if x.strip()]
                    except ValueError:
                        vec_list = []

                    ent_in = float(d.get('ent', 0.0))
                    v, e = self._sanitize_observation(vec_list, ent_in)

                    signals.append(ObservationSignal(
                        type="OBS",
                        origin_id=agent_name,
                        target_id="Router",
                        sequence_id=int(time.time() * 1000) % 10000,
                        intent_vector=[0.0]*8, 
                        perceived_entropy=e if e >= 0 else 0.0,
                        observation_vector=v
                    ))
                    found = True; break
        return signals

class SignalParser:
    def __init__(self): self._parser = TopologyAwareParser()
    def parse(self, text: str) -> List[CouncilSignal]: return self._parser.parse(text)
