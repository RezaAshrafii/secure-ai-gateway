from collections.abc import Sequence

from .models import Message


class MockProvider:
    """Deterministic local provider: useful for demos and tests without credentials."""

    def complete(
        self, messages: Sequence[Message], tool_result: dict[str, object] | None = None
    ) -> str:
        last_user = next(
            (message.content for message in reversed(messages) if message.role == "user"), ""
        )
        suffix = " Tool result was authorized and attached." if tool_result else ""
        return f"Demo response for a {len(last_user)}-character request.{suffix}"
