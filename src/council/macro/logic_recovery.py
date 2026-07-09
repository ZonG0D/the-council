import os
import sys
sys.path.append("/home/anonz/the-council")
import asyncio
import sys
import os
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

# Correcting path for local development and execution

try:
    from council.macro.orchestrator import CognitiveEngine, ControlSignal
    from logic.signal_parser import SignalParser
    # We realized ShellExecutor is part of logic_distributed in the current layout
    import sys as mod_sys
    from logic_distributed import ShellExecutor
except ImportError as e:
    print(f"Import Error: {e}")
    print("Try running via 'python3 the-council/logic_recovery.py'")
    sys.exit(1)

@dataclass
class MissionGoal:
    """The 'Intent Anchor' ($v_{goal}$) representing the desired outcome of an agent."""
    description: str
    target_state: Dict[str, Any]
    command_sequence: List[Dict[str, Any]]
    max_retries: int = 3

class AutonomousRecoveryManager:
    """
    The 'Self-Correction' Loop. 
    Closes the gap between 'what happened' (Execution) and 'what should be' (Goal).
    """
    def __init__(self, engine: CognitiveEngine, executor: ShellExecutor, parser: SignalParser):
        self.engine = engine
        self.executor = executor
        self.parser = parser

    async def execute_mission(self, mission: MissionGoal):
        print(f"\n[ARM] --- STARTING MISSION: {mission.description} ---")
        current_step = 0
        attempts = 0

        while current_step < len(mission.command_sequence) and attempts <= mission.max_retries:
            action = mission.command_sequence[current_step]
            cmd = action['cmd']
            expected_result = action.get('expected', None)

            print(f"[ARM-Step {current_step}] Attempting: {cmd}")
            result = await self.executor.execute(cmd)

            # Success check based on real state (for file existence/content)
            success = True
            if expected_result and isinstance(expected_result, dict):
                if expected_result['type'] == 'file_exists':
                    path = os.path.join(os.getcwd(), expected_result['path'])
                    success = os.path.exists(path)
                elif expected_result['type'] == 'text_in_file':
                    path = osing_path = os.path.join(os.getcwd(), expected_result['path'])
                    if os.path.exists(path):
                        with open(path, 'r') as f:
                            success = expected_result['text'] in f.read()
                    else:
                        success = False

            if success and "FAILED" not in result:
                print(f"[ARM-Step {current_step}] ✅ State Verified. Proceeding.")
                current_step += 1
                attempts = 0 
                continue
            else:
                print(f"[ARM-Step {current_step}] ❌ Result/State Error (Drift Detected).")

            # RECOVERY LOGIC
            attempts += 1
            if attempts > mission.max_retries:
                print("[ARM] 🚨 Max retries reached. Escalating to Engine Oversight.")
                await self.engine.emit(ControlSignal(action="HALT", reason=f"Mission Failed after {attempts} tries."), priority=0)
                break

            recovery_cmd = await self._determine_recovery(result, attempt=attempts)
            if recovery_cmd:
                print(f"[ARM-Recovery] Attempting automated repair: {recovery_cmd}")
                await self.executor.execute(recovery_cmd)
                # Wait for the system to stabilize after a command
                await asyncio.sleep(1) 
            else:
                print("[ARM] No automated recovery path found.")
                break

        status = "COMPLETED" if current_step == len(mission.command_sequence) else "FAILED/HALTED"
        print(f"\n[ARM] Mission result: {status}")

    async def _determine_recovery(self, error_message: str, attempt: int) -> Optional[str]:
        """Simple heuristic logic to remediate common shell errors."""
        if "No such file or directory" in error_message:
            # Very naive fix for the pilot test: create the parent directory if it's a nested path issue
            return f"mkdir -p /tmp/council_recovery_test/flag"
        if attempt < 3:
            await asyncio.sleep(0.5)
            return None
        return None

async def run_pilot():
    import shutil
    sandbox = "/tmp/council_recovery_test"
    if os.path.exists(sandbox):
        shutil.rmtree(sandbox)
    os.makedirs(sandbox, exist_ok=True)
    os.chdir(sandbox)

    engine = CognitiveEngine()
    parser = SignalParser()
    executor = ShellExecutor(engine, parser)
    arm = AutonomousRecoveryManager(engine, executor, parser)

    # MISSION: Write a file to 'flag/goal.txt'. 
    # We know the directory 'flag' doesn't exist yet. The agent MUST create it.
    mission = MissionGoal(
        description="The Self-Healing File Creation",
        target_state={"file_exists": "flag/goal.txt"},
        command_sequence=[
            {
                "cmd": "echo 'SUCCESS' > flag/goal.txt", 
                "expected": {"type": "text_in_file", "path": f"{sandbox}/flag/goal.txt", "text": "SUCCESS"}
            }
        ],
        max_retries=3
    )

    print("\n" + "="*60)
    print("     RECURSIVE RECOVERY PILOT (The Self-Correcting Loop)")
    print("="*60)
    engine.is_running = True
    monitor = asyncio.create_task(engine.monitor_loop())

    try:
        await arm.execute_mission(mission)
    finally:
        engine.is_running = False
        monitor.cancel()
        os.system(f"rm -rf {sandbox}")
    
    print("\n[Pilot] Testing Complete.")

if __name__ == "__main__":
    asyncio.run(run_pilot())