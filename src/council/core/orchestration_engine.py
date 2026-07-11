import asyncio
import os
from datetime import datetime

class OrchestrationEngine:
    """The Macro Scale Controller for spawning and managing autonomous agent sub-tasks."""
    def __init__(self, workspace="/home/anonz/projects/the-council"):
        self.workspace = workspace
        self._running_tasks = []

    async def spawn_task(self, cmd: str, name: str):
        """Spawns an asynchronous sub-process using correctly implemented asyncio primitives."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] [ORCHESTRATOR] Spawning Sub-Task: {name}")
        try:
            # Using the correct method for non-blocking subprocess creation in async environments
            process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            self._running_tasks.append((process, name))
            print(f"[ORCHESTRATOR] Task '{name}' initialized with PID: {process.pid}")
            return process, name
        except Exception as e:
            print(f"[CRITICAL ORCHESTRATION ERROR]: Failed to spawn {name}: {e}")
            return None, str(e)

    async def run_sequence(self, duration=15):
        """Executes a series of tasks in an unprompted management cycle."""
        print("\n" + "="*48)
        print("ORCHESTRATOR: COMMENCING AUTONOMOUS SEQUENCE")
        print("-" * 48 + "\n[SEQUENCE START]")

        test_cmd = "python3 /home/anonz/projects/the-council/src/council/core/sentinel_runtime.py"
        tasks_to_run = [(test_cmd, f"Sentinel_{i}") for i in range(2)]

        active_processes = []
        for cmd, name in tasks_to_run:
            proc, proc_name = await self.spawn_task(cmd, name)
            if proc: 
                active_processes.append((proc, proc_name))

        await asyncio.sleep(duration)               

        print("\n==============================")
        print("[ORCHESTRATOR] SEQUENCE PHASE COMPLETE.")
        print("=" * 48 + "\n")

if __name__ == "__main__":
    import asyncio; orch = OrchestrationEngine(); asyncio.run(orch.run_sequence())
