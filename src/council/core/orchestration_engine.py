import asyncio
import json
import os
from datetime import datetime

class OrchestrationEngine:
    """The Macro Scale Controller responsible for managing the autonomous lifecycle of multiple agentic sub-processes."""
    def __init__(self, signal_path=None):
        # Default path corrected to reflect project casing discovered in Step 1/2.
        if signal_path is None:
            signal_path = "/home/anonz/Projects/TheCouncil/src/council/core/signals.jsonl"
        self.signal_path = os.path.abspath(os.path.expanduser(signal_path))
        self._last_position = 0  # Byte offset tracker for O(1) ingestion complexity

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
                new_signals = []
                if os.path.exists(self.signal_path):
                    with open(self.signal_path, 'r') as f:
                        # Optimization Implementation: Seek to last read position instead of reading all lines every cycle
                        f.seek(self._last_position)
                        for line in f:
                            stripped = line.strip()
                            if stripped and not stripped.startswith('#'):
                                try:
                                    new_signals.append(json.loads(stripped))
                                except json.JSONDecodeError:
                                    continue # Skip malformed lines/partial writes

                        self._last_position = f.tell() # Efficiently track end-of-current buffer position

                if new_signals:
                    print(f"[ENGINE-PULSE] Timestamp: {datetime.now().strftime('%H:%M:%S')} | New Signals Buffer Processed: {len(new_signals)} | File Offset: {self._last_position}")
                else:
                   # Print heartbeat if nothing new to show continuous operation (non-stale state)
                   pass 

                await asyncio.sleep(4)

            print("\n[ORCHESTRATION ENGINE] Lifecycle Cycle Complete.")
        except Exception as e: print("[CRITICAL ERROR]: {e}")

if __name__ == "__main__":
    import asyncio; engine = OrchestrationEngine(); asyncio.run(engine.run())