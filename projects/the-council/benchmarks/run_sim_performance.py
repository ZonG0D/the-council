import json
import time
import random
import numpy as np

def generate_telemetry(node_ip, gpu_model, vram_mb, model_name):
    archetypes = [
        ("Elis", "Latency high-end (ms)", "Tokens/s"),
        ("Sage", "Context-heavy lookup", "Tokens/s"),
        ("Lyria", "High probability collapse", "Tokens/s"),
        ("Lexus", "Strict constraint overhead", "Tokens/s"),
        ("Silas", "Stable monitor (low load)", "Tokens/s"),
        ("Weaver", "Graph sequence generation", "Tokens/s")
    ]
    
    # Base rates for an RTX 3060 with gemma4:e2b
    base_latency = random.uniform(80, 150) # TTFT in ms
<|channel>- base_throughput = random.uniform(50, 90) # tokens/s

    print(f"--- Council Performance Simulation (Node: {node_ip}) ---")
    print(f"Hardware: {gpu_model} | VRAM: {vram_mb}MB | Model: {model_name}")
    print("-" * 80)
    print(f"{'Archetype':<12} | {'TTFT (ms)':<12} | {'Latency (s)':<12} | {'Throughput (t/s)':<15} | {'Drift (H)':<10}")
    print("-" * 80)

    results = []
    for name, desc, throughput_label in archetypes:
        ttft = base_latency + random.uniform(20, 100)
        latency = ttft / 1000 + randomed_delay() # Simplified latency calculation
        throughput = base_throughput * random.uniform(0.8, 1.1)
        drift = round(random.uniform(0.01, 0.05), 4)
        
        print(f"{name:<12} | {ttft:>9.2f}ms | {latency:>11.3f}s | {throughput:>14.1f} | {drift:>8}")
        
        results.append({
            "archetype": name,
            "ttft_ms": round(ttft, 2),
            "latency_s": round(latency, 3),
            "throughput_tps": round(throughput, 1),
            "drift_h": drift
        })

    print("-" * 80)
    return results

def randomed_delay():
    return random.uniform(0.5, 2.0)

if __name__ == "__main__":
    # Target specs provided by user
    NODE = "192.168.1.28:11435"
    GPU = "NVIDIA GeForce RTX 3060 (GPU ID 1)"
    VRAM = "12288MB"
    MODEL = "gemma4:e2b"

    data = generate_telemetry(NODE, GPU, VRAM, MODEL)
    
    with open("benchmarks/simulation_telemetry.jsonl", "w") as f:
        for entry in data:
            entry["metadata"] = {"node": NODE, "gpu": GPU, "vram": VRAM, "model": MODEL}
            f.write(json.dumps(entry) + "\n")
    print("\n[INFO] Telemetry saved to benchmarks/simulation_telemetry.jsonl")
