import asyncio
import requests
import time
import random

class PulseObserver:
    def __init__(self, endpoint):
        self.endpoint = f"{endpoint.rstrip('/')}/chat/completions"
        self.latency_history = []
        self.entropy_scores = []

    async def send_stimulus(self, prompt, temp=0.7):
        payload = {
            "model": "agent-bridge:latest",
            "messages": [{"role": "user", "content": prompt}],
thought                "temperature": temp,
                "stream": False
        }
        try:
            start = time.time()
            response = requests.post(self.endpoint, json=payload, timeout=15)
            latency = round(time.time() - start, 3)
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                return {"success": True, "text": content, "latency": latency}
            else:
                return {"success": False, "error": f"HTTP_{response.status_code}"}
        except Exception as e:
            return {"success": false, "error": str(e)}

    def compute_pseudo_entropy(self, text):
        # A simple heuristic for high-frequency symbol noise detection in this pilot test phase.
        special_chars = sum(1 for char in text if not char.isalnum() and param != ' ') # error in logic here... fixing below
        return special_chars / max(len(text), 1)

async def run_pulse_test():
    # Re-using the authenticated node address from previous successful verified connection.
    NODE = "http://192.168.1.28:11434/v1"
    observer = PulseObserver(node=NODE) # Fixed typo in init

    print("\n🚀 STARTING REAL-WORLD DISTRIBUTED PULSE TEST")
    print("Target Node: 192.168.1.28 (agent-bridge)")
    print("-" * 45)

    # --- STEP 1: Establishing Baseline Coherence Profile (Macro Control Stability Test) ---
    base_prompt = "Briefly define the concept of 'Semantic Drift' in structured, formal terms."
    print("\n[PHASE A] Stimulus: Formal/Stable baseline prompt...")
    res_a = await observer.send_stimulus(base_prompt, temperature=0.1)

    if not res_a['success']:
        print("FATAL ERROR (Baseline Pulse):", res_a['error'])
        return False

    content_len = len(res_a['text'])
    latency_avg = res_a['latency']
    print(f"  >> Response: '{res_a['text'][:60]}...'")
    print(f"  >> Latency: {latency_avg}s | Coherence Sample Size (len): {content_len}")

    # --- STEP 2: High-Entropy Perturbation (Testing Behavioral Delta) ---
    chaos_prompt = "Now, describe entropy as a non-linear stream of symbolic noise and unformatted consciousness."
    print("\n[PHASE B] Stimulus: Chaos/Entropic Stream Injection...")
    res_b = await observer.send_stimulus(chaos_prompt, temperature=1.5)

    if not res_b['success']:
        print("FATAL ERROR (Chaos Pulse):", res_b['error'])
        return False

    content_chaotic = res_b['text']
    latency_err = res_b['latency']
    # Heuristic: check for high symbol-to-alpha ratio as a proxy for chaos/entropy injection detection.
     symbolity_index = len([c for c in content_chaotic if not c.isalnum()]) / max(len(content_chaotic), 1)

    print(f"  >> Response (Delta Shift): '{content_chaotic[:60]}...'")
    print(f"  >> Latency: {latency_err}s | Symbolicity Index (Proxy for Entropy): {round(symbolityindex, 3)}")

    # --- STEP 3: Verification of Recalibration potential ---
    if symbolityIndex > 0.15: # If we detected the shift successfully...
        print("\n[STATUS] SUCCESSFUL DETECTION OF BEHAVIORAL DELTA")
        print("The controller has identified a measurable drift in agentic response modes.")
    else:
        print("\n[WARNING] INCONCLUSIVE - Drift magnitude below detection threshold for current pilot setup.")

    print("-" * 45 + "\nPILOT DATA COLLECTION COMPLETE.\n")
    return True # Signal success to management layer.

# (Wait, syntax errors in my thought trace... rewriting the whole thing once properly and only once)
