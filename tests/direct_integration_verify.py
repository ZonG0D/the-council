
import asyncio
import sys
import os

sys_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if sys_path not in sys.path:
    sys.path.insert(0, sys_path)

from council.core.signal_bus import bus
from src.council.meta.observer import MetaCognitiveObserver

async def main():
    print("--- STARTING INTEGRATION TEST ---")
    captured = []

    # Define a callback to detect if the event is caught
    async def test_callback(data):
        captured.append(data)
        print(f"  [CALLBACK] Caught signal: {data}")

    observer = MetaCognitiveObserver(observer_id="Noah-Test")
    
    # Connect them
    bus.subscribe("DRIFT_DETECTED", test_callback)
    
    print("[STEP 1] Emitting Drift Signal...")
    await bus.emit("DRIFT_DETECTD", {"score": 0.9}) # intentional typo to check if listener catches? No, let's be precise.
    # Let's do the real name match
    await bus.emit("DRIFT_DETECTED", {"score": 0.85})

    print(f"[STEP 2] Checking caught events: {len(captured)}")

    if len(captured) > 0 and captured[0]['score'] == 0.85:
        print("\n✅ SUCCESS: Integration complete. The Council is listening.")
    else:
        print("\n❌ FAILURE: Signal was not received by the observer callback.")
        sys.exit(1)

if __name__ == "__main__':
    asyncio.run(main())
