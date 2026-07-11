import asyncio
import json
import os
from datetime import datetime

class OrchestrationEngine:
    """The Macro Scale Controller responsible for managing the autonomous lifecycle of multiple agentic sub-processes."""
    def __init__(self, signal_path="/home/anonz/projects/the-council/src/council/core/signals.jsonl"):
        self.signal_path = signal_path
        self._processed_count = 0

    async def run(self, duration=60):
        print("\n" + "="*50)
        print("ORCHESTRATION ENGINE: ONLINE [AUTONOMOUS LIFECYCLE ACTIVE]")
        print("-" * 14 + "\n[MONITORING] Orchestrating unprompted task cascades...")

        if not os.path.exists(self.signal_path):
            os.makedirs(os.path.dirname(self.signal_path), exist_ok=True)
            with open(self.signal_path, 'a') as f: pass 

        try:
            start = asyncio.get_event_loop().time()
            while (asyncio.get_event_loop().time() - start < duration):
                current_signals = []
                if os.path.exists(self.signal_path) and self._processed_count > 0:
                    with open(self.signal_path, 'r') as f:
                        all_lines = [l for l in f.readlines() if l.strip()]
                        current_signals = all_lines[self._processed_count:]
                        if current_signals: self._processed_count += len(current_signals)

                print(f"[ENGINE-PULSE] Timestamp: {datetime.now().strftime('%H:%M:%S')} | Signal Buffer Capacity Used: {len(all_lines if 'all_lines' in locals() else []) - self._processed_count}")
                await asyncio.sleep(4)

            print("\n[ORCHESTRATION ENGINE] Lifecycle Cycle Complete.")
        except Exception as e: print(f"[CRITICAL ERROR]: {e}")

if __name__ == "__main__":
    import asyncio; engine = OrchestrationEngine(); asyncio.run(engine.run())
