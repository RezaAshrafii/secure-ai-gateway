from uuid import uuid4

from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse

from .audit import AuditLog
from .config import Settings
from .models import ChatRequest, ChatResponse
from .policy import PolicyError, execute_allowed_tool
from .provider import MockProvider
from .security import RateLimiter, scan_request_texts


class Gateway:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_env()
        self.audit = AuditLog()
        self.limiter = RateLimiter(self.settings.rate_limit, self.settings.rate_window_seconds)
        self.provider = MockProvider()


def create_app(gateway: Gateway | None = None) -> FastAPI:
    gateway = gateway or Gateway()
    app = FastAPI(title="Secure AI Gateway", version="0.1.0")

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/chat", response_model=ChatResponse)
    def chat(
        request: ChatRequest, x_client_id: str = Header(default="anonymous")
    ) -> ChatResponse | JSONResponse:
        request_id = str(uuid4())
        contents = [message.content for message in request.messages]
        if not gateway.limiter.allow(x_client_id):
            gateway.audit.record(request_id, "deny", "RATE_LIMITED", x_client_id, contents)
            return JSONResponse(
                status_code=429,
                content={
                    "request_id": request_id,
                    "decision": "deny",
                    "blocked_reason": "Client rate limit exceeded.",
                    "code": "RATE_LIMITED",
                },
            )
        security = scan_request_texts(contents)
        if not security.allowed:
            gateway.audit.record(request_id, "deny", security.code, x_client_id, contents)
            return JSONResponse(
                status_code=403,
                content={
                    "request_id": request_id,
                    "decision": "deny",
                    "blocked_reason": security.reason,
                    "code": security.code,
                },
            )
        tool_result = None
        if request.tool is not None:
            try:
                tool_result = execute_allowed_tool(request.tool.name, request.tool.arguments)
            except PolicyError as error:
                gateway.audit.record(request_id, "deny", error.code, x_client_id, contents)
                return JSONResponse(
                    status_code=403,
                    content={
                        "request_id": request_id,
                        "decision": "deny",
                        "blocked_reason": error.message,
                        "code": error.code,
                    },
                )
        answer = gateway.provider.complete(request.messages, tool_result)
        gateway.audit.record(request_id, "allow", "ALLOW", x_client_id, contents)
        return ChatResponse(
            request_id=request_id, decision="allow", answer=answer, tool_result=tool_result
        )

    return app


app = create_app()
