from typing import List, Dict
from dataclasses import dataclass, field
import asyncio

@dataclass(frozen=True)
class CouncilSignal:
    scale: str 
    archetype: str 
    event_type: str # 'ENTROPY_SPIKE', 'VIOLATION', etc.
    magnitude: float = 1.0
    metadata: dict = field(default_factory=dict)

class SignalBus:
    def __init__(self):
        self._subscribers: Dict[str, List] = {}
        self._wildcard_listeners: List = []

    async def publish(self, signal: CouncilSignal):
        print(f"[SIGNAL BUS] {signal.scale.upper()} | {signal.archetype} -> {signal.event_type}")
        # 1. Specific event dispatching (asynchronous)
        if signal.event_type in self._subscribers:
            for cb in self._subscribers[signal.event_type]:
                asyncio.create_task(cb(signal))

        # 2. Wildcard/Global-stream monitoring
        for cb in self._wildcard_listeners:
            asyncio.create_task(cb(signal))

    def subscribe(self, event_type: str, callback):
        if event_type == "*":
            self._wildcard_listeners.append(callback)
        else:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)

# --- INTEGRITY TEST ---
async def run_test():
    print("Running SignalBus Integrity Test...")
    bus = SignalBus()
    captured_signals = []

    async def capture_signal(sig: CouncilSignal):
        captured_signals.append(sig)

    bus.subscribe("*", capture_signal)
    await bus.publish(CouncilSignal("meso", "Silas", "DRIFT"))
    await asyncio.sleep(0.1)  # allow task queue to resolve

    if len(captured_signals) > 0:
        print("✓ Success: Captured signal from wildcard sub.")
        assert captured_signals[0].archetype == "Silas"
    else:
        raise Exception("FAIL: No signals caught by wildcard listener.")
    
    # Test specific trigger logic
    bus.subscribe("DRIFT", lambda s: print(f"  - Specific Subscriber Caught {s.scale} drift!"))
    await bus.publish(CouncilSignal("macro", "Lexus", "DRIFT"))
    await asyncio.sleep(0.1)

if __name__ == "__main__":
    import asyncio; 
    asyncio.run(run_test())
