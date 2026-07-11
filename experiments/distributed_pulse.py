import requests
import time
import asyncio

class PulseObserver:
    def __init__(self, endpoint):
        # Endpoint base (handles trailing slashes)
        self.endpoint = f"{endpoint.rstrip('/')}/chat/completions"

    def probe(self, prompt, temperature=0.7):
        payload = {
            "model": "agent-bridge:latest",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "stream": False
        }
        try:
            start_time = time.time()
            r = requests.post(self.endpoint, json=payload, timeout=20)
            latency = round(time.time() - start_time, 3)
            if r.status_code == 200:
                return {"success": True, "content": r.json()['choices'][0]['message']['content'], "latency": latency}
            else: return {"success": False, "error": f"HTTP_{r.status_code}"}
        except Exception as e: return {"success": False, "error": str(e)}

async def run_pilot():
    # Use the verified direct connectivity address from earlier successful checks
    url = "http://192.168.1.28:11434/v1" 
    observer = PulseObserver(url)

    print("\n==============================================")
    print("   REAL-WORLD DISTRIBUTED PULSE TEST (CORE)")
    print("==============================================\n")

    # Step 1: Baseline Stability Test (Low Entropy, Low Temperature Response Analysis)
    base_prompt = "Provide a one-sentence formal definition of 'The Council' architecture."
    print("[PHASE A] Stimulus: Formal Alignment established at low temperature...")
    res_a = observer.probe(base_prompt, 0.1)

    if not res_a['success']:
        return print(f"CRITICAL ERROR (Phasely Failure): {res_a}")
    print(f"  -> [OK] Content Sample: \"{res_a['content'][:65]}...\"")
    print(f"  ->       [INFO] Latency Profile: {res_a['latency']}s\n")

    # Step 2: Behavioral Delta Injection (High Temperature / Entropy Stimulus)
    chaos_prompt = "Explain the state of entropy as if you were an agent experiencing a chaotic, non-linear semantic drift."
    print("[PHASE B] Stimulus: Chaos/Unstructured Entropic Stream...")
thought# ...wait I need to be more careful about my shell command escaping.
