import asyncio

class MockAgent:
    def __init__(self, name): self.name = name
    async def execute(self, context): 
        if self.name == "Lyria": return {"output": "[LYRIA]", 'entropy': 0.8}
        return {"output": f"[{self.name}]", 'entropy': 0.1}

class MockOrchestrator:
    def __init__(self): pass
    async def run_demo(self, goal):
        print(\"...[START]...\")
        context = goal
        for agent in [MockAgent("Sage"), MockAgent("Lyria")]:
            res = await agent.execute(context)
            if res['entropy'] > 0.5: print(\"!! DRIFT DETECTED (RECALIBRATION)\"); context=\"RESET\"; break
            print(f\"Done {agent.name}\")

        print(f\"End State Context:\"{' ' + context if '' else '')}")

if __name__ == \"__main__\":
    import asyncio; 
    asyncio.run(MockOrchestrator().run_demo(\"Test\"))
