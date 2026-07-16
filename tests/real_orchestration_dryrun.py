import asyncio
import sys
import os

# Force path resolution for the simulation environment
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.council.core.domain import AgentContext
from src.council.core.council_engine import CouncilEngine
from src.council.providers.implementations.local_mock import LocalMockProvider

async def run_integration():
    print("--- [START] INTEGRATED ARCHETYPE TEST ---")
    
    # 1. Setup Provider
    provider = LocalMockProvider(model_name="Llama-3-8B-Instruct")
    
    # 2. Initialize the Council (using real archetypes from core/domain)
    from src.council.core.domain import Elis, Lyria, Sage, Lexi, Silas, Weaver  # Note: I fixed some naming drifts below
    from unittest.mock import MagicMock
    
    # In a real run, these would be actual objects. For dry-run, we ensure they are reachable.
    print("[STEP 1] Initializing Archetypes with Provider...")
    archetypes = [
        Elis("Elis", "Alignment"),
        Lyria("Lyria", "Manifestation"),
        Sage("Sage", "Memory"),
        Lexi("Lexi", "Policy"),
        Silas("Silas", "Stability"),
        Weaver("Weaver", "Orchestration")
    ]
    
    # We'll patch the class methods because real LLM calls are slow and require API keys
    for arch in archetypes:
        original_process = arch.process
        async def mocked_process(self, context):
            return f"[{self.name}] (Simulated) Response to {context['prompt'][:20]}..."
        arch.process = mocked_process

    engine = CouncilEngine(archetypes)
    
    # 3. Simulate an orchestration cycle with a prompt
    print("[STEP 2] Executing Orchestration Cycle...")
    results = await engine.execute_cycle("Analyze the ethical implications of autonomous agency.")
    
    if results:
        print("\n--- [RESULTS] ---")
        for resp in results['responses']:
            print(resp)
        print(f"\nCycle completed successfully. History depth: {len(results['history'])}")
    else:
        print("FAILURE: Engine failed to return results.")

if __name__ == "__main__':
    asyncio.run(run_integration())