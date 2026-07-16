import asyncio
from typing import Callable, List, Dict, Any

class SignalBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        """Subscribes a listener to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    async def emit(self, event_name: str, data: Any):
        """Emits an event to all subscribers."""
        if event_name in self._subscribers:
            for callback in self.subscribers[event_name]:
                # Support both async and sync callbacks
                if asyncio.iscoroutinefunction(callback):
                    await callback(data)
                else:
                    callback(data)

# Singleton instance for the Council
bus = SignalBus()
