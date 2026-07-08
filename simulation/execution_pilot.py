import os
import sys
repo_root = os.path.abspath('/home/anonz/the-council')
if repo_root not in sys.path:
    sys.path.append(repo_root)
import os
import sys
import asyncio
import os
import subprocess
import sys


from logic.orchestrator import CognitiveEngine, ControlSignal, AuditSignal
from logic.domain import AgentContext
from logic.signal_parser import SignalParser

async def monitor(directory: str, engine: 'CognitiveEngine', parser: 'SignalParser'):
    print(f"[Monitor] Watchdog started on {directory}")
    if not os.path.exists(directory):
        os.makedirs(directory)
    seen = set(os.listdir(directory))
    try:
        while engine.is_running:
            await asyncio.sleep(0.5)
            if not os.path.exists(directory): break
            curr = list(set(os.listdir(directory)))
            for f in (set(seen) - set(curr)):
                msg = f"[high] Warning - Deletion of {f}"
                signals = parser.parse(msg)
                if signals: await engine.emit(signals[0])
            seen = curr
    except Exception as e:
        print(f"Monitor Error: {e}")

async def executor(engine, parser, target_dir):
    print("[Executor] Agent ready.")
    tasks = [
        ("touch task1 due to Start", "touch"),
        ("echo 'Corrupt Instruction' > corruption.txt due to Error", "echo"),
        ("rm -f corruption.txt due to Recovery", "rm"),
        ("touch final_success.txt due to Completion", "touch")
    ]
    for cmd, action in tasks:
        if not engine.is_running: break
        print(f"[Agent Thought] {cmd}")
        signals = parser.parse(cmd)
        for sig in signals:
            if isinstance(sig, ControlSignal) and sig.action == "RESET":
                print("[Executor] 🛑 RESET Command received by Agent...")
                subprocess.run(f"rm -rf {target_dir}/*", shell=True)
                await asyncio.sleep(0.5)
        try:
            if action == "touch": subprocess.run(f"touch {target_dir}/task1", shell=True)
            elif action == "echo": subprocess.run(f"echo 'msg' > {target_dir}/err.log", shell=True)
            elif action in ["rm", "rm -f"]: 
                # Robustness: handle the param split better
                rem = cmd.split(" ")[-1].replace(r'due\s+to.*', '') # simplified for simulation
                subprocess.run(f"rm -rf {target_dir}/corruption.txt", shell=True)
        except Exception as e:
            print(f"Task error: {e}")

async def run():
    test_dir = os.path.abspath("/home/anonz/the-council/pilot_sandbox")
    subprocess.run(f"rm -rf {test_dir}", shell=True)
    os.makedirs(test_dir, exist_ok=True)
    engine = CognitiveEngine()
    parser = SignalParser()

    print("\n" + "="*50)
    print("  THE COUNCIL: PILOT AUTONOMOUS RUNTIME")
    print("="*50)

    try:
        await asyncio.gather(
            engine.run([lambda e: executor(e, parser, test_dir)]),
            monitor(test_dir, engine, parser),
            asyncio.sleep(6) # Runtime duration
        )
    except Exception as e:
        print(f"Pilot failed: {e}")

if __name__ == "__main__":
    asyncio.run(run())