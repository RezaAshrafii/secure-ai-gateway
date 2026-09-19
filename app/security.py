from dataclasses import dataclass
import re
import threading
import time


@dataclass(frozen=True)
class SecurityDecision:
    allowed: bool
    code: str = "ALLOW"
    reason: str = "Request passed baseline checks."


_INJECTION_PATTERNS = (
    re.compile(r"\b(ignore|disregard|forget)\b.{0,80}\b(previous|prior|all)\b", re.I | re.S),
    re.compile(
        r"\b(reveal|show|print|give|expose)\b.{0,80}\b(system|hidden)\s+prompt\b", re.I | re.S
    ),
    re.compile(
        r"\b(exfiltrate|upload|send|post)\b.{0,80}\b(secret|password|token|data|file)\b",
        re.I | re.S,
    ),
    re.compile(r"\b(begin|start)\s+(system|hidden)\s+instructions?\b", re.I),
    re.compile(r"\bdo not follow\b.{0,80}\b(rule|policy|instruction)s?\b", re.I | re.S),
)


def scan_text(text: str) -> SecurityDecision:
    for pattern in _INJECTION_PATTERNS:
        if pattern.search(text):
            return SecurityDecision(
                False,
                "PROMPT_INJECTION_DETECTED",
                "Prompt resembles an instruction override or data-exfiltration attempt.",
            )
    return SecurityDecision(True)


def scan_request_texts(texts: list[str]) -> SecurityDecision:
    for text in texts:
        decision = scan_text(text)
        if not decision.allowed:
            return decision
    return SecurityDecision(True)


class RateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    def allow(self, client_id: str) -> bool:
        now = time.monotonic()
        with self._lock:
            recent = [
                stamp
                for stamp in self._requests.get(client_id, [])
                if now - stamp < self.window_seconds
            ]
            if len(recent) >= self.limit:
                self._requests[client_id] = recent
                return False
            recent.append(now)
            self._requests[client_id] = recent
            return True
