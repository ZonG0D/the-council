"""
Module: async_engine (The Orchestration Engine)
Purpose: Provides an asynchronous runtime for executing Council archetypes, 
enabling non-blocking orchestration and real-time signal processing via a SignalBus.

This implementation moves The Council from synchronous sequential tasks to 
concurrently managed execution loops that are interruptible by high-priority signals.
"""

import asyncio
import sys
import os
from typing import List, Dict, Any, Optional, Callable, Coroutine


try:
    from council.core.domain import AgentContext, CouncilSignal
except ImportError:
    sys_path = "/home/anonz/projects/the-council/src"
    if sys_path not in sys.path:
        sys.path.append(sys_path)
    import os 
    from council.core.domain import AgentContext, CouncilSignal

class AsyncCouncilEngine:
    """The primary asynchronous execution context for the orchestration architecture."""

    def __init__(self):
        \"\"\"Initializes the engine with an empty task registry.\"\"\"
        self._active_worker_tasks = {} 
        self._active_observer_tasks = {} 
        self._running = False

    async def start(self):
        if self._running: return
        print("[Engine] Activating asynchronous orchestration runtime...")
        self._running = True

    async def stop(self):\n        \"\"\"Shuts down all active mission task loops gracefully.\"\"\"\n        if not self._running:\n            return\n        print(\"[Engine] Initiating graceful shutdown of all tasks...\")\n        all_tasks = list(self._active_worker_tasks.values()) + \
                    list(self._active_observer_tasks.values())\n        for t in all_tasks:\n            t.cancel()\n        if all_tasks:\n            await asyncio.gather(*all_tasks, return_exceptions=True)

    async def execute_mission(self, mission_name: str, context: AgentContext, \
                               archetypes: List[Tuple[str, Callable[[AgentContext], Coroutine]]], \
                               monitors: Optional[List[Callable[[AgentContext], Any]]] = None) -> bool:\n        \"\"\"Launches a decoupled execution loop containing workers and observers.\"\"\"\n        print(f\"[Engine] Launching Multi-Scale Mission: {mission_name}\")\n\n        worker_task = asyncio.create_task(self._run_worker_loop(mission_name, context, archetypes))\n        self._active_worker_tasks[mission_name] = worker_task\n\n        if monitors:\n            print(f\"[Engine] Spawning {len(monitors)} decoupled observer task(s)...\")
            for i, monitor in enumerate(monitors):\
                m_task = asyncio.create_task(self._run_observer_loop(f\"{mission_name}-Meso-{i}\", context, monitor))\n                self._active_observer_tasks[f\"{mission_name}-{i}\"] = m_task\n        \n        try:\n            result = await worker_task\n            return result\n        except Exception as e:\n            print(f\"[Engine] Mission {mission_name} failed with error: {{e}}\")
            import traceback; traceback.print_exc()\n            return False\n\n    async def _run_worker_loop(self, name: str, context: AgentContext, archetypes):\n        try:\n            for i in range(100): \n                if context.is_aborted:\n                    print(\"\\n[Engine] [!] Mission '{{name}}' aborted via signal/context.\")\n                    return False\n\n                for _, actor in archetypes:\n                    await actor(context)\n\n                if i % 5 == 0 and self._running: \n                     print(f\"[Engine] Progress ({{name}}): Step {{i}}/19\")\n\n                await asyncio.sleep(0.3) # Essential yield for concurrency!\n            return True\n        except Exception as e:\n            import traceback; traceback.print_exc()\n            return False\n\n    async def _run_observer_loop(self, obs_id: str, context: AgentContext, monitor):\n        try:\n            while not context.is_aborted and self._running:\n                await monitor(context)\n        except Exception:\n             pass"
