import asyncio
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, field

try:
    from council.core.domain import CouncilSignal, ObservationSignal, AuditSignal, ControlSignal
except ImportError:
    # Fallback for environments where pythonpath might not be set correctly during development
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)).replace('logic', '')) # This is a hacky fallback; the user's environment should have PYTHONPATH=.
    from council.core.domain import CouncilSignal, ObservationSignal, AuditSignal, ControlSignal

class CognitiveEngine:
    def __init__(self):
        self.event_queue = asyncio.PriorityQueue()
        self.active_tasks = set()
        self.is_running = False

    async def emit(self, signal: Union[CouncilSignal, Any], priority: int = 2):
        await self.event_queue.put((priority, signal))

    async def monitor_loop(self):
        print("[Engine] Monitor loop started.")
        try:
            while self.is_running:
                if self.event_queue.empty():
                    await asyncio.sleep(0.1)
                    continue
                priority, signal = await self.event_queue.get()

                # Unified handling for different signal implementations (direct or via duck typing)
                action = getattr(signal, 'action', '').upper() if isinstance(signal, ControlSignal) else ""
                if action in ["RESET", "HALT"]:
                    reason = getattr(signal, 'reason', 'unknown')
                    print(f"[Engine] 🚨 Reset Command Received: {reason}")
                    for task in list(self.active_tasks):
                        task.cancel()

                elif hasattr(signal, 'cause'): # AuditSignal
                    severity = getattr(signal, 'severity', 'low').lower()
                    cause = getattr(signal, 'cause', 'unknown')
                    if severity in ["high", "critical"]:
                        print(f"[Engine] ⚠️ High-priority audit detected: {cause}")
                        # Re-emit as a control signal for immediate response
                        await self.emit(ControlSignal(type="CTRL_RECALIBRATE", action="RESET", reason=f"Audit: {cause}"), priority=1)

                self.event_queue.task_done()
        except asyncio.CancelledError:
            print("[Engine] Monitor loop cancelled.")
        except Exception as e:
            print(f"[Engine Error in monitor_loop] {e}")

    async def run(self, tasks_config: List[Callable]):
        self.is_running = True
        monitor_task = asyncio.create_task(self.monitor_loop())
        self.active_tasks.add(monitor_task)
        try:
            work_tasks = []
            for t in tasks_config:
                # The user's simulation calls things like lambda e: executor(...) 
                # so we must handle both the coroutine itself and a callable that returns it.
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
            for t in list(self.active_tasks): 
                if not t.done():
                    t.cancel()
print("Engine refactor complete locally.")