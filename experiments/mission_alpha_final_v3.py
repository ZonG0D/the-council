import asyncio
import json
import os
from datetime import datetime

try:
    from src.council.core.governance_controller import GovernanceController
except ImportError:
    class GovernanceController:
        def __init__(self, signal_path=None): pass
        async def start(self, d): print("[RECOVERY] Mock Monitor Running")

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
                "data": {"e": round(0.8 + (i * 0.1), 2)}
            }
            with open(self.signal_path, 'a') as f:
                f.write(json.dumps(event) + "\n")
            print(f"[STIMULUS] Cycle {i}/3 completed for e={round(0.8 + (i * 0.1), 2)}")

    async def monitor(self):
        from src.council.core.governance_controller import GovernanceController
        gc = GovernanceController()
        await gc.start(45)

if __name__ == "__main__":
    path = "/home/anonz/projects/the-council/src/council/core/signals.jsonl"
    print(f"[LAUNCH] Mission Alpha Pilot: {path}")
    asyncio.run(asyncio.gather(MissionAlpha(path).stimulus(), MissionAlpha(path).monitor()))
