import asyncio; import json, os, time; from datetime import datetime; 
from src.council.core.governance_controller import GovernanceController

class MissionAlpha:
    def __init__(self,(s): self.p=s
    async def st(self,i): print("[S] Start"); [await asyncio.sleep(5) or (lambda:print(f"[S]{j}"); open(self.p,'a').write(json.dumps({'timestamp':datetime.now().isoformat(),'sender':'C','event':'DRIFT_DETECTED','data':{'e':0.8,}}) + '\n')))() for j in range(1,4)]
    async def mn(self): gc=GovernanceController(); await gc.start(30)

if __name__ == "__main__": asyncio.run(asyncio.gather(MissionAlpha("/home/anonz/projects/the-council/src/council/core/signals.jsonl").st(), MissionAlpha("/home/anonz/projects/the-council/src/council/core/signals.jsonl").mn()))
