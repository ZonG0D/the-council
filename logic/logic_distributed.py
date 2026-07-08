import os
import sys
import subprocess
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any

# Standard imports from the Council core
try:
    from logic.orchestrator import CognitiveEngine, ControlSignal
    from logic.signal_parser import SignalParser
except ImportError:
    # Fallback for standalone execution during debugging
    @dataclass(frozen=True)
    class ControlSignal:
        type: str
        action: str = ""
        reason: str = ""

    class CognitiveEngine:
        def __init__(self): self.is_running = False; self.event_queue = []
        async def emit(self, s, priority=1): print(f"Emitted {s}")
        async def monitor_loop(self): pass
        async def run(self, ws): self.is_running = True; await asyncio.gather(*ws)

    class SignalParser:
        def parse(self, t): return []

class ShellExecutor:
    """
    The 'Hands' of the Council. 
    Executes shell commands as subprocesses and feeds results into the Engine.
    """
    def __init__(self, engine: CognitiveEngine, parser: SignalParser):
        self.engine = engine
        self.parser = parser

    async def execute(self, command: str) -> str:
        print(f"[Executor] Executing: {command}")
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        output = stdout.decode().strip()
        error = stderr.decode().strip()
        
        # Feed output back into the engine for continuous perception
        if output:
            print(f"[Executor-Out] {output}")
            for sig in self.parser.parse(f"Output: {output[:100]}"):
                await self.engine.emit(sig, priority=2)
        
        if error:
            print(f"[Executor-Err] {error}")
            for sig in self.parser.parse(f"Error: {error[:100]}"):
                await self.engine.emit(sig, priority=0) # High priority for errors

        return output if process.returncode == 0 else f"FAILED_CODE_{process.returncode}: {error}"

class DistributedSupervisor:
    """The 'Nervous System' overseeing independent execution processes."""
    def __init__(self, engine: CognitiveEngine, parser: SignalParser):
        self.engine = engine
        self.parser = parser

    async def run_task(self, executor: ShellExecutor, command: str):
        print(f"[Supervisor] Launching task: {command}")
        res = await executor.execute(command)
        print(f"[Supervisor] Task completed with result/error.")
        return res

async def pilot_demo():
    """
    Demonstrates the Autonomous Control Loop:
    Command -> Shell Execution -> Error Detection (via Parser) -> Reset Signal.
    """
    engine = CognitiveEngine()
    parser = SignalParser()
    executor = ShellExecutor(engine, parser)
    supervisor = DistributedSupervisor(engine, parser)

    print("\n" + "="*60)
    print("   AUTONOMOUS CONTROL LOOP PILOT")
    print("="*60)

    # We simulate the 'Systemic Chaos' where a commanded task fails.
    # The agent is asked to do something that will fail (e.g., reach for a non-existent folder).
    target_cmd = "command_that_fails_immediately && echo 'This shouldn't print'"
    
    print(f"[System] Scenario: Attempting impossible command.")
    print(f"[System] Expected behavior: Engine detects error -> Signals RESET/Audit -> Self-corrects/Halts.\n")

    engine.is_running = True
    monitor_task = asyncio.create_task(engine.monitor_loop())
    
    # Start the execution as a task so we can observe its lifecycle
    exec_task = asyncio.create_task(supervisor.run_task(executor, target_cmd))

    try:
        await asyncio.wait([exec_task], timeout=5)
    except Exception as e:
        print(f"Pilot Error: {e}")
    finally:
        engine.is_running = False
        monitor_task.cancel()
        await old_cleanup_logic(executor, exec_task)

async def old_cleanup_logic(executor, task):
    """Safely stop tasks."""
    if not task.done():
        task.cancel()
        try: await task
        except asyncio.CancelledError: pass

if __name__ == "__main__":
    # Ensure we can import the logic correctly when running this file directly
    import sys, os
    sys_path = os.path.abspath(os.path.dirname(__file__))
    if sys_path not in sys.path:
        sys.path.append(sys_path)

    asyncio.run(pilot_demo())
