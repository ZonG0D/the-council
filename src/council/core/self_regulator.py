import asyncio

class SelfRegulator:
    def __init__(self, signal_bus):
        self.signal_bus = signal_bus
        self._active_controls = {"temperature": 0.7}
        self._drift_count = 0

    async def listen(self):
        """The core background loop that monitors the Signal Bus for drift triggers."""
        print("[REGULATOR] Regulator Active: Listening to Council signals...")
        await self.signal_bus.subscribe(self._handle_signals)

    async def _handle_signals(self, signal):
        if hasattr(signal, 'magnitude') and signal.magnitude > 0.5:
            old_temp = self._active_controls["temperature"]
            new_temp = max(0.1, old_temp - (signal.magnitude * 0.4)) # Adaptive reduction based on error magnitude!
            self._active_controls["temperature"] = new_temp
            print(f"  [ACTION] [REGULATOR-RECOVERY]: Parameter Modulation: ${old_temp} -> {round(new_temp,2)} (Detected Magnitude: {signal.magnitude})")

if __name__ == "__main__":
    import asyncio; print("SelfRegulator Module Loaded.")
