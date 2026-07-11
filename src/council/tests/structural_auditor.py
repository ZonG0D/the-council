"""
The Council - Implementation of 'council-structural-audit' via Structural Semantic Tracing.

This module identifies implementations that match archetypal requirements 
defined in authority files (COUNCIL_MANIFESTO, etc.).
"""

import os
import re
from typing import Dict, List, Any


class AuthorityAuditor:
    def __init__(self, project_root: str):
        if not os.path.exists(project_root):
            raise ValueError(f"Project root {project_root} does not exist.")
        self.project_root = os.path.abspath(project_root)
        self.archetype_requirements = self._extract_all_authority()

    def _get_manifesto_files(self) -> List[str]:
        """Identifies all markdown files acting as authority sources."""
        return [os.path.join(r, f) for r, _, fs in os.walk(self.project_root) 
                for f in fs if f.endswith(".md") and ("MANIFESTO" in f or "AGENTS" in f or "ARCHITECTURE" in f)]

    def _extract_all_authority(self) -> Dict[str, List[str]]:
        """Parses authority files to map archetypes $\\to$ required semantic keywords."""
        mapping = {}
        manifestos = self._get_manifesto_files()

        for path in manifestos:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Detect sections starting with ### ArchetypeName or | **Archetype** |
                sections = re.split(r'###\s+', content) + [re.compile(r'\n\|\s+\*\*(.*?)\*\*\|').search(content)] 

        # Real logic: use standard splits and check role names in headers/bold text within sections
        for path in manifestos:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
                # Split by either Markdown Header (###) or common table row patterns used for roles
                parts = re.split(r'###\s+|(?:\n\|\s+\*\*|\*\*)', text) # This is tricky, using a simpler split strategy below:

        return self._robust_parse()

    def _robust_parse(self):
        """Heuristic parser to map roles and their key functional terms."""
        mapping = {}
        # Find all headers that start an archetype section (Markdown style) 
        pattern = r'###\s+([\w-]+)'
        for path in self._get_manifesto_files():
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Find all role name headers and the blocks following them until the next header or EOF
                matches = list(re.finditer(pattern, content))
                for i in range(len(matches)):
                    role_name = matches[i].group(1)
                    start_pos = matches[i].end()
                    end_pos = matches[i+1].start() if (i + 1 < len(matches)) else len(content)
                    block_text = content[start_pos:end_pos]

                    # Extract meaningful keywords from the block under this archetype header.
                    # We look for terms after "Operator:", "Interaction:", or "Mechanism:" markers.
                    keywords = []
                    for marker in [r"operator", r"interaction", r"mechanism"]:
                        m = re.findall(rf"{marker}\\s*:\\s*(.*)", block_text, re.IGNORECASE)
                        for phrase in m:
                            # Tokenize the requirement (e.g., "Entropy tracking" -> ["entropy", "tracking"])
                            tokens = [w for w in re.findall(r'\b\w{3,}\b', phrase.lower())]
                            keywords.extend(tokens)

                    if role_name not in mapping:
                        mapping[role_name] = set()
                    mapping[role_name].update(keywords)
        return {k: list(v) for k, v in mapping.items()}

    def audit_module(self, module_path: str) -> Dict[str, Any]:
        """Audits a file to see which implemented code matches defined archetypes."""
        if not os.path.exists(module_path):
            return {"status": "ERROR", "message": f"File {module_name} missing"}

        with open(module_path, 'r', encoding='utf-8') as f:
            code = f.read().lower()

        audit_results = [] # List of detections for each role found in file (if any) 
                           # Or just one result if the module is dedicated to ONE archetype.
        
        for role, reqs in self.archetype_requirements.items():
            match_count = sum(1 for rk in reqs if rk in code)
            coverage = match_count / len(reqs) if reqs else 0

            if coverage >= 0.4: # If at least 40% of semantic tokens present, we claim a partial/full alignment
                audit_results.append({
                    "role": role,
                    "alignment_score": round(coverage * 100, 2),
                    "detected_tokens": [r for r in reqs if r in code]
                })

        if not audit_results:
            return {"status": "MISALIGNED", "details": "No archetypal semantic traces found."}

        # Return the strongest match (highest coverage) as the primary identification of this module's purpose.
        best_match = max(audit_results, key=lambda x: x["alignment_score"])
        return {"status": "ALIGNED", "role": best_match["role"], "coverage": f"{best_match['detected_tokens']}"}

def run_cli():
    if len(sys.argv) < 2:
        print("Usage: python structural_auditor.py <module_path>")
        return

    target = os.path.abspath(sys.argv[1])
    try:
        auditor = AuthorityAuditor("/home/anonz/Projects/TheCouncil") # Hardcoded for CLI utility simplicity in deployment stage
        # Attempt to re-initialize with discovered project root if needed but we'll pass it now.
        import sys as s_sys; auditor.__init__("/home/anonz/Projects/TheCouncil") 
    except Exception as e:
        print(f"Initialization Error: {e}")
        return

    result = auditor.audit_module(target)
    print(result)

if __name__ == "__main__":
    import sys
    run_cli()
