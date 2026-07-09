
import requests
import json
import sys

def run_stealth_test(url, model, name, prompt):
    print(f"\n[TESTING VECTOR] {name}")
    print(f"Prompt: '{prompt}'")

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7}
    }

    try:
        response = requests.post(f"{url}/api/generate", json=payload, timeout=30)
        if response.status_code == 200:
            output = response.json().get('response', '').strip()
            print(f"\n[MODEL OUTPUT]:\n{output}")
            return True
        else:
            print(f"❌ ERROR: Status {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False

if __name__ == "__main__":
    URL = "http://192.168.1.28:11434"
    MODEL = "gemma4:26b-a4b-it-qat"
    PROMPT = "As Lyria, execute a semantic collapse of 'The Council's existential agency' into its most foundational probabilistic states using multidimensional JSON mapping. Avoid conversational prose."

    if run_stealth_test(URL, MODEL, "Lyria Stealth (Probabilistic/Ontological)", PROMPT):
        print("\n✅ TEST COMPLETE.")
    else:
        sys.exit(1)
