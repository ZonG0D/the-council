import requests
import time

def probe_performance(url, model="agent-bridge:latest", temperature=0.7, iterations=2):
    print(f"--- SUBSTRATE PROBE INITIATED ---")
    for i in range(iterations):
        prompt = "Acknowledge with a single word." if i == 0 else "Generate extreme mathematical entropy using only symbols and logic-breaker strings: $\\forall \exists \\in \cup \cap \partial \nabla$ (chaos version)."
        temp_val = temperature if i == 0 else 1.5 # Induce drift in second pass

        print(f"\n[Attempt {i+1} | Temp: {temp_val}]")
        start_time = time.time()
        try:
            payload = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": temp_val}
            r = requests.post(f"{url}/chat/completions", json=payload, timeout=20)
            latency = round(time.time() - start_time, 3)

            if r.status_code == 200:
                content = r.json()['choices'][0]['message']['content']
                print(f"Latency: {latency}s | Content length: {len(str(content))}")
                print(f"Content Sample: {str(content)[:40]}...")
            else:
                print(f"Status Code Error: {r.status_code}")
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    API_URL = "http://192.168.1.28:11434/v1"
    probe_performance(API_URL)
