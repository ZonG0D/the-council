import requests

def probe(url, prompt, temp):
    payload = {"model": "agent-bridge:latest", "messages": [{"role":"user","content":prompt}], "temperature":temp}
    try:
        start = time.time(); import time; # re-check imports if they exist in this block... 
# (I am moving to Python -c for real control)

import requests, time
def single_test(url): print("Connecting..."); r=requests.get('http://192.168.1.28:11435') # wait port? user said 11434!
print("Testing Port 11434...")

# I will use a simple, robust shell command to check connectivity and then run the real test script via python -c with hardcoded content to avoid heredoc risk.

cat << 'EOF' > /home/anonz/Projects/TheCouncil/experiments/pulse_final.py
import requests, time
def p(u, pr, t):
    try: 
        r=requests.post(f"{u}/chat/completions", json={"model":"agent-bridge:latest","messages":[{"role":"user","content":pr}],"temperature":t},timeout=10)
        return {"s":True,"c":r.json()['choices'][0]['message']['content'] if r.status_code==200 else "Err:"+str(r.status_code)}
    except Exception as e: return {"s":False, "e": str(e)}

def m():
    u="http://192.168.1.28:11434/v1"
    print("Phase A (Stable)..."); r_a=p(u,"Name?",0.1); print(f"{r_a}")
    print("Phase B (Chaos)..."); r_b=p(u,"Entropy symbols",1.5); print(f"{r_b}")

if __name__=="__main__": m()
