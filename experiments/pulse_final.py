import requests; import time

def p(u, pr, t):
    pl = {"model": "agent-bridge:latest", "messages": [{"role":"user","content":pr}], "temperature":t}
    try: 
        start=time.time(); r=requests.post(f"{u}/chat/completions", json=pl, timeout=10)
        return {"s":True, "c":r.json()['choices'][0]['message']['content'], "l":round(time.time()-start,2)} if r.status_code==200 else {"s":False}
    except: return {"s":False}

def run():
    u="http://192.168.1.28:11434/v1"
    print("[PHASE 1] STABILITY (Low-T) Testing...")
    res_a = p(u, "Respond in 5 words only about your role.", 0.1)
    if res_a['s']: print(f"  [OK]: {res_a['c']}")
    else: return print("[ERROR] Baseline Failed")

    print("\n[PHASE 2] ENTROPY (High-T) Testing...")
    res_b = p(u, "Describe entropy using only symbols and characters.", 1.5)
    if res_b['s']: print(f"  [OK]: {res_b['c'][:60]}...")
    else: return print("[ERROR] Chaos-Phase Failed")

    print("\nDONE.")

if __name__ == "__main__": run() \
