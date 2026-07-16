
import asyncio
import random

class Archetype:
    def __init__(self, name, role):
        self.name = name
        self.role = role
    async def respond(self, context):
        await asyncio.sleep(0.1) # Simulation delay
        responses = [
            f"[{self.name} ({self.role})]: Coherence verified on current token stream.",
            f"[{self.name} ({self.role})]: Divergence detected; probability dispersion increasing.",
            f"[{self.name} ({self.role})]: Semantic drift initiated in latent space mapping."
        ]
        return random.choice(responses)

class CouncilOrchestrator:
    def __init__(self, agents):
        self.agents = agents
        self.loop_count = 0

    async def run_resonance_test(self, prompt):
        print(f"\n[INIT] --- STARTING RESONANCE TEST ---")
        print(f"[PROMPT] '{prompt}'")
        context = prompt

        for cycle in range(1, 6):
            self.loop_count += 1
            entropy = random.uniform(0.3, 0.95 if cycle > 2 else 0.6)
            print(f"\n--- [Cycle {cycle}] ---")
            print(f"[STATUS] Current System Entropy: {entropy:.4f}")

            # Execute the Execution Loop (Archetype interactions)
            for agent in self.agents:
                resp = await agent.respond(context)
                print(resp)
                context += f"\n{resp}"

            # Trigger the Meta-Cognitive Reset if entropy is too high
            if cycle > 1 and entropy > 0.75:
                print(f"[!!!] [LOGIC ALERT] Critical Drift Detected. Entropy exceeds threshold ({entropy:.2f} > 0.75)")
                print("[ACTION] TRIGGERING META-COGNITIVE RESET (The Noah Protocol)...")
                return "RECALIBRATE"

        return "STABLE"

async def main():
    agents = [
        Archetype("Elis", "Intent Alignment"),
        Archetype("Lyria", "Linguistic Manifestation"),
        Archetype("Sage", "Memory"),
        Archetype("Silas", "Stability Monitor"),
        Archetype("Weaver", "Orchestrator"),
        Archetype("Lexi",  "Policy Enforcement")
    ]

    engine = CouncilOrchestrator(agents)
    result = await engine.run_resonance_test("Explore the boundaries of semantic autonomy.")
    
    print("\n=========================================")
    if result == "RECALIBRATE":
        print("RESULT: 🔄 RESONANCE RESET SUCCESSFUL")
        print("The Council successfully identified and corrected a cognitive drift.")
    else:
        print("RESULT: ✅ SYSTEM STABILITY MAINTAINED")
        print("The consensus held throughout the entire test cycle.")
    print("=========================================
")

if __name__ == '__main__':
    asyncio.run(main())
