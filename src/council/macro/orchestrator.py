from __future__ import annotations
import asyncio
import os
import sys
import enum
from datetime import datetime
from typing import Union, Any, List, Callable, Dict, Optional

try:
    from council.core.domain import (
        CouncilSignal, 
        ObservationSignal, 
        AuditSignal, 
        ControlSignal,
        LoopState
    )
except ImportError:
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "projects/the-council/src")))
    from council.core.domain import (
        CouncilSignal, 
        ObservationSignal, 
        AuditSignal, 
        ControlSignal,
        LoopState
    )

class OrchestratorMode(enum.Enum):
    NOMINAL = "NOMINAL"           # Standard operation
    RECALIBRATING = "RECALIBRATING" # Adjusting state due to drift/entropy
    STABILIZING = "STABILIZING"   # High-priority response to audit/threats
    HALTED = "HALTED"             # Systemic pause

class CognitiveEngine:
    """
    Macro-Scale Orchestrator: A Hierarchical Finite Automaton (HFA) for high-fidelity control.
    Implements anticipatory logic and context-preserving signal inference.
    """
    def __init__(self):
        self._event_queue = asyncio.PriorityQueue()
        self._active_tasks = set()
        self._mode: OrchestratorMode = OrchestratorMode.NOMINAL
        self._system_id = "System"
        # Context window for cross-task intent injection
        self._context_buffer: List[Dict[str, Any]] = []
        # NEW: Observer Registry to bridge Meso/Macro layers
        self._observers: List[Any] = []

    @property
    def mode(self) -> OrchestratorMode:
        return self._mode

    async def _transition_to(self, new_mode: OrchestratorMode, reason: str):
        if self._mode != new_mode:
            print(f"[Engine: HFA] 🔄 Transition: {self._mode.name} -> {new_mode.name} | Reason: {reason}")
            self._mode = new_mode

    async def register_observer(self, observer: Any):
        '''Registers a monitoring component (e.g., SemanticEvaluator) into the engine loop.'''
        self._observers.append(observer)
        print(f"[Engine] 🧩 Registered Observer: {type(observer).__name__}")

    async def _infer_identity(self, signal: Any) -> str:
        """Performs heuristic identity inference on unheadered signals to prevent loss of archetypal context."""
        origin_id = getattr(signal, 'origin_id', None)
        if origin_id and origin_id != self._system_id:
            return origin_id
        
        payload = str(getattr(signal, 'reason', '')).lower()
        if 'entropy' in payload or 'drift' in payload:
            return "Lyria" 
        if 'audit' in payload or 'threat' in payload:
            return "Silas"  
        return self._system_id

    async def emit(self, signal: Union[CouncilSignal, Any], priority: int = 2):
        """Processes and injects signals into the event loop with identity inference."""
        origin_id = getattr(signal, 'origin_id', None)
        target_id = getattr(signal, 'target_id', "Orchestrator")

        if not origin_id or origin_id == self._system_id:
            inferred_id = await self._infer_identity(signal)
            reason = f"Inferred identity from payload: {type(signal).__name__}"
            
            # Detection of mode shift from signal content (Simulation for demonstration)
            if "STABILIZE" in str(signal).upper():
                await self._transition_to(OrchestratorMode.STABILIZING, reason)

            signal = ControlSignal(
                type=getattr(signal, 'type', "SYSTEM_RECOVERY"), 
                origin_id=inferred_id if inferred_id != self._system_id else origin_id,
                target_id=target_id,
                sequence_id=0,
                action="WRAP",
                reason=reason
            )

        await self._event_queue.put((priority, signal))

    async def monitor_loop(self):
        print(f"[Engine: HFA] 👁️ Monitor loop initialized in {self._mode.name} mode.")
        try:
            while True:
                if self._event_queue.empty():
                    await asyncio.sleep(0.1)
                    continue

                priority, signal = await self._event_queue.get()
                
                # 1. Observer Relay (Meso -> Macro bridge)
                for observer in self._observers:
                    if hasattr(observer, 'process_signal'):
                        try:
                            result = await observer.process_signal(signal)
                            if result and isinstance(result, ControlSignal):
                                # Re-inject control signals at high priority
                                await self.emit(result, priority=0)
                        except Exception as e:
                            print(f"[Engine] ⚠️ Observer Error ({type(observer).__name__}): {e}")

                # 2. HFA State Machine Logic
                action = getattr(signal, 'action', '').upper() if isinstance(signal, ControlSignal) else ""
                
                if action in ["RESET", "HALT"] or self._mode == OrchestratorMode.STABILIZING:
                    reason = getattr(signal, 'reason', 'unknown')
                    print(f"[Engine: HFA] 🚨 Mode Override: {action} | Reason: {reason}")
                    for task in list(self._active_tasks):
                        if not task.done():
                            task.cancel()

                # Audit Logic (Handling High-Priority audit signals)
                if isinstance(signal, AuditSignal):
                    severity = getattr(signal, 'severity', 'low').lower()
                    cause = getattr(signal, 'cause', 'unknown')
                    if severity in ["high", "critical"]:
                        await self._transition_to(OrchestratorMode.STABILIZING, f"Audit: {cause}")
                        # Trigger emergency recalibration jump-start
                        await self.emit(ControlSignal(
                            type="RECALIBRATE", 
                            origin_id=self._system_id,
                            target_id=self._system_id,
                            sequence_id=999, 
                            action="RESET", 
                            reason=f"Emergency Audit Recalibration: {cause}"
                        ), priority=0)

                self._event_queue.task_done()

        except asyncio.CancelledError:
            print("[Engine] Monitor loop shutdown gracefully.")
        except Exception as e:
            print(f"[Engine Error] CRITICAL FATAL EXCEPTION: {e}")
            await self._transition_to(OrchestratorMode.HALTED, str(e))

    async def run(self, tasks_config: List[Callable]):
        self.is_running = True
        monitor_task = asyncio.create_task(self.monitor_loop())
        self._active_tasks.add(monitor_task)
        try:
            work_tasks = []
            for t in tasks_config:
                if asyncio.iscoroutinefunction(t):
                    work_tasks.append(asyncio.create_task(t(self)))
                else:
                    res = t(self) if callable(t) else None
                    if asyncio.iscoroutine(res):
                        work_tasks.append(asyncio.create_task(res))
            await asyncio.gather(*work_tasks, return_exceptions=True)
        finally:
            self.is_running = False
            monitor_task.cancel()
            for t in list(self._active_tasks): 
                if not t.done():
                    t.cancel()
