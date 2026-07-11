import os
import sys
import asyncio
import random
import time

# Ensure project root is in the path for imports
PROJECT_ROOT = "/home/anonz/projects/the-council"
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

class RecursiveOrchestrator:
    """
    Phase 5 Core Implementation: Fractal Orchestration Loop.
    Implements recursive depth-first task decomposition.
    """
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.total_tasks_spawned = 0

    async def execute(self, task_name: str, current_depth: int) -> list:
        """Recursively spawns sub-agent tasks until max depth is reached."""
        if current_depth > self.max_depth:
            return []

        print(f"🌀 [LAYER {current_depth}] Orchestrating Task: '{task_name}'...")
        
        # 1. Macro/Meso decomposition (Spawning sub-tasks)
        # Every task is decomposed into N sub-dependencies for the next layer
        sub_tasks = []
        num_children = random.randint(2, 4)
        for i in range(num_children):
            child_task = f"{task_name}_Sub{i}"
            sub_tasks.append(self.execute(child_task, current_depth + 1))

        # Wait for all sub-agents in this layer to resolve
        results = await asyncio.gather(*sub_tasks)
        
        self.total_tasks_spawned += num_children
        
        # Flatten results from children for the parent tracker
        flattened_results = []
        for r in results:
            if isinstance(r, list):
                flattened_results.extend(r)
            else:
                flattened_results.append(r)

        return [f"Completed '{task_name}' at L{current_depth}"] + flattened_results

    async def run_simulation(self, initial_goal: str):
        start_time = time.perf_counter()
        print(f"\n🚀 INITIATING RECURSIVE FRACTAL LOOP")
        print(f"Initial Goal: '{initial_goal}'\n")
        
        # explicitly pass 1 as the first layer depth
        results = await self.execute(initial_goal, 1)
        
        duration = time.perf_counter() - start_time
        print("\n--- [PHASE 5 SIMULATION REPORT] ---")
        print(f"Execution Time: {duration:.2f}s")
        print(f"Total Task Lifecycle Events (Sub-tasks): {len(results) - 1}")
        # Note: results includes the current task + its children's contents.
        # Detailed count is provided by tracking sub_tasks spawned.
        return results

if __name__ == "__main__":
    import asyncio
    orch = RecursiveOrchestrator(max_depth=3)
    asyncio.run(orch.run_simulation("Achieve Self-Sustaining Autonomy"))
