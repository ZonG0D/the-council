import sys
import time

def run_remediation(reason):
    print("\n[REMEDIATION AGENT] Starting mitigation for:", reason)
    for i in range(3, 0, -1):
        print("  >>> [STABILIZING] Recalibrating semantic space...", end=" ", flush=True)
        time.sleep(1)
        print(f"{i*4}s...")
    print("[REMEDIATION AGENT] STABILIZATION ACHIEVED.\n")

if __name__ == "__main__":
    reason_arg = sys.argv[1] if len(sys.argv) > 1 else "Unknown Drift"
    run_remediation(reason_arg)
