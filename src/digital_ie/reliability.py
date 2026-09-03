"""Reliability and maintainability arithmetic with explicit model assumptions."""

from __future__ import annotations

from math import ceil, exp, fsum, gamma, isfinite, log, prod
from typing import Sequence


def _nonnegative(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    result = float(value)
    if not isfinite(result) or result < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def _positive(name: str, value: float) -> float:
    result = _nonnegative(name, value)
    if result <= 0:
        raise ValueError(f"{name} must be positive")
    return result


def _probability(name: str, value: float, *, open_interval: bool = False) -> float:
    result = _nonnegative(name, value)
    valid = 0 < result < 1 if open_interval else 0 <= result <= 1
    if not valid:
        interval = "between 0 and 1 exclusive" if open_interval else "between 0 and 1"
        raise ValueError(f"{name} must be {interval}")
    return result


def observed_metrics(
    operating_time: float,
    failures: int,
    repair_time: float = 0,
) -> dict[str, float | None]:
    """Calculate observed repairable-item MTBF, MTTR, and inherent availability."""
    operating_time = _nonnegative("operating time", operating_time)
    repair_time = _nonnegative("repair time", repair_time)
    if isinstance(failures, bool) or not isinstance(failures, int) or failures < 0:
        raise ValueError("failures must be a nonnegative integer")
    if failures and operating_time == 0:
        raise ValueError("positive failures require positive operating time")
    if repair_time and failures == 0:
        raise ValueError("positive repair time requires at least one failure")
    mtbf = operating_time / failures if failures else None
    mttr = repair_time / failures if failures else None
    availability = (
        operating_time / (operating_time + repair_time)
        if operating_time + repair_time > 0 else None
    )
    return {
        "mtbf": mtbf,
        "mttr": mttr,
        "failure_rate": failures / operating_time if operating_time > 0 else None,
        "observed_inherent_availability": availability,
    }


def observed_mttf(total_time_on_test: float, failures: int) -> float | None:
    """Calculate observed nonrepairable-item MTTF; zero failures is undefined."""
    total_time = _nonnegative("total time on test", total_time_on_test)
    if isinstance(failures, bool) or not isinstance(failures, int) or failures < 0:
        raise ValueError("failures must be a nonnegative integer")
    if failures and total_time == 0:
        raise ValueError("positive failures require positive total time on test")
    return total_time / failures if failures else None


def operational_availability(uptime: float, total_downtime: float) -> float | None:
    """Calculate uptime divided by uptime plus all included downtime."""
    uptime = _nonnegative("uptime", uptime)
    downtime = _nonnegative("total downtime", total_downtime)
    return uptime / (uptime + downtime) if uptime + downtime > 0 else None


def inherent_availability(mtbf: float, mttr: float) -> float:
    """Calculate Ai = MTBF / (MTBF + MTTR)."""
    mtbf = _positive("MTBF", mtbf)
    mttr = _nonnegative("MTTR", mttr)
    return mtbf / (mtbf + mttr)


def exponential_model(time: float, *, failure_rate: float | None = None, mttf: float | None = None) -> dict[str, float]:
    """Evaluate a constant-hazard exponential life model."""
    time = _nonnegative("time", time)
    if (failure_rate is None) == (mttf is None):
        raise ValueError("provide exactly one of failure_rate or MTTF")
    rate = _positive("failure rate", failure_rate) if failure_rate is not None else 1 / _positive("MTTF", mttf)
    cumulative_hazard = rate * time
    if not isfinite(cumulative_hazard):
        raise ValueError("failure rate and time produce a nonfinite cumulative hazard")
    reliability = exp(-cumulative_hazard)
    return {
        "failure_rate": rate,
        "mttf": 1 / rate,
        "reliability": reliability,
        "cdf": 1 - reliability,
        "hazard": rate,
        "cumulative_hazard": cumulative_hazard,
    }


def weibull_model(
    time: float, scale: float, shape: float
) -> dict[str, float | None]:
    """Evaluate a two-parameter Weibull life model with zero location."""
    time = _nonnegative("time", time)
    scale = _positive("scale", scale)
    shape = _positive("shape", shape)
    normalized = time / scale
    try:
        cumulative_hazard = normalized**shape
        reliability = exp(-cumulative_hazard)
        mean_life = scale * gamma(1 + 1 / shape)
    except OverflowError as error:
        raise ValueError("Weibull parameters produce nonfinite outputs") from error
    if time == 0:
        hazard = 0.0 if shape > 1 else (1 / scale if shape == 1 else None)
        density = hazard
    else:
        hazard = (shape / scale) * normalized ** (shape - 1)
        density = hazard * reliability
    for value in (cumulative_hazard, reliability, mean_life, hazard, density):
        if value is not None and not isfinite(value):
            raise ValueError("Weibull parameters produce nonfinite outputs")
    return {
        "reliability": reliability,
        "cdf": 1 - reliability,
        "pdf": density,
        "hazard": hazard,
        "cumulative_hazard": cumulative_hazard,
        "mean_life": mean_life,
    }


def series_reliability(component_reliabilities: Sequence[float]) -> float:
    """Calculate independent series-system reliability."""
    if not component_reliabilities:
        raise ValueError("component reliabilities cannot be empty")
    return prod(_probability("component reliability", item) for item in component_reliabilities)


def parallel_reliability(component_reliabilities: Sequence[float]) -> float:
    """Calculate independent active-parallel system reliability."""
    if not component_reliabilities:
        raise ValueError("component reliabilities cannot be empty")
    return 1 - prod(1 - _probability("component reliability", item) for item in component_reliabilities)


def k_out_of_n_reliability(component_reliabilities: Sequence[float], required: int) -> float:
    """Calculate independent heterogeneous k-out-of-n reliability by convolution."""
    if not component_reliabilities:
        raise ValueError("component reliabilities cannot be empty")
    if isinstance(required, bool) or not isinstance(required, int) or not 1 <= required <= len(component_reliabilities):
        raise ValueError("required must be an integer from 1 through component count")
    probabilities = [1.0] + [0.0] * len(component_reliabilities)
    for reliability in component_reliabilities:
        reliability = _probability("component reliability", reliability)
        updated = [0.0] * len(probabilities)
        for successes in range(len(probabilities)):
            updated[successes] += probabilities[successes] * (1 - reliability)
            if successes + 1 < len(probabilities):
                updated[successes + 1] += probabilities[successes] * reliability
        probabilities = updated
    return fsum(probabilities[required:])


def zero_failure_binomial_sample_size(
    reliability_requirement: float, confidence: float
) -> int:
    """Return units needed for a zero-failure, fixed-mission demonstration."""
    reliability = _probability("reliability requirement", reliability_requirement, open_interval=True)
    confidence = _probability("confidence", confidence, open_interval=True)
    return ceil(log(1 - confidence) / log(reliability))


def zero_failure_exponential_test_time(mtbf_requirement: float, confidence: float) -> float:
    """Return accumulated test time for a zero-failure exponential demonstration."""
    mtbf = _positive("MTBF requirement", mtbf_requirement)
    confidence = _probability("confidence", confidence, open_interval=True)
    return -mtbf * log(1 - confidence)
