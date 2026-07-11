import requests
import time

class ProbativeInterface:
    def __init__(self, endpoint_url):
        """Initialize with target LLM provider URL."""
        self.endpoint = endpoint_url

    def probe(self, prompt, temperature=0.7):
        payload = {
            "model": "agent-bridge:latest",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        try:
            print(f"[PROBE] Sending stimulus to {self.endpoint}")
            response = requests.post(self.endpoint, json=payload, timeout=10)
            if response.status_code == 200:
                return {"success": True, "content": response.json()['choices'][0]['message']['content']}
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("Verifying module load...")
    p = ProbativeInterface("http://192.168.1.28:11434/v1/chat/completions")
    # Mock test (expecting failure if node is unreachable)
    res = p.probe("Hi.")
    print(f"Result of local connectivity check: {res}")
