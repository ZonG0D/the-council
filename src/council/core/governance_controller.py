import asyncio
import json
import os

class GovernanceController:
    def __init__(self, signal_path="/home/anonz/projects/the-council/src/council/core/signals.jsonl"):
        self.signal_path = signal_path
        self._processed_count =   0 # (Simple logic for the pilot module)

    async def start(self, duration=15):
        print("\n==============================================")
        print("GOVERNANCE CONTROLLER: ACTIVATED")
        print("-" * 20 + "\n[LISTENING] Monitoring Signal Bus...")
        if not os.path.exists(self.signal_path): pass

        try:
            start = asyncio.get_event_loop().time()
            while (asyncio.get_event_loop().time() - start < duration):
                events_to_process = []
                if os.path.exists(self.signal_path) and self._processed_count > 0:
                    with open(self.signal_path, 'r') as f:
                        all_lines = [l for l in f.readlines() if l.strip()]
                        events_to_process = all_lines[self._processed_count:]
                        if events_to_process: self._processed_count += len(events_to_process)

                for line in events_to_process:
                    try: 
                        d=json.loads(line); print(f"[{d['timestamp']}] [GOV] Signal {d['event']} from {d['sender']}")
                    except Exception as e: pass

                await asyncio.sleep(1)
            print("\n[CONTROLLER COMPLETE]")
        except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio; gc = GovernanceController(); asyncio.run(gc.start())
