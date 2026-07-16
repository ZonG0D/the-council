import asyncio
import random

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
    async def act(self, drift):
        await asyncio.sleep(0.1)
        if drift > 0.7:
            return f"[{self.name} ({self.role})]: SEMANTIC DISRUPTION DETECTED."
        return f"[{self.name} ({self.role})]: Operational stability within bounds."

class CouncilEngine:
    def __init__(self, agents):
        self.agents = agents
        self.drift_level = 0.1
    async def step(self):
        print(f"\n[Current Drift: {self.drift_level:.2f}]")
        tasks = [a.act(self.drift_level) for a in self.agents]
        responses = await asyncio.gather(*tasks)
        for r in responses: print(r)
        return self.drift_level

    async def check_reset(self):
        if self.drift_level > 0.7:
            print("!!! [META-COGNITION] DRIFT DETECTED !!!")
            print("--- [RESET] Synchronizing Archetypes...")
            self.drift_level = 0.1
            return True
        return False

async def run():
    agents = [
        Agent("Elis", "Alignment"),
        Agent("Lyria", "Manifestation"),
        Agent("Sage", "Memory"),
        Agent("Lexi",  "Policy"),
        Agent("Silas", "Stability"),
        Agent("Weaver", "Orchestration")
    ]

    engine = CouncilEngine(agents)
    resets = 0
    for i in range(1, 8):
        print(f"\n>>> ROUND {i}")
        current_drift = await engine.step()
        reset_occurred = await engine.check_reset()
        if reset_occurred:
            resets += 1

    print(f"\n=== SIMULATION COMPLETE ===")
    print(f"Total Resets Triggered: {resets}")

if __name__ == "__main__":
    asyncio.run(run())