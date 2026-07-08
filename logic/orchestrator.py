import asyncio
import time
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field

# --- CP-1 Signal Schemas (Abstracted) ---

@dataclass(frozen=True)
class CouncilSignal:
    """Base class for all signals defined in CP-1."""
    type: str
    timestamp: float = field(default_factory=time.time)

@dataclass(frozen=True)
class ObservationSignal(CouncilSignal):
    agent: str = ""
    vector: List[float] = field(default_factory=list)
    entropy: float = 0.0

@dataclass(frozen=True)
class AuditSignal(CouncilSignal):
    cause: str = ""
    severity: str = "low"  # low, medium, high, critical

@dataclass(frozen=True)
class ControlSignal(CouncilSignal):
    reason: str = ""
    action: str = "" # RESET, HALT

# --- Orchestrator Components ---

class CognitiveEngine:
    """
    The central orchestration layer for The Council.
    Implements the Triple-Loop logic via an asynchronous event queue.
    """
    def __init__(self):
        self.event_queue = asyncio.PriorityQueue()
        self.active_tasks = set()
        self.is_running = False

    async def emit(self, signal: CouncilSignal, priority: int = 2):
        await self.event_queue.put((priority, signal))

    async def monitor_loop(self):
        while self.is_running:
            try:
                priority, signal = await self.event_queue.get()
                if isinstance(signal, ControlSignal):
                    await self._handle_control(signal)
                elif isinstance(signal, AuditSignal):
                    await self._handle_audit(signal)
                self.event_queue.task_done()
            except Exception as e:
                print(f"[Engine Error] {e}")
                break

    async def _handle_control(self, signal: ControlSignal):
        if signal.action == "RESET":
            for task in list(self.active_tasks):
                task.cancel()
            # Re-add the current loop to allow new tasks to pick up after reset if needed
            print(f"[Engine] 🚨 {signal.reason}: Resetting active tasks...")

    async def _handle_audit(self, signal: AuditSignal):
        if signal.severity in ("high", "critical"):
            await self.emit(ControlSignal(type="CTRL_RECALIBRATE", reason=signal.cause, action="RESET"), priority=1)

    async def task_runner(self, task_id: str, worker_func):
        try:
            await worker_func(self)
        except asyncio.CancelledError:
            # This is expected when a RESET occurs
            pass
        except Exception as e:
            print(f"[Task-{task_id}] Failed: {e}")

    async def run(self, tasks: List[callable]):
        self.is_running = True
        monitor_task = asyncio.create_task(self.monitor_loop())
        work_tasks = [asyncio.create_task(self.task_runner(f"Agent-{i}", t)) 
                      for i, t in enumerate(tasks)]
        self.active_tasks.update(work_tasks)

        # Wait for workers to finish or engine to stop
        await asyncio.gather(*work_tasks, return_exceptions=True)
        self.is_running = False
        monitor_task.cancel()

# --- Testable Workflows ---

async def stable_worker(engine: CognitiveEngine):
    for i in range(10):
        await asyncio.sleep(0.5)

async def chaos_worker(engine: CognitiveEngine):
    """Simulates a task that eventually causes high entropy."""
    for i in range(10):
        await asyncio.sleep(0.5)
        if i == 3:
            print("  [ChaosAgent] Triggering anomaly...")
            await engine.emit(AuditSignal(type="AUDIT", cause="Entropy Spike", severity="high"))

async def drift_worker(engine: CognitiveEngine):
    """Simulates a task that eventually causes semantic misalignment."""
    for i in range(10):
        await asyncio.sleep(1)
        if i == 4:
            print("  [DriftAgent] Drifting away from Prime Directive...")
            await engine.emit(ControlSignal(type="CTRL_RECALIBRATE", reason="Semantic Drift", action="RESET"))

if __name__ == "__main__":
    async def main():
        engine = CognitiveEngine()
        print("=== Testing Integrated Control Loop ===")
        # Run stable task and chaos task concurrently
        await engine.run([stable_worker, chaos_worker, drift_worker])
        print("=== Test Complete ===")

    asyncio.run(main())
