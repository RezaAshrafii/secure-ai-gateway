from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import threading
from typing import Any


@dataclass(frozen=True)
class AuditEvent:
    request_id: str
    timestamp: str
    decision: str
    code: str
    client_id: str
    message_count: int
    content_sha256: str
    content_chars: int


class AuditLog:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []
        self._lock = threading.Lock()

    def record(
        self, request_id: str, decision: str, code: str, client_id: str, contents: list[str]
    ) -> AuditEvent:
        joined = "\n".join(contents)
        event = AuditEvent(
            request_id,
            datetime.now(timezone.utc).isoformat(),
            decision,
            code,
            client_id,
            len(contents),
            hashlib.sha256(joined.encode()).hexdigest(),
            len(joined),
        )
        with self._lock:
            self.events.append(event)
        return event

    def as_dicts(self) -> list[dict[str, Any]]:
        with self._lock:
            return [asdict(event) for event in self.events]
