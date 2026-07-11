
import asyncio
import json
import os
from datetime import datetime
from src.council.core.governance_controller import GovernanceController

class MissionAlpha:
    def __init__(self, signal_path):
        self.signal_path = signal_path

    async def stimulus(self, interval=5):
        print("[STIMULUS] --- Starting Chaos Loop (3 Iterations) ...")
        for i in range(1, 4):
            await asyncio.sleep(interval)
            event = {
                "timestamp": datetime.now().isoformat(),
                "sender": "Chaos_Stimulus",
                "event": "DRIFT_DETECTED",
                "data": {"e": round(0.8 + (i * 1 / 5), 2)} # Scale drift up over time
            }
            with open(self.signal_path, 'a') as f:
                f.write(json.dumps(event) + "\n")
            print(f"[STIMULUS] Cycle {i}/3 completed for e={event['data']['e']}")

    async def monitor(self):
        await GovernanceController().start(40)

if __name__ == "__main__":
    path = "/home/anonz/projects/the-council/src/council/core/signals.jsonl"
    print("[LAUNCH] Mission Alpha Pilot: Fully Orchestrated Autonomous Loop.")
    asyncio.run(asyncio.gather(MissionAlpha(path).stimulus(), MissionAlpha(path).monitor()))

