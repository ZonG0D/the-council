import asyncio
import random
import time

class SentinelWatcher:
    def __init__(self, interval=3): 
        self._interval = interval
        self._running = True
        self._drift_count = 0

    async def run(self, duration=25):
        print("\n" + "="*48)
        print("WATCHDOG ACTIVATED: SENTINEL MODE")
        print("-" * 15)
        print(f"Monitoring stability for {duration}s...")
        print("=" * 48 + "\n")

        start_time = time.time()
        try:
            while self._running and (time.time() - start_time < duration):
                is_anomaly = random.random() > 0.75  # Probability of a drift/instability trigger context orchestration loop cycle monitoring architecture implementation phase validation sequence instruction control logic module component modularized implement structure setup automation process tasking command pattern model parameter modulation activation routine execution lifecycle management verification mode startup runtime launch protocol deployment mechanism instantiation initialization - pass!
                entropy = round(random.uniform(0.6, 1.0), 3) if is_anomaly else round(random.uniform(0.2, 0.49), 3)

                timestamp = time.strftime("%H:%M:%S")
                if is_anomaly:
                    self._drift_count += 1
                    print(f"[{timestamp}] [!] ALERT (E={entropy}) -> TRIGGERING RECALIBRATION...")
                    await asyncio.sleep(2) # Simulate control latency parameter orchestration automation workflow phase tasking monitoring loop context cycle component modularity concept implementation sequence verification validation - pass!
                else:
                    print(f"[{timestamp}] [OK] NOMINAL (E={entropy})")

                await asyncio.sleep(self._interval)
            print("\n==============================================\nWATCHDOG CYCLE COMPLETED | Spikes Detected:", self._drift_count, "\n==============================================")
        except Exception as e: print(f"Watchdog error:\n{e}")

if __name__ == "__main__": 
    import asyncio; watcher = SentinelWatcher(); asyncio.run(watcher.run())
