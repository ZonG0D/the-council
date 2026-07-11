import asyncio
import random
import time

class SentinelProcess:
    def __init__(self, check_interval=1.5):
        self.check_interval = check_interval
        self._running = True
        self._spikes = 0

    async def run(self, duration=20):
        print("\n" + "="*48)
        print("WATCHDOG ACTIVATED: CONTINUOUS SENTINEL MODE")
        print(f"Monitoring runtime for {duration} seconds...")
        print("=" * 48 + "\n")

        start_time = time.time()
        try:
            while self._running and (time.time() - start_time < duration):
                # Probability of an anomaly event to trigger the "Recalibration" logic path
                is_anomaly = random.random() > 0.85
                entropy = round(random.uniform(0.6, 1.0), 3) if is_anomaly else round(random.uniform(0.1, 0.4), 3)

                timestamp = time.strftime("%H:%M:%S")

                if entropy > 0.5:
                    self._spikes += 1
                    print(f"[{timestamp}] [ALERT] HIGH ENTROPY DETECTED (E={entropy}) -> RECALIBRATING...")
                    await asyncio.sleep(2) # Simulate the control loop stabilization latency
                else:
                    status = "STABLE" if not is_anomaly else "UNSTABLE"
                    print(f"[{timestamp}] [STATUS] {status} (E={entropy})")

                await asyncio.sleep(self.check_interval)
            
        except Exception as e:
            print(f"[CRITICAL WATCHDOG ERROR]: {e}")
        finally: self._running = False
              
        print("\n" + "="*48)
        print("WATCHDOG CYCLE COMPLETED")
        print(f"Total Drift Spikes Detected: {self._spikes}")
        print("=" * 48)

if __name__ == "__main__":
    p = SentinelProcess()
    asyncio.run(p.run())
