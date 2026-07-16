import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from council.core import CouncilOrchestrator as EngineClass
from src.council.meta.observer import MetaCognitiveObserver

async def simulate_semantic_drift():
    print("--- STARTING META-COGNITIVE DRIFT TEST ---")
    print("[STEP 1] Initializing the Council and Julian (The Observer)...")
    
    engine = EngineClass()
    observer = MetaCognitiveObserver(observer_id="Test-Julian")

    print("[STEP 2] Simulating high divergence event...")
    divergence_score = 0.85 

    print(f"[STEP 3] Analyzing Divergence Score: {divergence_score}")
    
    will_trigger = observer.trigger_recalibration(divergence_score)

    if will_trigger:
        print("✅ [SUCCESS] Meta-Cognitive Observer correctly detected drift and triggered recalibration.")
        return True
    else:
        print("❌ [FAILURE] Observer failed to trigger recalibration on critical divergence.")
        return False

async def main():
    success = await simulate_semantic_drift()
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())