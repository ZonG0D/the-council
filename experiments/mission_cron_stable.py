import asyncio
import json
import os
from datetime import datetime

class AutonomousCronAgent:
    def __init__(self, path="/home/anonz/projects/the-council/src/council/core/signals.jsonl"):
        self.path = path

    async def run(self):
        print("[CRON] --- Stimulus Cycle Active...")
        try:
            with open(self.path, "a") as f:
                event = {
                    "timestamp": datetime.now().isoformat(), 
                    "sender": "Cron_Agent", 
                    "event": "DRIFT_DETECTED",
                    "data": {"e": 0.85}
                }
                f.write(json.dumps(event) + "\\n")
            print("[CRON] --- Signal Injected.")
        except Exception as e:
            print(f"[ERROR]: {e}")

if __name__ == "__main__":
    import asyncio; agent = AutonomousCronAgent(); asyncio.run(agent.run())