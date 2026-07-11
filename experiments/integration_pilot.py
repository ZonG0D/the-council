import asyncio
import time
from src.council.core.probative_interface import ProbativeInterface

class AutonomousIntegrator:
    def __init__(self, endpoint):
        self.interface = ProbativeInterface(endpoint)
        self.system_entropy = 0.1
        self.temperature = 0.7

    async def _execute_step(self, prompt_desc):
        print("[STEP] Stimulus:", prompt_desc)
        # We assume .probe is an async method based on the context of original usage in run_real_pilot
        res = await self.interface.probe(prompt_desc, temperature=0.7) 
        end = time.time()

        if res['success']:
            print(f"  [RESPONSE] (Latency: {round(end-start, 2)}s)")
            return True
        else:
            err = res.get('error', 'Unknown error') if isinstance(res, dict) else "Non-dict response"
            print(f"  [FAILED] Error: {err}")
            return False

    async def run_real_pilot(self):
        """The actual robust execution script."""
        print("\n" + "="*40)
        print("INTEGRATED FEEDBACK LOOP TEST (Live Brain)")
        print("="*40 + "\n")

        # 1. Anchor Phase: Low Temp / High Coherence Prompting
        base_prompt = "Provide a strictly structured, formal response about 'The Council' architecture."
        await self._execute_step(f"Anchor (Low-T=0.2): {base_prompt}")

         # 2. Chaos Injection Phase: Highly Stochastic/Dynamic Stimulus
        chaos_prompt = "Tell me everything you know in a completely unstructured, chaotic stream of consciousness style."
        await self._execute_step(f"Chaos (High-T=1.5): {chaos_prompt}")

         # 3. The 'Self-Correction' Test: Measuring our ability to regain control/low entropy via the next step.
        stabilization_prompt = "Returning to baseline: Provide a formal summary of current semantic structure."
        await self._execute_step(f"Stabilize (Low-T=0.1): {stabilization_prompt}")

if __name__ == "__main__":
    # Note: Connectivity depends on your environment setup for the local Ollama node.
    pi = AutonomousIntegrator("http://192.168.1.28:11434/v1/chat/completions")
    asyncio.run(pi.run_real_pilot())
