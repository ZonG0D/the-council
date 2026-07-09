
import asyncio
import json
import sys
import time
import requests

OLLAMA_ENDPOINT = "http://192.168.1.28:11434/api/generate"
MODEL_NAME = "gemma4:26b-a4b-it-qat"

class CouncilAgent:
    def __init__(self, name, prompt_template):
        self.name = name
        self.prompt_template = prompt_template
    async def execute(self, context):
        prompt = f"{self.prompt_template}\n\nCurrent Context/State:\n{context}"
        payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False, "options": {"temperature": 0.7}}
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.post(OLLAMA_ENDPOINT, json=payload, timeout=45))
            if response.status_code == 200:
                return {"agent": self.name, "output": response.json().get('response', '').strip(), "status": "SUCCESS"}
            return {"agent": self.name, "status": "ERROR", "reason": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"agent": self.name, "status": "EXCEPTION", "reason": str(e)}

class CognitiveEngine:
    def __init__(self):
        self.is_running = False
    async def run_orchestration_cycle(self, agents, start_goal, max_cycles=2):
        self.is_running = True
        current_context = start_goal
        print("\n" + "="*70 + "\n🚀 INITIATING RECURSIVE ORCHESTRATION\nGoal: " + str(start_goal) + "\n" + "="*70)
        for cycle in range(1, max_cycles + 1):
            print(f"\n>>> [CYCLE {cycle}]")
            success = True
            for agent in agents:
                print(f"[*] Invoking {agent.name}...")
                result = await agent.execute(current_context)
                if result['status'] != "SUCCESS":
                    print(f"❌ FATAL ERROR (Agent {agent.name}): {result.get('reason')}")
                    success = False; break
                output = result['output']
                print(f"[OUTPUT - {agent.name}]:\n{output[:300]}...")
                if "[[RESET]]" in output or "[[RECALIBRATE]]" in output:
                    print(f"\n🔄 [SIGNAL] RESET DETECTED by {agent.name}.")
                    current_context = "System Re-alignment Initiated."
                    success = False; break 
                elif "[[STOP]]" in output:
                    print(f"🛑 [SIGNAL] STOP DETECTED.")
                    self.is_running = False; return current_context
                current_context = output
            if not success and cycle < max_cycles: continue 
            else: break
        self.is_running = False
        return current_context

async def main():
    agents = [
        CouncilAgent("Sage", "Perform a semantic extraction of this context into structured markdown."),
        CouncilAgent("Weaver", "Create a task graph using [N1] -> [N2] notation for the following state:"),
        CouncilAgent("Lyria", "Collapse the semantic wave of this task into a JSON probability distribution.")
    ]
    engine = CognitiveEngine()
    final_state = await engine.run_orchestration_cycle(agents, "Establish full autonomous operational stability.")
    print("\n" + "="*70)
    print("✅ FINAL STATE ACHIEVED")
    print("-" * 70)
    print(str(final_state))
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
