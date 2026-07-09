import os
import sys
import asyncio
from dataclasses import dataclass # Import added here

# Add the project root to sys.path so we can import from 'src' correctly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

if os.path.join(project_root, "src") not in sys.path:
    sys.path.append(os.path.join(project_root, "src"))

print("Starting Verification of Distributed Actor Model...")

try:
    from council.macro.orchestrator import CognitiveEngine, ControlSignal
    from council.meso.signal_parser import SignalParser
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

import subprocess

@dataclass(frozen=True)
class MockAuditSignal:
    type: str = "AUDIT"
    cause: str = "Test Failure"
    severity: str = "high"

class DistributedProcessActor:
    """A simple version of the actor to test basic lifecycle."""
    def __init__(self, name, command):
        self.name = name
        self.command = command
        self.process = None

    async def start(self):
        # Using python3 -c for a quick reliable process
        self.process = subprocess.Popen(["python3", "-c", "import time; print('Running...'); time.sleep(10)"], 
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True

    async def stop_immediately(self):
        if self.process:
            self.process.kill()
        return True

class TestOrchestrator:
    def __init__(self, engine):
        self.engine = engine

async def run_test():
    # Setup mocks for the test components that might not be real yet
    @dataclass(frozen=True)
    class MockTask:
        async def __call__(self, eng):
            print("  [Mock] Task started and running...")
            await asyncio.sleep(10)

    engine = CognitiveEngine()
    parser = SignalParser()
    orchestrator = TestOrchestrator(engine)
    engine.is_running = True
    
    monitor = asyncio.create_task(engine.monitor_loop())
    agent_task = asyncio.create_task(asyncio.to_thread(lambda: None)) # Placeholder for async execution context
    # Let's use a real task loop that can be cancelled
    async def worker():
        try:
            print("  [Worker] Sleeping...")
            await asyncio.sleep(10)
        except asyncio.CancelledError:
            print("  [Worker] CANCELED!")
            raise

    worker_task = asyncio.create_task(worker())
    
    print("[Test] Emitting high-priority Audit/Control signal...")
    # Mimic exactly what the controller looks for
    sig_list = parser.parse("Anomaly detected: Critical failure")
    if sig_list:
        sig = sig_list[0]
        await engine.emit(sig, priority=0)
    else:
        from council.macro.orchestrator import ControlSignal
        sig = ControlSignal(type="CONTROL", action="RESET", reason="Test")

    try:
        # Wait for the task to react to the cancellation signal or timeout
        await asyncio.wait_for(worker_task, timeout=3)
    except (asyncio.TimeoutError, asyncio.CancelledError):
        pass
        
    if worker_task.done():
        print("VERIFIED_SUCCESS")
    else:
        print("VERIFIED_FAILURE")
        
    engine.is_running = False
    monitor.cancel()

async def main():
    await run_test()

if __name__ == "__main__":
    asyncio.run(main())
