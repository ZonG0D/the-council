import sys
import os
import asyncio
import numpy as np

# Setup path so imports work correctly
sys.path.append(os.path.abspath("/home/anonz/projects/the-council"))

from src.council.meso.drift_monitor import DriftMonitor
from src.council.macro.control_runner import ControlRunner

class MockEngine:
    async def emit(self, signal, priority=1): 
        print(f"  -> [Signal Received] Priority:{priority} Action:{getattr(signal, 'action', 'N/A')}")

async def run_test():
    dm = DriftMonitor(threshold=0.2)
    engine = MockEngine()
    cr = ControlRunner(engine, dm)
    
    print("Starting simulation for 50 steps...")
    await cr.run_loop(lambda x: None, [1.0, 0.0, 0.0], iterations=50)

if __name__ == "__main__":
    asyncio.run(run_test())
