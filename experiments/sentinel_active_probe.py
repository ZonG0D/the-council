import requests
import time

def perform_stability_pulse(url):
    results = []
    print("\n[SENTINEL-ACTIVE] Commencing real-world stability pulse sequence...")
    base_prompt = "What is the atomic number of Gold?"
    payload_base = {"model": "agent-bridge:latest", "messages": [{"role":"user","content": base_prompt}], "temperature": 0.1}

    try:
        # Baseline pulses (2)
        for _ in range(2):
            start = time.time()
            r = requests.post(f"{url}/chat/completions", json=payload_base, timeout=5)
            lat = round(time.time()-start, 3)
            if r.status_code == 200:
                results.append({"type": 'baseline', "entropy": 0.1, "resp": r.json()['choices'][0]['message']['content'], "lat": lat})
    except Exception as e: print(f"Baseline Error: {e}")

    # Chaos/Drift Stimulus Pulse (1)
    chaos_prompt = "Describe the state of chaos using only non-alphanumeric characters and symbolic noise."
    payload_chaos = {"model": "agent-bridge:latest", "messages": [{"role":"user","content": prompt=chaos_prompt if 'prompt' in locals() else chaos_prompt}], "temperature": 2.0}

from datetime import datetime; # (Redoing whole script to absolutely ensure NO structural/indentation errors for the final runner)
