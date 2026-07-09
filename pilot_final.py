import asyncio
import os
import subprocess
import sys

# Ensure the path is set for imports within the testing environment
sys.path.append('/home/anonz/the-council')

try:
    from council.macro.orchestrator import CognitiveEngine, ControlSignal, AuditSignal
    from logic.signal_parser import SignalParser
except ImportError as e:
    print(f"CRITICAL IMPORT ERROR: {e}")
    sys.exit(1)

class MockAgent:
    """Simulates a real agent running in a loop that responds to shell commands."""
    async def run(self, engine: 'CognitiveEngine'):
        target_name = "mission_file.txt"
        print("[Agent] Starting persistent mission...")
        
        try:
            for i in range(10):  # Long running task
                if not engine.is_running:
                    return
                
                # Performing real work (creating a file)
                with open(target_name, "w") as f:
                    f.write(f"Progress step {i}")
                
                print(f"[Agent] Completed task step {i}")
                await asyncio.sleep(0.5)
            
            print("[Agent] Mission completed successfully.")
        except asyncio.CancelledError:
            print("[Agent] Task was CANCELLED by Council Reset!")
            raise

class OrchestrationPilot:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.engine = CognitiveEngine()
        self.parser = SignalParser()

    async def observe_environment(self):
        """The Sensor Loop monitoring the real filesystem."""
        print(f"[Monitor] Watching: {self.target_dir}")
        # Track the existence of a specific file that is part of our mission
        mission_file = os.path.join(self.target_dir, "mission_file.txt")
        
        while self.engine.is_running:
            await asyncio.sleep(0.5)
            if not os.path.exists(mission_file):
                print(f"[Sensor] ⚠️ DRIFT DETECTED: Mission file {os.path.basename(mission_file)} disappeared!")
                # Turn the observation into a signal
                parsed = self.parser.parse(f"Anomaly detected: File mission_file.txt was deleted")
                if parsed:
                    await self.engine.emit(parsed[0], priority=1)

    async def run(self):
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir, exist_ok=True)

        print("\n" + "="*60)
        print("      THE COUNCIL: INTEGRATED AUTONOMOUS PILOT")
        print("="*60)
        print(f"[System] Target Dir: {self.target_dir}")

        # Launch the three pillars of the runtime concurrently
        try:
            await asyncio.gather(
                self.engine.run([MockAgent().run]), # The Actor (Execution)
                self.observe_environment(),         # The Sensor (Perception)
                self.simulate_external_chaos()      # The Trigger (The "Chaos" Event)
            )
        except Exception as e:
            print(f"Pilot Error: {e}")
            import traceback
            traceback.print_exc()

    async def simulate_external_chaos(self):
        """Simulates an unmodeled event in the real world (Chaos)."""
        await asyncio.sleep(2) # Wait for agent to get into progress
        print("\n[External Event] !!! SPONTANEOUS SYSTEM CORRUPTION !!!")
        # Real-world destructive action (deletion)
        os.system(f"rm {self.target_dir}/mission_file.txt")

if __name__ == "__main__":
    import shutil
    sandbox = "/tmp/council_pilot_sandbox"
    if os.path.exists(sandbox):
        shutil.rmtree(sandbox)
    os.makedirs(sandbox, exist_ok=True)

    pilot = OrchestrationPilot(sandbox)
    asyncio.run(pilot.run())
