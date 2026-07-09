
import requests
import json
import sys

def run_smoke_test(url, model, prompt):
    print("--- Starting Smoke Test ---")
    print(f"Target URL: {url}")
    print(f"Target Model: {model}")
    print(f"Prompt: '{prompt}'\n")

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    try:
        response = requests.post(f"{url}/api/generate", json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS: Connection and Model Response established.")
            print(f"Response: {result.get('response')}")
            return True
        else:
            print(f"❌ ERROR: Received status code {response.status_code}")
            print(f"Response body: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the Ollama node (Network/Host unreachable).")
        return False
    except requests.exceptions.Timeout:
        print("❌ ERROR: Request timed out.")
        return False
    except Exception as e:
        print(f"❌ ERROR: An unexpected error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Configuration
    OLLAMA_ENDPOINT = "http://192.168.1.28:11434"
    MODEL_NAME = "gemma4:26b-a4b-it-qat"
    PROMPT = "You are an agent of The Council. Acknowledge your operational status."

    if run_smoke_test(OLLAMA_ENDPOINT, MODEL_NAME, PROMPT):
        sys.exit(0)
    else:
        sys.exit(1)
