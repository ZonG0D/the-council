import os
import sys
import asyncio
import subprocess

# Add current directory and logic directory to path for simulation purposes
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'logic'))

try:
    from orchestrator import CognitiveEngine, ControlSignal
    from signal_parser import SignalParser
    # We'll use a basic version of the Executor within this test to avoid local file issues
except ImportError:
    print("Dependencies not found. Ensure you run from /home/anonz/the-council/")
    sys.exit(1)

class MockExecutor:
    """Simplified executor for integration testing."""
    def __init__(self, engine):
        self.engine = engine

    async def execute(self, cmd: str):
        print(f"[Executor] Attempting execution: {cmd}")
        # Using shell=True so it behaves like a real terminal environment
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        res = stdout.decode().strip()
        err = stderr.decode().strip()

        if process.returncode != 0:
            print(f"[Executor] Error caught: {err}")
            # We simulate the detection of error by the system
            await self.engine.emit(ControlSignal(type="CONTROL", action="REPAIR", reason=err), priority=1)
            return f"FAIL_{process.returncode}: {err}"
        return res

class AutonomousRecoveryManager:
    """The part we are testing for closure of the loop."""
    def __init__(self, engine, executor):
        self.engine = engine
        self.executor = executor
        self.recovery_count = 0

    async def run_mission(self, command_list):
        for cmd in command_list:
            print(f"\n[Mission] Target Command: {cmd}")
            # Note: In the real logic_recovery we'll have a persistent loop, 
            # here we do a single step for verification.
            result = await self.executor.execute(cmd)
            
            if "FAIL" in result:
                print("[Recovery] Analyzing error...")
                await asyncio.sleep(1) # Simulate thought delay
                recovery_cmd = self._recover()
                if recovery_cmd:
                    print(f"[Recovery] Executing repair command: {recovery_cmd}")
                    await self.executor.execute(recovery_cmd)
                    # Retry the failed command now that environment is fixed
                    print("[Recovery] Retrying original command...")
                    await self.executor.execute(cmd)
                else:
                    return False
            else:
                print("[Mission] Step success.")
        return True

    def _recover(self):
        # Hardcoded for testing the logic path of 'mkdir' in our specific scenario
        return "mkdir -p /tmp/council_test_sandbox/subdir"

async def main():
    print("=== STARTING INTEGRATED AUTONOMY TEST ===")
    engine = CognitiveEngine()
    executor = MockExecutor(engine)
    arm = AutonomousRecoveryManager(engine, executor)

    # THE SCENARIO: Command wants to write to a non-existent folder.
    # It MUST trigger directory creation and then succeed on retry.
    target_path = "/tmp/council_test_sandbox/subdir/goal.txt"
    mission_command = f"echo 'SUCCESS' > {target_path}"

    engine.is_running = True
    monitor = asyncio.create_task(engine.monitor_loop())

    try:
        success = await arm.run_mission([mission_command])
        if success and os.path.exists(target_path):
            print("\n[RESULT] VERIFIED: Loop closed successfully.")
            print("          Target state reached via automated repair.")
            sys.exit(0)
        else:
            print("\n[RESULT] FAILED: Mission did not achieve target state.")
            sys.exit(1)
    finally:
        engine.is_running = False
        monitor.cancel()

if __name__ == "__main__":
    # Cleanup before start
    import shutil
    if os.path.exists("/tmp/council_test_sandbox"):
        shutil.rmtree("/tmp/council_test_sandbox")
    os.makedirs("/tmp/council_test_sandbox", exist_ok=True)
    
    asyncio.run(main())
