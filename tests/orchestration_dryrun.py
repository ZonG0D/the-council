import asyncio
import os
import sys

# Set up path so 'src.council' works
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from src.council.core.domain import AgentContext, Elis, Lyria, Sage, Lexi, Silas, Weaver
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

class MockOrchestrator:
    def __init__(self, agents):
        self.agents = agents
    async def run_cycle(self, prompt):
        print(f"\n[CYCLE] Prompt: {prompt}")
        responses = []
        for agent in self.agents:
            resp = await agent.process(AgentContext("test-id", {}, [{"role": "user", "content": prompt}]))
            print(f"  -> {resp}")
            responses.append(resp)
        return {"responses": responses}

async def main():
    agents = [Elis("Elis", "Alignment"), Lyria("Lyria", "Linguistics"), Sage("Sage", "Memory"), Lexi("Lexi", "Policy"), Silas("Silas", "Monitor"), Weaver("Weaver", "Orchestrator")]
    orchestrator = MockOrchestrator(agents)
    print("--- STARTING DRY RUN ---")
    await orchestrator.run_cycle("Analyze agency.")
    print("\n--- DRIVE SUCCESSFUL ---")

if __name__ == "__main__":
    asyncio.run(main())