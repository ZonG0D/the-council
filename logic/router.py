"""
The Council MoE Router (Model-based Routing)
This module implements semantic routing based on the COUNCIL_MANIFEST.md.
It directs intelligence signals to the most likely functional MoE Nodes.
"""

class CouncilRouter:
    def __init__(self):
        # Mapping derived from Manifest/Topology
        self.routing_map = {
            'Lexicon': ['syntax', 'grammar', 'sentence', 'word', 'text'],
            'Rosetta': ['translate', 'language', 'foreign', 'idiom', 'cross-lingual'],
            'Euclid': ['math', 'logic', 'calculate', 'formula', 'equation', 'number'],
            'Turing': ['code', 'python', 'function', 'variable', 'algorithm', 'software'],
            'Alexandria': ['fact', 'history', 'who', 'when', 'knowledge', 'data', 'capital', 'country'],
            'Weaver': ['creative', 'story', 'poem', 'prose', 'narrative'],
            'Ariadne': ['context', 'long-range', 'remember', 'dependency', 'sequence'],
            'Prism': ['format', 'json', 'yaml', 'structure', 'schema', 'parsing'],
            'Kepler': ['science', 'physics', 'biology', 'chemical', 'empirical'],
            'Lyria': ['audio', 'sound', 'music', 'spectrogram', 'waveform'],
            'Aegis': ['safety', 'policy', 'prohibited', 'against', 'constraint', 'guard']
        }

    def route_signal(self, input_text: str) -> list[str]:
        input_lower = input_text.lower()
        activated_nodes = set()

        # Check matches
        for node, keywords in self.routing_map.items():
            if any(kw in input_lower for kw in keywords):
                activated_nodes.add(node)

        # Handle the Eris Factor (Stochastic Triggering/Noise Injection)
        if "eris" in input_text.lower():
             activated_nodes.add("Eris")

        # Final result logic: 
        # If we found specific semantic matches, return them + 'Apex' as fallback path
        # If nothing is found, only return 'Apex'
        result = sorted(list(activated_nodes))
        if not result or "Eris" in result:
            if "Eris" in result: # Standardize out the internal tag for end-user perception
                result.remove("Eris")
                result.append("Apex") 
            elif "Apex" not in result:
                result.append("Apex")
        else:
            result.append("Apex")

        return sorted(list(set(result)))

if __name__ == "__main__":
    router = CouncilRouter()
    print("--- Router Test ---")
    test_inputs = [
        "Can you write a Python function to sort a list?",
        "Who was the first president of the United States?",
        "Please translate this sentence into French.",
        "Generate some ambient music soundscapes.",
        "Make sure the output is in JSON format only.",
        "Just say hello."
    ]

    for text in test_inputs:
        targets = router.route_signal(text)
        print(f"Input: '{text}' -> Targets: {targets}")
