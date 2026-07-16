import asyncio
import sys
import os

# Set up path so we can import our own modules correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    import council.core.signal_bus as bus_mod
    from src.council.meta.observer import MetaCognitiveObserver
    print("--- LOGIC VALIDATION SUCCESSFUL: All modules imported ---")
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    sys.exit(1)

async def run_integration():
    print("\n[START] INTEGRATION TEST: SIGNAL PROPAGATION")
    
    # 1. Setup the components in memory
    observer = MetaCognitiveObserver()
    bus = bus_mod.bus
    
    # 2. Wire up the Observer to the Bus (Manual wiring for test)
    print("[SETUP] Wiring Observer -> SignalBus...")
    bus.subscribe("DRIFT_DETECTED", observer.on_drift_event)

    # 3. Trigger a Drift Event through the Bus (Simulating the Core detecting drift)
    test_score = 0.85
    print(f"[ACTION] Emitting DRIFT_DETECTED event with score: {test_score}")
    await bus.emit("DRIFT_DETECTED", {"score": test_score})

    # 4. Verification of the observer's reaction (The callback)
    # In a real async system, we might need a tiny sleep to allow task scheduling
    await asyncio.sleep(0.1)
    print("[VERIFICATION] Check if 'Observer caught signal' appeared in output.")

if __name__ == "__main__":
    asyncio.run(run_integration())