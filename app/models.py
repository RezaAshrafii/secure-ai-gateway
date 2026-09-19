from typing import Literal

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(min_length=1, max_length=8_000)


class ToolRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    arguments: dict[str, object] = Field(default_factory=dict)


class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1, max_length=20)
    tool: ToolRequest | None = None


class ChatResponse(BaseModel):
    request_id: str
    decision: Literal["allow", "deny"]
    answer: str | None = None
    tool_result: dict[str, object] | None = None
    blocked_reason: str | None = None
