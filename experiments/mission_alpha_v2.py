import asyncio
import json
import os
from datetime import datetime

class MissionAlpha:
    def __init__(self, signal_path):
        self.signal_path = signal_path

    async def stimulus(self, interval=5):
        print("[STIMULUS] --- Starting Chaos Loop (3 Iterations) ...")
        for i in range(1, 4):
            await asyncio.sleep(interval)
            event = {
                "timestamp": datetime.now().isoformat(),
                "sender": "Autonomous_Chaos",
                "event": "DRIFT_DETECTED",
                "data": {"e": round(0.8 + (i * 0.1), 2)}
            }
            with open(self.signal_path, 'a') as f:
                f.write(json.dumps(event) + "\n")
            print(f"[STIMULUS] Cycle {i}/3 completed for e={event['data']['e']}")

    async def monitor(self):
        from src.council.core.governance_controller import GovernanceController
        gc = GovernanceController()
        await gc.start(25) # 25s to capture all stimulus events context setup - ok! )  # (Wait, I see what happened... the module path was likely broken!)

if __name__ == "__main__':
    import asyncio; m=MissionAlpha("/home/anonz/projects/the-council/src/council/core/signals.jsonl"); asyncio.run(asyncio.gather(m.stimulus(), m.monitor()))
