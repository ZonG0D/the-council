import asyncio
import sys
from typing import List, Callable, Any
from dataclasses import dataclass

# Mocking the signal schemas for isolation in this script
@dataclass(frozen=True)
class ControlSignal:
    type: str
    reason: str = ""
    action: str = "RESET"

class CognitiveEngine:
    """
    The Core of Autonomy: The Orchestrator with Active Preemption.
    Implements the ability to interrupt and reset running tasks upon receiving high-priority ControlSignals.
    """
    def __init__(self):
        self.event_queue = asyncio.PriorityQueue()
        self.active_tasks = set()  # Set of active asyncio.Task objects
        self.is_running = False

    async def emit(self, signal: Any, priority: int = 2):
        """Pushes a signal into the engine."""
        await self.event_queue.put((priority, signal))

    async def monitor_loop(self):
        while self.is_running:
            try:
                priority, signal = await self.event_queue.get()
                if isinstance(signal, ControlSignal) and signal.action == "RESET":
                    await self._handle_reset(signal.reason)
                else:
                    print(f"[Engine] Received {type(signal).__name__}: {getattr(signal, 'reason', '')}")
                self.event_queue.task_done()
            except Exception as e:
                print(f"[Engine Monitor Error] {e}")

    async def _handle_reset(self, reason: str):
        print(f"\n[ENGINE-CONTROL] 🚨 RESET TRIGGERED: {reason}")
        # PREEMPTION LOGIC: Cancel all existing tasks immediately.
        if self.active_tasks:
            for task in list(self.active_tasks):
                task.cancel()
            await asyncio.gather(*self.active_tasks, return_exceptions=True)
            self.active_tasks.clear()
            print("[Engine] All tasks successfully terminated/preempted.")

    async def run(self, workers: List[Callable]):
        self.is_running = True
        # Start the background controller
        monitor_task = asyncio.create_task(self.monitor_loop())
        
        # Launch worker tasks
        tasks = []
        for w in workers:
            t = asyncio.create_task(w(self))
            tasks.append(t)
            self.active_tasks.add(t)
        
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        finally:
            self.is_running = False  # Stop the monitor loop

    async def task_wrapper(self, coro):
        """Wraps a coroutine to track it in active_tasks."""
        task = asyncio.current_task()
        self.active_tasks.add(task)
        try:
            await coro
        finally:
            self.active_tasks.discard(task)

if __name__ == "__main__":
    async def heavy_worker(engine):
        print("[Worker] Started long-running task.")
        try:
            for i in range(10):
                await asyncio.sleep(1)
                print(f"[Worker] Step {i}...")
            print("[Worker] Task finished naturally.")
        except asyncio.CancelledError:
            print("[Worker] PREEMPTED by Engine!")
            raise # Re-raise to allow cleaning up

    async def main():
        engine = CognitiveEngine()
        await engine.run([heavy_worker])

    asyncio.run(main())
