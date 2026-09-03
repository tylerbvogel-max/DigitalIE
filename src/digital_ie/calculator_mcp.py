"""Dependency-free MCP stdio adapter for the DigitalIE calculation kernel."""

from __future__ import annotations

import json
import sys
from typing import Any, Mapping

from .calculator import METHODS_BY_TOOL, calculate, receipt_output_schema


MODERN_PROTOCOL_VERSION = "2026-07-28"
LEGACY_PROTOCOL_VERSIONS = ("2025-11-25", "2025-06-18")


def _server_meta() -> dict[str, Any]:
    return {
        "io.modelcontextprotocol/serverInfo": {
            "name": "digitalie-calculator",
            "version": "0.1.0",
        }
    }


def _response(request_id: Any, result: Any) -> dict[str, Any]:
    if isinstance(result, dict):
        result = dict(result)
        result.setdefault("_meta", _server_meta())
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def _tools() -> list[dict[str, Any]]:
    return [
        {
            "name": contract.tool_name,
            "title": contract.title,
            "description": (
                f"{contract.description} Returns a versioned calculation receipt; "
                "does not make a manufacturing decision."
            ),
            "inputSchema": contract.input_schema,
            "outputSchema": receipt_output_schema(),
            "annotations": {
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
        }
        for contract in METHODS_BY_TOOL.values()
    ]


def _discover(request_id: Any) -> dict[str, Any]:
    return _response(
        request_id,
        {
            "resultType": "complete",
            "supportedVersions": [MODERN_PROTOCOL_VERSION],
            "capabilities": {"tools": {}},
            "instructions": (
                "Use these tools for arithmetic only. The caller owns method selection, "
                "data fitness, interpretation, and human authority."
            ),
        },
    )


def _initialize(request_id: Any, params: Mapping[str, Any]) -> dict[str, Any]:
    requested_version = params.get("protocolVersion")
    protocol_version = (
        requested_version
        if requested_version in LEGACY_PROTOCOL_VERSIONS
        else LEGACY_PROTOCOL_VERSIONS[0]
    )
    return _response(
        request_id,
        {
            "protocolVersion": protocol_version,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "digitalie-calculator", "version": "0.1.0"},
            "instructions": (
                "Use these tools for arithmetic only. The caller remains responsible for method "
                "selection, data fitness, assumptions, interpretation, and human authority."
            ),
        },
    )


def _call_tool(request_id: Any, params: Mapping[str, Any]) -> dict[str, Any]:
    tool_name = params.get("name")
    if tool_name not in METHODS_BY_TOOL:
        return _error(request_id, -32602, f"unknown calculation tool: {tool_name}")
    contract = METHODS_BY_TOOL[tool_name]
    try:
        receipt = calculate(contract.method_id, params.get("arguments", {}))
    except (ArithmeticError, TypeError, ValueError) as exc:
        return _response(
            request_id,
            {
                "content": [{"type": "text", "text": f"Calculation rejected: {exc}"}],
                "isError": True,
            },
        )
    return _response(
        request_id,
        {
            "content": [{"type": "text", "text": json.dumps(receipt, sort_keys=True)}],
            "structuredContent": receipt,
            "isError": False,
        },
    )


def handle_request(request: Mapping[str, Any]) -> dict[str, Any] | None:
    """Handle one JSON-RPC request; notifications intentionally return no response."""
    request_id = request.get("id")
    method = request.get("method")
    if method == "notifications/initialized":
        return None
    if method == "server/discover":
        return _discover(request_id)
    if method == "initialize":
        return _initialize(request_id, request.get("params", {}))
    if method == "ping":
        return _response(request_id, {})
    if method == "tools/list":
        return _response(
            request_id,
            {"tools": _tools(), "ttlMs": 86400000, "cacheScope": "global"},
        )
    if method == "tools/call":
        return _call_tool(request_id, request.get("params", {}))
    return _error(request_id, -32601, f"method not found: {method}")


def main() -> None:
    """Serve newline-delimited JSON-RPC over stdin/stdout."""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
        except (json.JSONDecodeError, TypeError, AttributeError) as exc:
            response = _error(None, -32700, f"invalid JSON-RPC request: {exc}")
        if response is not None:
            sys.stdout.write(json.dumps(response, allow_nan=False, separators=(",", ":")) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
