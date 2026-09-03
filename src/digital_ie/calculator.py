"""Versioned, auditable calculation operations for DigitalIE.

The calculation kernel owns arithmetic. It does not select a method, establish
data fitness, interpret causality, or exercise manufacturing decision authority.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import fsum, isfinite, sqrt
from typing import Any, Callable, Mapping

from . import statistics


METHOD_VERSION = "1.0.0"
AUTHORITY_BOUNDARY = (
    "Calculation only; no product acceptance, process disposition, causal conclusion, "
    "or manufacturing approval is made."
)
COMMON_UNESTABLISHED = (
    "measurement-system suitability",
    "sampling representativeness",
    "independence or dependence structure",
    "distributional assumptions beyond mechanical input checks",
    "causality and practical significance",
)


@dataclass(frozen=True)
class MethodContract:
    method_id: str
    tool_name: str
    title: str
    description: str
    formulas: tuple[str, ...]
    input_schema: dict[str, Any]
    compute: Callable[[Mapping[str, Any]], tuple[dict[str, Any], dict[str, Any]]]

    def public_description(self) -> dict[str, Any]:
        return {
            "method_id": self.method_id,
            "tool_name": self.tool_name,
            "version": METHOD_VERSION,
            "title": self.title,
            "description": self.description,
            "formulas": list(self.formulas),
            "input_schema": self.input_schema,
            "authority_boundary": AUTHORITY_BOUNDARY,
        }


def _array_schema(min_items: int = 1) -> dict[str, Any]:
    return {"type": "array", "items": {"type": "number"}, "minItems": min_items}


def _object_schema(properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            **properties,
            "context": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "case_id": {"type": "string"},
                    "analysis_id": {"type": "string"},
                    "evidence_ids": {"type": "array", "items": {"type": "string"}},
                    "units": {"type": "string"},
                    "purpose": {"type": "string"},
                },
            },
        },
        "required": required,
    }


def _describe_values(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    values = args["values"]
    result = {
        "mean": statistics.mean(values),
        "sample_variance": statistics.sample_variance(values),
        "sample_standard_deviation": statistics.sample_standard_deviation(values),
        "standard_error_mean": statistics.standard_error_mean(values),
    }
    return {"count": len(values), "sum": fsum(values)}, result


def _weighted_mean(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    result = statistics.weighted_mean(args["values"], args["weights"])
    return {"total_weight": fsum(args["weights"])}, {"weighted_mean": result}


def _binomial(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    result = statistics.binomial_probability(args["successes"], args["trials"], args["probability"])
    return {}, {"probability": result}


def _hypergeometric(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    result = statistics.hypergeometric_probability(
        args["successes"], args["draws"], args["population_successes"], args["population_size"]
    )
    return {}, {"probability": result}


def _poisson(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    has_expected = "expected_events" in args
    has_rate_form = "rate" in args or "exposure" in args
    if has_expected == has_rate_form:
        raise ValueError("provide either expected_events or rate with exposure")
    if has_rate_form and not {"rate", "exposure"}.issubset(args):
        raise ValueError("Poisson rate parameterization requires both rate and exposure")
    expected = args["expected_events"] if has_expected else args["rate"] * args["exposure"]
    result = statistics.poisson_probability(args["events"], expected)
    return {"expected_events": expected}, {"probability": result}


def _one_sample_z(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    standard_error = args["sigma"] / sqrt(args["n"])
    result = statistics.one_sample_z_statistic(
        args["sample_mean"], args["null_mean"], args["sigma"], args["n"]
    )
    return {"standard_error": standard_error}, {"z_statistic": result}


def _one_sample_t(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    values = args["values"]
    intermediate = {
        "sample_mean": statistics.mean(values),
        "sample_standard_deviation": statistics.sample_standard_deviation(values),
        "standard_error": statistics.standard_error_mean(values),
    }
    result = statistics.one_sample_t_statistic(values, args["null_mean"])
    return intermediate, {"t_statistic": result, "degrees_freedom": len(values) - 1}


def _paired_t(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    differences = tuple(after - before for before, after in zip(args["before"], args["after"]))
    result = statistics.paired_t_statistic(
        args["before"], args["after"], args.get("null_difference", 0.0)
    )
    intermediate = {
        "differences": differences,
        "mean_difference": statistics.mean(differences),
        "difference_standard_error": statistics.standard_error_mean(differences),
    }
    return intermediate, {"t_statistic": result, "degrees_freedom": len(differences) - 1}


def _welch_t(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    first, second = args["first"], args["second"]
    result, degrees_freedom = statistics.welch_t_statistic(
        first, second, args.get("null_difference", 0.0)
    )
    intermediate = {
        "mean_1": statistics.mean(first),
        "mean_2": statistics.mean(second),
        "variance_1": statistics.sample_variance(first),
        "variance_2": statistics.sample_variance(second),
    }
    return intermediate, {"t_statistic": result, "degrees_freedom": degrees_freedom}


def _one_proportion_z(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    result = statistics.one_proportion_z_statistic(
        args["events"], args["n"], args["null_proportion"]
    )
    return {"observed_proportion": args["events"] / args["n"]}, {"z_statistic": result}


def _two_proportion_z(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    pooled = (args["events_1"] + args["events_2"]) / (args["n_1"] + args["n_2"])
    result = statistics.two_proportion_z_statistic(
        args["events_1"], args["n_1"], args["events_2"], args["n_2"]
    )
    intermediate = {
        "proportion_1": args["events_1"] / args["n_1"],
        "proportion_2": args["events_2"] / args["n_2"],
        "pooled_proportion": pooled,
    }
    return intermediate, {"z_statistic": result}


def _wilson(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    lower, upper = statistics.wilson_proportion_interval(
        args["events"], args["n"], args["z_critical"]
    )
    return {"observed_proportion": args["events"] / args["n"]}, {"lower": lower, "upper": upper}


def _chi_square_independence(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    observed = args["observed"]
    row_totals = [fsum(row) for row in observed]
    column_totals = [fsum(row[index] for row in observed) for index in range(len(observed[0]))]
    total = fsum(row_totals)
    expected = [
        [row_total * column_total / total for column_total in column_totals]
        for row_total in row_totals
    ]
    result, degrees_freedom = statistics.chi_square_independence(observed)
    return {"expected_counts": expected}, {"chi_square": result, "degrees_freedom": degrees_freedom}


def _chi_square_goodness(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    fitted = args.get("fitted_parameters", 0)
    result, degrees_freedom = statistics.chi_square_goodness_of_fit(
        args["observed"], args["expected_probabilities"], fitted
    )
    total = fsum(args["observed"])
    expected = [total * probability for probability in args["expected_probabilities"]]
    return {"expected_counts": expected}, {"chi_square": result, "degrees_freedom": degrees_freedom}


def _runs(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    first, second = args["first_count"], args["second_count"]
    total = first + second
    expected = 1 + 2 * first * second / total
    variance = 2 * first * second * (2 * first * second - first - second) / (total**2 * (total - 1))
    result = statistics.runs_test_z(first, second, args["observed_runs"])
    return {"expected_runs": expected, "variance_runs": variance}, {"z_statistic": result}


def _anova(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    result = statistics.one_way_anova(args["groups"])
    values = asdict(result)
    statistic = values.pop("f_statistic")
    return values, {"f_statistic": statistic}


def _regression(args: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    result = statistics.simple_linear_regression(args["x"], args["y"])
    values = asdict(result)
    reported = {
        key: values.pop(key)
        for key in ("intercept", "slope", "correlation", "determination", "slope_t")
    }
    return values, reported


def _number_schema() -> dict[str, Any]:
    return {"type": "number"}


def _integer_schema() -> dict[str, Any]:
    return {"type": "integer"}


def _positive_integer_schema() -> dict[str, Any]:
    return {"type": "integer", "minimum": 1}


def _proportion_schema() -> dict[str, Any]:
    return {"type": "number", "minimum": 0, "maximum": 1}


def _contract(
    method_id: str,
    title: str,
    description: str,
    formulas: tuple[str, ...],
    properties: dict[str, Any],
    required: list[str],
    compute: Callable[[Mapping[str, Any]], tuple[dict[str, Any], dict[str, Any]]],
    schema_extensions: Mapping[str, Any] | None = None,
) -> MethodContract:
    input_schema = _object_schema(properties, required)
    if schema_extensions:
        input_schema.update(schema_extensions)
    return MethodContract(
        method_id,
        method_id.replace(".", "_"),
        title,
        description,
        formulas,
        input_schema,
        compute,
    )


METHODS = (
    _contract("descriptive.summary", "Descriptive summary", "Mean and sample dispersion.",
              ("x_bar=sum(x_i)/n", "s^2=sum((x_i-x_bar)^2)/(n-1)", "SE=s/sqrt(n)"),
              {"values": _array_schema(2)}, ["values"], _describe_values),
    _contract("descriptive.weighted_mean", "Weighted mean", "Mean with explicit nonnegative weights.",
              ("x_bar_w=sum(w_i*x_i)/sum(w_i)",),
              {"values": _array_schema(), "weights": _array_schema()}, ["values", "weights"], _weighted_mean),
    _contract("probability.binomial", "Binomial probability", "Probability of exactly x successes.",
              ("P(X=x)=C(n,x)*p^x*(1-p)^(n-x)",),
              {"successes": _integer_schema(), "trials": _integer_schema(),
               "probability": _proportion_schema()},
              ["successes", "trials", "probability"], _binomial),
    _contract("probability.hypergeometric", "Hypergeometric probability", "Finite-lot sampling without replacement.",
              ("P(X=x)=C(K,x)*C(N-K,n-x)/C(N,n)",),
              {"successes": _integer_schema(), "draws": _integer_schema(),
               "population_successes": _integer_schema(),
               "population_size": _positive_integer_schema()},
              ["successes", "draws", "population_successes", "population_size"], _hypergeometric),
    _contract("probability.poisson", "Poisson probability", "Event probability over a declared exposure.",
              ("P(X=x)=exp(-lambda)*lambda^x/x!", "lambda=rate*exposure"),
              {"events": _integer_schema(), "expected_events": _number_schema(),
               "rate": _number_schema(), "exposure": _number_schema()},
              ["events"], _poisson,
              {"oneOf": [
                  {"required": ["events", "expected_events"]},
                  {"required": ["events", "rate", "exposure"]},
              ]}),
    _contract("inference.one_sample_z", "One-sample z statistic", "Mean statistic with genuinely known sigma.",
              ("z=(x_bar-mu_0)/(sigma/sqrt(n))",),
              {"sample_mean": _number_schema(), "null_mean": _number_schema(),
               "sigma": _number_schema(), "n": _positive_integer_schema()},
              ["sample_mean", "null_mean", "sigma", "n"], _one_sample_z),
    _contract("inference.one_sample_t", "One-sample t statistic", "Mean statistic with sigma estimated by s.",
              ("t=(x_bar-mu_0)/(s/sqrt(n))", "df=n-1"),
              {"values": _array_schema(2), "null_mean": _number_schema()},
              ["values", "null_mean"], _one_sample_t),
    _contract("comparison.paired_t", "Paired t statistic", "Test the mean of within-pair differences.",
              ("d_i=after_i-before_i", "t=(d_bar-delta_0)/(s_d/sqrt(n))"),
              {"before": _array_schema(2), "after": _array_schema(2),
               "null_difference": _number_schema()},
              ["before", "after"], _paired_t),
    _contract("comparison.welch_t", "Welch two-sample t statistic", "Compare independent means without equal variances.",
              ("t=(x_bar_1-x_bar_2-delta_0)/sqrt(s1^2/n1+s2^2/n2)", "df=Welch-Satterthwaite"),
              {"first": _array_schema(2), "second": _array_schema(2),
               "null_difference": _number_schema()},
              ["first", "second"], _welch_t),
    _contract("comparison.one_proportion_z", "One-proportion z statistic", "Compare an observed proportion with p0.",
              ("z=(p_hat-p0)/sqrt(p0*(1-p0)/n)",),
              {"events": _integer_schema(), "n": _positive_integer_schema(),
               "null_proportion": _proportion_schema()},
              ["events", "n", "null_proportion"], _one_proportion_z),
    _contract("comparison.two_proportion_z", "Two-proportion z statistic", "Compare two independent proportions.",
              ("p_pool=(x1+x2)/(n1+n2)", "z=(p1-p2)/sqrt(p_pool*(1-p_pool)*(1/n1+1/n2))"),
              {"events_1": _integer_schema(), "n_1": _positive_integer_schema(),
               "events_2": _integer_schema(), "n_2": _positive_integer_schema()},
              ["events_1", "n_1", "events_2", "n_2"], _two_proportion_z),
    _contract("inference.wilson_interval", "Wilson proportion interval", "Score interval for a binomial proportion.",
              ("Wilson score interval with supplied z critical value",),
              {"events": _integer_schema(), "n": _positive_integer_schema(),
               "z_critical": _number_schema()},
              ["events", "n", "z_critical"], _wilson),
    _contract("comparison.chi_square_independence", "Chi-square independence", "Categorical association in a contingency table.",
              ("E_ij=row_i*column_j/N", "chi^2=sum((O_ij-E_ij)^2/E_ij)"),
              {"observed": {"type": "array", "items": _array_schema(2), "minItems": 2}},
              ["observed"], _chi_square_independence),
    _contract("comparison.chi_square_goodness_of_fit", "Chi-square goodness of fit", "Observed counts against declared probabilities.",
              ("E_j=n*p_j", "chi^2=sum((O_j-E_j)^2/E_j)", "df=k-1-m"),
              {"observed": {"type": "array", "items": _integer_schema(), "minItems": 2},
               "expected_probabilities": _array_schema(2),
               "fitted_parameters": _integer_schema()},
              ["observed", "expected_probabilities"], _chi_square_goodness),
    _contract("sequence.runs_test", "Runs-test z statistic", "Normal approximation for binary-sequence run count.",
              ("E(R)=1+2*n1*n2/(n1+n2)", "z=(R-E(R))/sqrt(Var(R))"),
              {"first_count": _positive_integer_schema(),
               "second_count": _positive_integer_schema(),
               "observed_runs": _positive_integer_schema()},
              ["first_count", "second_count", "observed_runs"], _runs),
    _contract("comparison.one_way_anova", "One-way ANOVA", "Partition variation across independent groups.",
              ("F=MS_between/MS_within",),
              {"groups": {"type": "array", "items": _array_schema(2), "minItems": 2}},
              ["groups"], _anova),
    _contract("regression.simple_linear", "Simple linear regression", "Least-squares line and diagnostics.",
              ("b1=Sxy/Sxx", "b0=y_bar-b1*x_bar", "R^2=1-SSE/SST"),
              {"x": _array_schema(3), "y": _array_schema(3)}, ["x", "y"], _regression),
)

METHODS_BY_ID = {method.method_id: method for method in METHODS}
METHODS_BY_TOOL = {method.tool_name: method for method in METHODS}


def list_methods() -> list[dict[str, Any]]:
    """Return stable public contracts without executable callables."""
    return [method.public_description() for method in METHODS]


def receipt_output_schema() -> dict[str, Any]:
    """Return the MCP output contract for a successful calculation."""
    required = [
        "calculation_id", "method", "method_version", "formulas", "inputs", "context",
        "intermediates", "results", "mechanically_validated", "context_gaps",
        "assumptions_not_established", "authority_boundary",
    ]
    return {
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": {
            "calculation_id": {"type": "string"},
            "method": {"type": "string"},
            "method_version": {"type": "string"},
            "formulas": {"type": "array", "items": {"type": "string"}},
            "inputs": {"type": "object"},
            "context": {"type": "object"},
            "intermediates": {"type": "object"},
            "results": {"type": "object"},
            "mechanically_validated": {"type": "array", "items": {"type": "string"}},
            "context_gaps": {"type": "array", "items": {"type": "string"}},
            "assumptions_not_established": {
                "type": "array", "items": {"type": "string"},
            },
            "authority_boundary": {"type": "string"},
        },
    }


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, Mapping)
    if expected == "array":
        return isinstance(value, (list, tuple))
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return False


def _validate_schema(value: Any, schema: Mapping[str, Any]) -> None:
    pending = [(value, schema, "input")]
    while pending:
        current, current_schema, path = pending.pop()
        expected_type = current_schema.get("type")
        if expected_type and not _matches_type(current, expected_type):
            raise ValueError(f"{path} must be {expected_type}")
        if isinstance(current, float) and not isfinite(current):
            raise ValueError("calculation inputs must contain only finite numbers")
        if expected_type in ("integer", "number"):
            if "minimum" in current_schema and current < current_schema["minimum"]:
                raise ValueError(f"{path} is below its minimum")
            if "maximum" in current_schema and current > current_schema["maximum"]:
                raise ValueError(f"{path} is above its maximum")
        if expected_type == "array":
            if len(current) < current_schema.get("minItems", 0):
                raise ValueError(f"{path} has too few items")
            item_schema = current_schema.get("items")
            if item_schema:
                pending.extend(
                    (item, item_schema, f"{path}[{index}]")
                    for index, item in enumerate(current)
                )
        if expected_type == "object":
            properties = current_schema.get("properties", {})
            missing = set(current_schema.get("required", [])) - set(current)
            if missing:
                raise ValueError(f"{path} is missing: {', '.join(sorted(missing))}")
            unexpected = set(current) - set(properties)
            if current_schema.get("additionalProperties") is False and unexpected:
                raise ValueError(f"{path} has unexpected fields: {', '.join(sorted(unexpected))}")
            pending.extend(
                (item, properties[key], f"{path}.{key}")
                for key, item in current.items()
                if key in properties
            )


def calculate(method_id: str, arguments: Mapping[str, Any]) -> dict[str, Any]:
    """Execute a registered method and return a content-addressed receipt."""
    if method_id not in METHODS_BY_ID:
        raise ValueError(f"unknown calculation method: {method_id}")
    if not isinstance(arguments, Mapping):
        raise ValueError("calculation arguments must be an object")
    contract = METHODS_BY_ID[method_id]
    _validate_schema(arguments, contract.input_schema)
    inputs = {key: value for key, value in arguments.items() if key != "context"}
    context = dict(arguments.get("context", {}))
    intermediates, results = contract.compute(inputs)
    digest_source = json.dumps(
        {"method": method_id, "version": METHOD_VERSION, "inputs": inputs},
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    context_gaps = [
        name for name in ("case_id", "analysis_id", "evidence_ids", "units", "purpose")
        if not context.get(name)
    ]
    return {
        "calculation_id": f"calc-{sha256(digest_source).hexdigest()[:20]}",
        "method": method_id,
        "method_version": METHOD_VERSION,
        "formulas": list(contract.formulas),
        "inputs": inputs,
        "context": context,
        "intermediates": intermediates,
        "results": results,
        "mechanically_validated": [
            "registered method selected",
            "required inputs present",
            "calculation completed without a domain error",
        ],
        "context_gaps": context_gaps,
        "assumptions_not_established": list(COMMON_UNESTABLISHED),
        "authority_boundary": AUTHORITY_BOUNDARY,
    }
