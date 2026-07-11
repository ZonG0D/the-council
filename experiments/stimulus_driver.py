import json
from datetime import datetime

def inject():
    print("[STIMULUS] Injecting DRIFT_DETECTED signal...")
    with open("/home/anonz/projects/the-council/src/council/core/signals.jsonl", "a") as f:
        event = {
            "timestamp": datetime.now().isoformat(),
            "sender": "Chaos_Stimulus",
            "event": "DRIFT_DETECTED",
            # (Simulated high-entropy value)
            "data": {"e": 0.98}
        }
        f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    inject()
