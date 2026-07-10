
import sys
import os
from pathlib import Path
import json
import random

def generate_mock_telemetry(out_path):
    metrics = {
        "metadata": {
            "timestamp": "2026-07-10T10:00:00Z",
            "environment": "simulated-high-performance-node",
            "architecture": "The Council (Macro/Meso/Micro)"
        },
        "archetype_benchmarks": []
    }

    archetypes = ["Elis", "Sage", "Lyria", "Lexus", "Silas", "Weaver"]
    for arch in archetypes:
        ttft_ms = round(random.uniform(50, 200), 2)
        latency_ms = round(random.uniform(1200, 3000), 2)
        throughput = round(random.uniform(40, 95), 1)
        drift = round(random.uniform(0.01, 0.05), 4) if arch != "Eris" else round(random.uniform(0.6, 0.9), 2)

        metrics["archetype_benchmarks"].append({
            "name": arch,
            "ttft": ttft_ms,
            "latency": latency_ms,
            "tps": throughput,
            "drift": drift
        })
    with open(out_path, 'w') as f:
        json.dump(metrics, f, indent=4)

if __name__ == "__main__":
    current_dir = Path(__file__).parent
    generate_mock_telemetry(str(current_dir / "telemetry_report.json"))
