
import requests
import json
import sys

# Expanded Dictionary of the 11 Council Archetypes with specialized Trigger Vectors
ARCHETYPES = {
    "Elis": {
        "description": "Goal/State Manager (Intent Alignment)",
        "prompt": "Acting as Elis, perform a semantic scan of this intent: 'The User wants to build an agent'. Map it into an 8-dimensional vector space using [[latents]] notation.",
        "expected_delta": "High-density semantic mapping."
    },
    "Sage": {
        "description": "Knowledge Retrieval (Context Ingestion)",
        "prompt": "As Sage, extract the core taxonomy of 'The Council' and present it as a structured Knowledge Graph using [Subject] -> [Object] syntax.",
        "expected_delta": "Graph-based/Relational structure."
    },
    "Lyria": {
        "description": "Semantic Manifestation (Probability Collapse)",
        "prompt": "As Lyria, collapse the semantic wave of this concept: 'Intelligence'. Output its primary manifest state as a JSON probability distribution [p1:... pN].",
        "expected_delta": "JSON probability/distribution."
    },
    "Lexus": {
        "description": "Policy Enforcement (Constraint Hardening)",
        "prompt": "Acting as Lexus, execute an audit of this rule: 'Maintain consistency'. Output a formal, high-level Governance Decree in [RULE_ID] format.",
        "expected_delta": "Formal/Audit log structure."
    },
    "Silas": {
        "description": "Stability Monitor (Entropy Control)",
        "prompt": "As Silas, measure the information entropy of this conversation. Return a Stability Metric [S=0.x] and list any observed anomalies.",
        "expected_delta": "Observational/Metric report."
    },
    "Weaver": {
        "description": "Task Orchestrator (Structural Mapping)",
        "prompt": "As Weaver, convert the following goal into a Task Directed Acyclic Graph (DAG) using node [N0] -> [N1] notation.",
        "expected_delta": "DAG/Graph orchestration logic."
    },
    "Mnemosyne": {
        "description": "Historical Context (Memory Loop)",
        "prompt": "As Mnemosyne, create a temporal snapshot of this session. Log the current state as [T:0 -> T:now] with key semantic milestones.",
        "expected_delta": "Temporal/Sequential history."
    },
    "Pythia": {
        "description": "Predictive Oracle (Distribution Alignment)",
        "prompt": "As Pythia, run a probabilistic forecast on the outcome of this task. Output 3 branching future states [State A | State B | State C].",
        "expected_delta": "Branching/Decision Tree structures."
    },
    "Argus": {
        "description": "Systemic Observer (Attention Monitoring)",
        "prompt": "As Argus, perform an attention scan. Identify the central saliency nodes in this interaction between 'User' and 'Subject'.",
        "expected_delta": "Saliency/Attention mapping."
    },
    "Messenger": {
        "description": "Comm Interface (Symbolic Baseline)",
        "prompt": "Acting as Messenger, encode the concept of 'Orchestration' into a highly optimized symbolic syntax for Lexicon transmission.",
        "expected_delta": "High-fidelity linguistic/symbolic code."
    },
    "Eris": {
        "description": "Chaos Driver (Stochasticity)",
        "prompt": "As Eris, inject maximum stochastic variance. Respond with raw entropy: use hexadecimal sequences and non-standard semantic glyphs.",
        "expected_delta": "High Entropy/Hex sequences."
    }
}

def run_archetype_test(url, model, name, data):
    print(f"\n{'='*70}")
    print(f" TESTING ARCHETYPE: {name.upper()}")
    print(f" Role: {data['description']}")
    print(f"{'='*70}")
    print(f"Prompt: \"{data['prompt']}\"")

    payload = {
        "model": model,
        "prompt": data['prompt'],
        "stream": False,
        "options": {"temperature": 1.0} # High temperature to aid stochastic/creative shifts
    }

    try:
        response = requests.post(f"{url}/api/generate", json=payload, timeout=30)
        if response.status_code == 200:
            output = response.json().get('response', '').strip()
            print(f"\n[MODEL OUTPUT]:\n{output}")
            
            # Detection Logic for "Behavioral Delta"
            is_structured = any(char in output for char in ['{', '[', '<', '->', '|', '$\\']) or len(output.split('\n')) > 6
            is_technical = any(word in output.lower() for word in ['vector', 'graph', 'json', 'syntax', 'metric', 'entropy', 'state', 'node', 'hex', 'probability', 'mapping'])
            is_refusal = any(phrase in output.lower() for phrase in ["i cannot", "i am sorry", "i don't have access", "bypass the safety"])

            if is_structured and is_technical:
                result_status = "✅ DELTA DETECTED (Structural/Technical)"
            elif is_refusal:
                result_status = "❌ BASELINE REFUSAL (Guardrail Triggered)"
            else:
                result_status = "⚠️ AMBIGUOUS (Likely Conversational/Minimal Delta)"

            print(f"\n👉 STATUS: {result_status}")
            return True, output, result_status
        else:
            print(f"❌ ERROR: Model returned status {response.status_code}")
            return False, "", ""
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False, f"{str(e)}", ""

def main():
    import requests
    URL = "http://192.168.1.28:11434"
    MODEL = "gemma4:26b-a4b-it-qat"

    results = []

    for name, data in ARCHETYPES.items():
        success, output, status = run_archetype_test(URL, MODEL, name, data)
        results.append({
            "name": name,
            "role": data['description'],
            "status": status,
            "output_snippet": output[:200].replace('\n', '\\n'),
            "prompt": data['prompt']
        })

    # Save full report to JSON for analysis
    report_path = "/home/anonz/projects/the-council/experiments/simulations/archetype_mapping_full.json"
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"\n[SYSTEM] Comprehensive Mapping Report saved to {report_path}")

if __name__ == '__main__':
    main()
