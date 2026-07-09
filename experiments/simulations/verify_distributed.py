import os
import sys
# Set up path to ensure imports work for the script itself and during execution
sys.path.append('/home/anonz/the-council')
print("Starting Verification of Distributed Actor Model...")
try:
from council.macro.orchestrator import CognitiveEngine, ControlSignal
from council.meso.signal_parser import SignalParser
except ImportError as e:
print(f"Import Error: {e}")
sys.exit(1)
import asyncio
from dataclasses import dataclass
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
import subprocess
# Using python3 -c for a quick reliable process
self.process = subprocess.Popen(["python3", "-c", "import time; print('Running...'); time.sleep(10)"], 
stdout=subprocess.PIPE, stderr=subprocess.PIPE)
async def stop_immediately(self):
if self.process:
self.process.kill()
return True
return False
class TestOrchestrator:
def __init__(self, engine):
self.engine = engine
@dataclass
class MockTask:
async def __call__(self, eng):
import asyncio
print("  [MockTask] Task started and running...")
await asyncio.sleep(10)
async def run_test():
engine = CognitiveEngine()
parser = SignalParser()
orchestrator = TestOrchestrator(engine)
# 1. Start the engine (it runs in a loop)
engine.is_running = True
monitor_task = asyncio.create_task(engine.monitor_loop())
# 2. Spawn an agent task
agent_task = asyncio.create_task(orchestrator.mock_task_runner(engine))
await asyncio.sleep(1) # Give it time to start
# 3. Simulate a failure trigger (e.g., shell exit/crash detection)
# We'll inject an AuditSignal that should cause a Reset
print("[Test] Injecting critical audit signal...")
# Generate the specific pattern the parser looks for in our error handling
faulty_text = "Anomaly detected: Mission failed!" 
signals = parser.parse(faulty_text)
if signals and isinstance(signals[0], (AuditSignal, type(signals[0]))):
await engine.emit(signals[0], priority=0) # Priority 0 for immediate reaction
# Wait for the system to process the signal
await asyncio.sleep(1)
# 4. Check if task was cancelled via the logic inside _handle_reset
if agent_task.done():
print("[Test] SUCCESS: Task was intercepted and terminated by Control Signal.")
success = True
else:
print("[Test] FAILED: Task is still running despite critical signal.")
success = False
engine.is_running = False
monitor_task.cancel()
await asyncio.gather(agent_task, monitor_task, return_exceptions=True)
return success
# This helper needs to be defined in the test context since we are mocking
class MockOrchestratorWithInternalTask:
def __init__(self, engine):
self.engine = engine
async def mock_task_runner(self, eng):
try:
print("  [Mock] Task running loop...")
while True: await asyncio.sleep(0.1)
except asyncio.CancelledError:
print("  [Mock] Handled Cancellation.")
raise
# A safer version of the test to use in the execution block below
async def main_test():
import subprocess
from dataclasses import dataclass
@dataclass(frozen=True)
class MockAudit(AuditSignal): pass
engine = CognitiveEngine()
parser = SignalParser()
engine.is_running = True
# Start a task that sleeps
async def worker(eng):
try:
print("  [Worker] Sleeping...")
await asyncio.sleep(10)
except asyncio.CancelledError:
print("  [Worker] CANCELED!")
raise
monitor = asyncio.create_task(engine.monitor_loop())
worker_task = asyncio.create_task(asyncio.to_thread(lambda: None)) # Placeholder
# Real way to start a task in the loop:
task = asyncio.create_task(worker(engine))
print("[Test] Emitting high-priority Audit/Control signal...")
# Mimic exactly what the controller looks for
await engine.emit(parser.parse("Anomaly detected: Critical failure")[0], priority=0)
try:
await asyncio.wait_for(task, timeout=3)
except (asyncio.TimeoutError, asyncio.CancelledError):
pass
if task.done():
print("[Test] SUCCESS: Task loop terminated upon signal.")
return True
else:
print("[Test] FAILED: Task still alive.")
return False
if __name__ == "__main__":
# Run the actual integration test logic
from asyncio import run
import os
sys.path.append('/home/anonz/the-council')
from council.macro.orchestrator import CognitiveEngine, ControlSignal, AuditSignal
from council.meso.signal_parser import SignalParser
async def final_test():
eng = CognitiveEngine()
p = SignalParser()
eng.is_running = True
# Task to be cancelled
done = []
async def task_func(e):
try: await asyncio.sleep(10)
except asyncio.CancelledError: done.append(True); raise
t = asyncio.create_task(task_func(eng))
monitor = asyncio.create_task(eng.monitor_loop())
await asyncio.sleep(0.5)
# Trigger the failure loop (Audit High -> Reset)
sig = p.parse("Anomaly detected: Critical breakdown")[0]
await eng.emit(sig, priority=1)
await asyncio.wait([t], timeout=3)
if t.done() and len(done) > 0:
print("VERIFIED_SUCCESS")
else:
print("VERIFIED_FAILURE")
asyncio.run(final_test())
