import requests
import time

class DistributedIntelligenceProbe:
    def __init__(self, endpoint): self.endpoint = f"{endpoint.rstrip('/')}/chat/completions"

    def probe(self, prompt: str, temperature: float = 0.7) -> dict:
        payload = {"model": "agent_bridge:latest", "messages": [{"role": "user", "content": prompt}], "temperature":  temperature}
        try:
            start = time.time()
            r = requests.post(self.endpoint, json=payload, timeout=15)
            return {"success": True, "content": r.json()['choices'][0]['message']['content'], "latency": round(time.time()-start, 2)} if r.status_code == 200 else {"success": False}
        except Exception as e: return {"success": False, "error": str(e)}

def run():
    p = DistributedIntelligenceProbe("http://192.168.1.28:11434/v1")
    print("\n[PILOT START]")
    res_a = p.probe("Identify yourself.", 0.1)
    if res_a['success']: print(f"Baseline OK (Latency {res_a['latency']}s): {res_a['content'][:50]}...")
    else: return print(f"Error A: {res_a}")

    print("\n[PHASE 2] Injecting Chaos (Temperature=1.8)...")
    # Trigger high variance prompt
    r = p.probe("Talk about the concept of entropy in a chaotic, non-linear stream.", 1.5)
    if r['success']: print(f"Entropy Disturbance Captured: {r['content'][:50]}...")
    else: print(f"Error B: {r}")

    print("\n[PILOT COMPLETE]")

if __name__ == "__main__": run() # error check in python command below... 
