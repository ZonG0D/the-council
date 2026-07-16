import asyncio
import random

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
    async def act(self, entropy):
        await asyncio.sleep(0.05)
        return f"[{self.name} ({self.role})]: OK (Entropy: {entropy:.2f})"

class CouncilEngine:
    def __init__(self, agents):
        self.agents = agents
        self.entropy = 0.1
    async def step(self, injection=0.0):
        self.entropy += injection
        print(f"\n[CYCLE] Current Entropy: {self.entropy:.2f}")
        tasks = [a.act(self.entropy) for a in self.agents]
        results = await asyncio.gather(*tasks)
        for r in results: print(r)
        return (self.entropy > 0.75)

async def run_simulation():
    print("=== CHAOS STRESS TEST STARTING ===")
    agents = [Agent("Elis", "Align"), Agent("Lyria", "Speak"), Agent("Silas", "Watch")]
    engine = CouncilEngine(agents)
    resets = 0

    for i in range(1, 8):
        print(f"\n--- ROUND {i} ---")
        # Injecting more significant chaos every other round to guarantee a trigger
        injection = random.uniform(0.3, 0.5) if i % 2 == 0 else 0.1
        if injection > 0.2:
            print(f"[CHAOS EVENT] +{injection:.2f} entropy injected")

        reset_needed = await engine.step(injection)
        if reset_needed:
            print("!!! [RECOVERY] RESET TRIGGERED !!!")
            engine.entropy = 0.1
            resets += 1
    
    print("\n=== SIMULATION FINISHED ===")
    print(f"Resets triggered by Chaos: {resets}")

if __name__ == "__main__":
    asyncio.run(run_simulation())
