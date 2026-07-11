import asyncio
import random
import time

class AutonomousWatchdog:
    def __init__(self, check_interval=1.5):
        self.check_interval = check_interval
        self._running = False
        self._drift_spikes = 0

    async def run(self, duration=6.0):
        """Runs a time-bounded monitoring session for demonstration."""
        print("\n[WATCHDOG START] Monitoring Semantic/Operational stability...")
        start_time = time.time()
        self._running = True
        
        try:
            while self._running and (time.time() - start_time < duration):
                # Simulate observing semantic drift from a stream of inputs
                entropy = random.uniform(0, 1.0) if random.random() > 0.6 else 0.2
                timestamp = time.strftime("%H:%M:%S")

                if entropy > 0.5:
                    print(f"[{timestamp}] [ALERT] ENTROPY SPIKE! (E={entropy:.3f}) -> Triggering Meta-Recalibration...")
                    self._drift_spikes += 1
                    await asyncio.sleep(2) # Simulate recalibration delay
                else:
                    print(f"[{timestamp}] [STATUS] Nominal (E={entropy:.3f})")

                await asyncio.sleep(self.check_interval)

            print("\n[WATCHDOG ENDED] Session complete.")
        except Exception as e:
            print(f"Watchdog interrupted by error: {e}")
        finally:
            self._running = False

    def get_statistics(self):
         return {"spikes": self._drift_spikes}

if __name__ == "__main__":
    watcher = AutonomousWatchdog()
    asyncio.run(watcher.run())
