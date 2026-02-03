from dataclasses import dataclass, asdict
from typing import List
from datetime import datetime

@dataclass
class LogEvent:
    timestamp: str
    did: str
    source_ip: str
    event_type: str
    success: bool
    details: str

class LogStorage:
    def __init__(self):
        self._events: List[LogEvent] = []

    def log_event(self, did: str, source_ip: str, event_type: str, success: bool, details: str):
        event = LogEvent(
            timestamp=datetime.utcnow().isoformat(),
            did=did,
            source_ip=source_ip,
            event_type=event_type,
            success=success,
            details=details
        )
        self._events.append(event)

    def get_events_for_did(self, did: str, last_n: int = 20) -> List[dict]:
        events = [e for e in self._events if e.did == did]
        return [asdict(e) for e in events[-last_n:]]
