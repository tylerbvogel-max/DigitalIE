"""Builders for calculation-pack method registries."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Callable, Mapping

from .calculation_contracts import MethodContract


def context_schema() -> dict[str, Any]:
    """Build optional receipt-context schema."""
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "case_id": {"type": "string"},
            "analysis_id": {"type": "string"},
            "evidence_ids": {"type": "array", "items": {"type": "string"}},
            "units": {"type": "string"},
            "purpose": {"type": "string"},
        },
    }


def number(minimum: float | None = None, maximum: float | None = None) -> dict[str, Any]:
    """Build a numeric JSON schema."""
    schema: dict[str, Any] = {"type": "number"}
    if minimum is not None:
        schema["minimum"] = minimum
    if maximum is not None:
        schema["maximum"] = maximum
    return schema


def integer(minimum: int | None = None, maximum: int | None = None) -> dict[str, Any]:
    """Build an integer JSON schema."""
    schema: dict[str, Any] = {"type": "integer"}
    if minimum is not None:
        schema["minimum"] = minimum
    if maximum is not None:
        schema["maximum"] = maximum
    return schema


def string() -> dict[str, Any]:
    """Build a nonempty string JSON schema."""
    return {"type": "string", "minLength": 1}


def array(items: Mapping[str, Any], minimum: int = 1) -> dict[str, Any]:
    """Build an array JSON schema."""
    return {"type": "array", "items": dict(items), "minItems": minimum}


def object_schema(
    properties: Mapping[str, Any], required: tuple[str, ...] = ()
) -> dict[str, Any]:
    """Build a closed object JSON schema."""
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": dict(properties),
        "required": list(required),
    }


def input_schema(properties: Mapping[str, Any], required: tuple[str, ...]) -> dict[str, Any]:
    """Build a closed method input schema with optional receipt context."""
    return object_schema({**properties, "context": context_schema()}, required)


def _result_mapping(result: Any, scalar_name: str | None) -> dict[str, Any]:
    if is_dataclass(result) and not isinstance(result, type):
        return asdict(result)
    if isinstance(result, Mapping):
        return dict(result)
    if scalar_name is None:
        raise TypeError("a scalar calculation result requires a result field name")
    return {scalar_name: result}


def compute_adapter(
    function: Callable[..., Any], argument_names: tuple[str, ...], scalar_name: str | None = None
) -> Callable[[Mapping[str, Any]], tuple[dict[str, Any], dict[str, Any]]]:
    """Adapt a pure keyword-callable calculation to the receipt contract."""
    def compute(arguments: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        supplied = {name: arguments[name] for name in argument_names if name in arguments}
        results = _result_mapping(function(**supplied), scalar_name)
        undefined = sorted(name for name, value in results.items() if value is None)
        return {"undefined_metrics": undefined}, results

    return compute


def method(
    method_id: str,
    title: str,
    description: str,
    formulas: tuple[str, ...],
    properties: Mapping[str, Any],
    required: tuple[str, ...],
    function: Callable[..., Any],
    argument_names: tuple[str, ...],
    assumptions: tuple[str, ...],
    authority_boundary: str,
    scalar_name: str | None = None,
) -> MethodContract:
    """Build one versioned calculation method contract."""
    return MethodContract(
        method_id=method_id,
        tool_name=method_id.replace(".", "_"),
        title=title,
        description=description,
        formulas=formulas,
        input_schema=input_schema(properties, required),
        compute=compute_adapter(function, argument_names, scalar_name),
        assumptions_not_established=assumptions,
        authority_boundary=authority_boundary,
    )
