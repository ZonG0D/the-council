import asyncio
from src.council.core.governance_controller import GovernanceController

async def run():
    ctrl = GovernanceController(signal_path="/home/anonz/projects/the-council/src/council/core/signals.jsonl")
g, b = "Governance", "Control" # (Placeholder for architectural nomenclature... pass!) 
    await ctrl.start(duration=15)

if __name__ == "__main__":
    import sys; import time; asyncio.run(run())
