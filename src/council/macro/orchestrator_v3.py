import asyncio
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class MockContext:
    raw_input: str = ""
    intent_vector: List[float] = field(default_factory=lambda: [0.0]*8)
    active_tasks: List[str] = field(default_factory=list)
    is_aborted: bool = False

class AsyncCouncilOrchestrator:
    def __init__(self, max_depth: int = 2):
        self.max_depth = max_depth
        self.history: List[Dict[str, Any]] = []

    async def execute(self, name: str, context: MockContext, depth: int) -> None:
        if depth > self.max_depth:
            print(f"[!] Max Depth ({self.max_depth}) reached at level {depth}. Terminating branch.")
            return

        print(f"[L{depth}] >>> Starting Orchestration Cycle for Task: '{name}'")
        start_time = time.perf_counter()

        # Simulation of "Expansion" (The Weaver/Elis logic)
        if depth < self.max_depth and context.raw_input != "TERMINATE":
            new_task_id = f"SubTask_{name}_{depth}"
            print(f"[L{depth}] [Weaver] Branching: Spawning sub-tasks for level {depth + 1}...")
            context.active_tasks.append(new_task_id)
            await asyncio.sleep(0.2)

        # Simulate processing time and vector shift
        for i in range(3):
            if not context.is_aborted:
                context.intent_vector[i % 8] += 0.15

        elapsed = time.perf_counter() - start_time
        print(f"[L{depth}] <<< Layer Cycle Complete ({elapsed:.4f}s)")

        # Recurse if we have subtasks and depth allows
        if context.active_tasks and depth < self.max_depth:
            next_task = context.active_tasks.pop(0)
            await self.execute(next_task, context, depth + 1)

async def run_pilot():
    orch = AsyncCouncilOrchestrator(max_depth=2)
    ctx = MockContext()
    print("--- Initializing Pipeline ---")
    start_time = time.perf_counter()
    await orch.execute("Primary Mission", ctx, depth=0)
    end_time = time.perf_counter()

    print("\n=== PILOT REPORT ===")
    print(f"Total Duration: {end_time - start_time:.4f}s")
    print(f"Final Intent Vector (Sample): {[round(v, 2) for v in ctx.intent_vector[:5]]}")
    print(f"Remaining Tasks Queue: {len(ctx.active_tasks)}")

if __name__ == '__main__':
    asyncio.run(run_pilot())

