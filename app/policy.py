from typing import Any


class PolicyError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def authorize_tool(name: str, arguments: dict[str, object]) -> None:
    if name != "search_docs":
        raise PolicyError("TOOL_NOT_ALLOWED", f"Tool '{name}' is not in the gateway allowlist.")
    query = arguments.get("query")
    if not isinstance(query, str) or not query.strip():
        raise PolicyError(
            "INVALID_TOOL_ARGUMENTS", "search_docs requires a non-empty string query."
        )
    if len(query) > 500:
        raise PolicyError(
            "INVALID_TOOL_ARGUMENTS", "search_docs query exceeds the 500 character limit."
        )


def execute_allowed_tool(name: str, arguments: dict[str, object]) -> dict[str, Any]:
    authorize_tool(name, arguments)
    query = str(arguments["query"])
    return {
        "tool": "search_docs",
        "query": query,
        "documents": [
            {
                "title": "Gateway security policy",
                "snippet": "Only explicitly allowlisted, read-only tools may run.",
            }
        ],
    }
