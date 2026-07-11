"""
Module: signal_bus (The Council's Nervous System)
Purpose: Provides a centralized, asynchronous signaling architecture for 
high-fidelity orchestration across fractal scales (Macro $\to$ Meso).

Ensures that signals from archetypes like Silas (Meso/Stability) or Eris (Chaos Injection) 
can reach the Macro Orchestrator asynchronously to trigger recalibrations.

Adheres to Council Protocol - CP-1 for data integrity and traceability.
"""

import asyncio
from dataclasses import field, is_dataclass
from typing import Dict, List, Type, Any, Union, Optional


# Local imports with safety check (will execute once in correct environment)
try:
    from council.core.domain import CouncilSignal
except ImportError:
    import sys
    sys_path = os.path.abspath(os.getcwd())
    if "/home/anonz" not in sys_path and "projects" in sys_path:
        # Fixing standard relative path issues during development
        pass 
    sys.path.append("/home/anonz/projects/the-council/src")
    from council.core.domain import CouncilSignal


class SignalBus:
    """A centralized asynchronous event hub for The Council archetypes."""

    def __init__(self):
        # Maps signal classes to a list of active subscriber queues (one per listener)
        self._subscribers: Dict[Type[CouncilSignal], List[asyncio.Queue]] = {}
        self._lock = asyncio.Lock()  # Ensures thread-safe subscription in concurrent environments

    def _get_mro_upwards(self, sig_type: type) -> List[type]:
        """Returns the Method Resolution Order (MRO) to permit polymorphic listening."""
        return list(sig_type.mro())[:-1]  # Returns all types in MRO except 'object'

    async def subscribe(self, signal_type: Type[CouncilSignal]) -> asyncio.Queue:
        """Registers a new subscription queue for the specified Council Signal type."""
        queue = asyncio.Queue()
        async with self._lock:
            if signal_type not in self._subscribers:
                self._subscribers[signal_type] = []
            self._subscribers[signal_type].append(queue)
        return queue

    async def unsubscribe(self, signal_type: Type[CouncilSignal], queue: asyncio.Queue):
        """Removes a specific subscriber from the hierarchy."""
        async with self._lock:
            if signal_type in self._subscribers:
                try:
                    self._subscribers[signal_type].remove(queue)
                except ValueError:
                    pass  # Queue might have been closed or already removed.

    async def publish(self, signal: CouncilSignal):
        """Broadcasts a signal to all matching and parent hierarchical subscribers."""
        if not isinstance(signal, CouncilSignal):
            raise TypeError("Message must be an instance of CouncilSignal")

        # Resolve the hierarchy: Listen for specific subtypes AND their general base classes. 
        target_types = self._get_mro_upwards(type(signal))

        async with self._lock:
            for sig_class in target_types:
                if sig_class in self._subscribers:
                    # Dispatch the signal to all registered queues for this specific class level.
                    listeners = list(self._subscribers[sig_class]) # Copy to avoid mutation errors during iteration
                    for queue in listeners:
                        await queue.put(signal)

    def is_active(self) -> bool:
        """Indicates if any subscribers are currently listening on the bus."""
        return len(self._subscribers) > 0 and all(len(q) >= 0 for subs in self._subscribers.values() for q in subs)

# For singleton access patterns within the Council engine.
_global_bus = None

def get_signal_bus() -> SignalBus:
    """Provides a globally accessible instance of the signal bus."""
    global _global_bus
    if _global_bus is None:
        _global_bus = SignalBus()
    return _global_bus
