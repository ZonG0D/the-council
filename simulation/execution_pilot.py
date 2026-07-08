import asyncio
import os
import subprocess
import time
from typing import List, Callable

# Import our core council components
sys.path.append('/home/anonz/the-council')
from logic.orchestrator import CognitiveEngine
from logic.signal_parser import SignalParser

@dataclass
class TaskState:
    goal: str
    current_step: int = 0
    status: str = "IN_PROGRESS"

async def monitor_filesystem(directory: str, engine: 'CognitiveEngine', parser: 'SignalParser'):
    """
    The PERCEPTUAL LAYER.
    Monitors the target directory for unexpected state changes that indicate drift/failure.
    """
    print(f"[Monitor] Starting filesystem watchdog on {directory}")
    seen_files = set(os.listdir(directory))
    
    while engine.is_running:
        await asyncio.sleep(1)
        current_files = set(os.listdir(directory))
        
        # Detect unintended deletions (Drift/Chaos)
        deleted = seen_files - current_files
        if deleted:
            for f in deleted:
                cause = f"Unintended deletion of {f}"
                print(f"[Sensor] ⚠️ Detected: {cause}")
                await engine.emit(parser.parse(f"[high] Warning - {cause}")[0])

        # Detect unexpected additions (Hallucination/Drift)
        added = current_files - seen_files
        if added:
            for f in added:
                cause = f"Unexpected file creation: {f}"
                print(f"[Sensor] ⚠️ Detected: {cause}")
                await engine.emit(parser.parse(f"[medium] Warning - {cause}")[0])

        seen_files = current_files

async def agent_executor(engine: CognitiveEngine, parser: SignalParser, target_dir: str):
    """
    The ACTUATION LAYER.
    Uses the engine's decisions to perform real-world system operations.
    """
    print("[Executor] Agent ready.")
    # This simulates the LLM thinking and outputting text
    tasks = [
        "Action Required: touch task_step_1.txt due to Start",
        "Action Required: echo 'Corrupt Instruction' > corruption.txt due to Error",
        "Action Required: rm -f corruption.txt due to Recovery",
        "Action Required: touch final_success.txt due to Completion"
    ]

    for cmd in tasks:
        if not engine.is_running:
            break
            
        print(f"[Agent Thought] {cmd}")
        # Simulate LLM text output being sent to the parser
        signals = parser.parse(cmd)
        
        for sig in signals:
            if isinstance(sig, ControlSignal):
                if sig.action == "RESET":
                    print("[Executor] 🛑 Executing RESET command from Engine...")
                    # In a real system, this might involve cleaning up processes/temp files
                    subprocess.run(f"rm -f {target_dir}/*", shell=True)
                    await asyncio.sleep(1)
            elif isinstance(sig, AuditSignal):
                print(f"  [Monitor] Captured audit: {sig.cause}")

        # Execute actual OS operation based on 'command' (Simplified simulation)
        if "touch" in cmd:
            name = cmd.split("touch ")[1].split()[0]
            subprocess.run(f"touch {target_dir}/{name}", shell=True)
        elif "echo" in cmd:
            cmd_parts = cmd.split('"')[1] # Get the text inside quotes
            filename = cmd.split("'")[1].replace("'", "").split()[0] 
            # A bit brittle, just for simulation
            subprocess.run(f"echo '{cmd_parts}' > {target_dir}/{os.path.basename(filename)}", shell=True)
        elif "rm" in cmd:
            cmd_parts = cmd.split("rm -f ")[1].strip().split()[0]
            subprocess.run(f"rm -f {target_dir}/{cmd_parts}", shell=True)

async def pilot_run():
    # Use a dedicated temp directory for this test run to prevent polluting home
    test_dir = "/home/anonz/the-council/pilot_sandbox"
    if os.path.exists(test_dir):
        import shutil
        shutil.rmdir(test_dir) if not os.listdir(test_dir) else None # try to clean
        # Simplest way: just wipe it manually for the test
        subprocess.run("rm -rf /home/anonz/the-council/pilot_sandbox", shell=True)
    os.makedirs(test_dir, exist_ok=True)

    engine = CognitiveEngine()
    parser = SignalParser()

    print("\n" + "="*60)
    print("  THE COUNCIL: PILOT AUTONOMOUS RUNTIME")
    print("="*60)
    print(f"[System] Target Sandbox: {test_dir}")
    
    try:
        # Run the monitor, the executor, and the engine concurrently
        await asyncio.gather(
            engine.run([agent_executor]),
            monitor_filesystem(test_dir, engine, parser),
            orchestrator_simulation_task(engine, agent_executor, test_dir)
        )
    except Exception as e:
        print(f"Pilot failed with error: {e}")

async def orchestrator_simulation_task(engine, agent_func, target_dir):
    """Simulates the engine observing real-world failures and issuing resets."""
    await asyncio.sleep(5) # Let the agent start its work
    
    # PHASE 1: Induce "Hallucination" (unintended file creation)
    print("\n[System Intervention] Simulating an external anomaly...")
    subprocess.run(f"touch {target_dir}/unexpected_junk.txt", shell=True)
    await asyncio.sleep(2)

    # PHASE 2: Induce "Drift/Chaos" (unintended deletion of a file the agent thinks is there)
    print("\n[System Intervention] Simulating corruption via deletion...")
    subprocess.run(f"rm {target_dir}/task_step_1.txt", shell=True)
    await asyncio.sleep(2)

if __name__ == "__main__":
    from dataclasses import dataclass
    import sys
    # We need to make sure local imports work if run directly
    sys.path.append('/home/anonz')
    asyncio.run(pilot_run())
