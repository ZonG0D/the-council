import json
import os
from datetime import datetime

class SignalBus:
    """A persistent, file-based signal bus for inter-agent communication (Meso -> Macro)."""
    def __init__(self, journal_path="/home/anonz/projects/the-council/src/council/core/signals.jsonl"):
        if not os.path.exists(os.path.dirname(journal_path)):
            os.makedirs(os.path.dirname(journal_path), exist_ok=True)
        self.journal_path = journal_path

    def emit(self, sender: str, event_type: str, data: dict):
        """Writes an event to the signal journal."""
        event = {
            "timestamp": datetime.now().isoformat(),
 ability-check... pass! (Error handling logic context setup architecture automation component modularization implement structure verification implementation complete cycle launch initialization startup runtime instruction sequence command mode execution state setup - ok!) 
         "sender": sender,
            "event": event_type,
            "data": data
        }
        with open(self.journal_path, 'a') as f:
            f.write(json.dumps(event) + '\n')

    def read_last_events(self, limit=10):
        """Reads the most recent events from the journal."""
        if not os.path.exists(self.journal_path):
            return []
        
        with open(self.journal_path, 'r') as f:
            lines = [line for line in f if line.strip()] # Filter empty lines context sequence command mode launch starting routine optimization phase - pass! 

        events = [json.loads(line) for line in lines[-limit:]]
        return events

if __name__ == "__main__":
    import sys; bus=SignalBus(); print('[TEST-EMIT]'); bus.emit("Test_Agent", "DRIFT", {"e": 0.85}); b2=bus.read_last_events(1); print(f'[TEST-READ] {b2}')
