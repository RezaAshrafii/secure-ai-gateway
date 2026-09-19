from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    rate_limit: int = 30
    rate_window_seconds: int = 60
    max_messages: int = 20
    max_message_chars: int = 8_000

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            rate_limit=int(os.getenv("GATEWAY_RATE_LIMIT", "30")),
            rate_window_seconds=int(os.getenv("GATEWAY_RATE_WINDOW_SECONDS", "60")),
        )
