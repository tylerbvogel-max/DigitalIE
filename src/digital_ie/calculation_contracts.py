"""Shared contracts for deterministic calculation methods."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping


ComputeFunction = Callable[[Mapping[str, Any]], tuple[dict[str, Any], dict[str, Any]]]


@dataclass(frozen=True)
class MethodContract:
    """Public method metadata plus its deterministic compute adapter."""

    method_id: str
    tool_name: str
    title: str
    description: str
    formulas: tuple[str, ...]
    input_schema: dict[str, Any]
    compute: ComputeFunction
    assumptions_not_established: tuple[str, ...]
    authority_boundary: str
    version: str = "1.0.0"

    def public_description(self) -> dict[str, Any]:
        """Return serializable discovery metadata."""
        return {
            "method_id": self.method_id,
            "tool_name": self.tool_name,
            "version": self.version,
            "title": self.title,
            "description": self.description,
            "formulas": list(self.formulas),
            "input_schema": self.input_schema,
            "assumptions_not_established": list(self.assumptions_not_established),
            "authority_boundary": self.authority_boundary,
        }
