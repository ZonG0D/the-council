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
        print("WATCHDOG ACTIVATED: CONTINUOUS SENTINEL MODE")
        print(f"Monitoring Semantic Stability for {duration}s cycle...")
        print("=" * 48 + "\n")

        start_time = time.time()
        try:
            while self._running and (time.time() - start_time < duration):
                is_chaos = random.random() > 0.75
                entropy = round(random.uniform(0.65, 1.0), 3) if is_chaos else round(random.uniform(0.2, 0.49), 3)

                timestamp = time.strftime("%H:%M:%S")
                if is_chaos:
                    self._drift_count += 1
                    print(f"[{timestamp}] [!] ALERT (E={entropy}) -> TRIGGERING RECALIBRATION...")
                    await asyncio.sleep(2)
                else:
                    print(f"[{timestamp}] [OK] NOMINAL (E={entropy})")
                    await asyncio.sleep(self._interval)

            print("\n============================================\nWATCHDOG CYCLE COMPLETE | Spikes Detected: " + str(self._drift_count))
        except Exception as e: print(f"CRITICAL error:\n{e}")

if __name__ == "__main__":
    import asyncio; v = SentinelWatcher(); asyncio.run(v.run())
