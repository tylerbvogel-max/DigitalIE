"""Deterministic production-flow calculations with explicit assumptions."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, factorial, fsum, isfinite, log, sqrt
from typing import Sequence


def _nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _positive(name: str, value: float) -> None:
    _nonnegative(name, value)
    if value == 0:
        raise ValueError(f"{name} must be positive")


@dataclass(frozen=True)
class ProductionPaceResult:
    takt_time: float
    demonstrated_capacity: float
    demand_utilization: float
    minimum_parallel_resources: int
    staffing_gap: int | None


def production_pace(
    available_time: float,
    demand: float,
    effective_cycle_time: float,
    installed_parallel_resources: int | None = None,
) -> ProductionPaceResult:
    """Calculate takt, idealized capacity, and minimum parallel resources."""
    _positive("available time", available_time)
    _positive("demand", demand)
    _positive("effective cycle time", effective_cycle_time)
    if installed_parallel_resources is not None and (
        isinstance(installed_parallel_resources, bool)
        or not isinstance(installed_parallel_resources, int)
        or installed_parallel_resources < 0
    ):
        raise ValueError("installed parallel resources must be a nonnegative integer")
    takt = available_time / demand
    minimum_resources = ceil(effective_cycle_time / takt)
    return ProductionPaceResult(
        takt_time=takt,
        demonstrated_capacity=available_time / effective_cycle_time,
        demand_utilization=effective_cycle_time / takt,
        minimum_parallel_resources=minimum_resources,
        staffing_gap=(
            minimum_resources - installed_parallel_resources
            if installed_parallel_resources is not None else None
        ),
    )


@dataclass(frozen=True)
class LineBalanceResult:
    station_loads: tuple[float, ...]
    cycle_time: float
    total_work_content: float
    line_efficiency: float
    balance_delay: float
    smoothness_index: float
    output_capacity: float


def line_balance(station_task_times: Sequence[Sequence[float]], available_time: float) -> LineBalanceResult:
    """Evaluate an existing station assignment without solving precedence."""
    _positive("available time", available_time)
    if not station_task_times:
        raise ValueError("at least one station is required")
    loads = []
    for station in station_task_times:
        if not station:
            raise ValueError("stations cannot be empty")
        for value in station:
            _positive("task time", value)
        loads.append(fsum(station))
    cycle = max(loads)
    work = fsum(loads)
    available_station_time = len(loads) * cycle
    efficiency = work / available_station_time
    return LineBalanceResult(
        station_loads=tuple(loads),
        cycle_time=cycle,
        total_work_content=work,
        line_efficiency=efficiency,
        balance_delay=1 - efficiency,
        smoothness_index=sqrt(fsum((cycle - load) ** 2 for load in loads)),
        output_capacity=available_time / cycle,
    )


@dataclass(frozen=True)
class OeeResult:
    availability: float
    performance: float
    quality: float
    oee: float
    fully_productive_time: float


def overall_equipment_effectiveness(
    planned_production_time: float,
    run_time: float,
    ideal_cycle_time: float,
    total_count: float,
    good_count: float,
) -> OeeResult:
    """Calculate OEE as availability times performance times quality."""
    _positive("planned production time", planned_production_time)
    _nonnegative("run time", run_time)
    _positive("ideal cycle time", ideal_cycle_time)
    _nonnegative("total count", total_count)
    _nonnegative("good count", good_count)
    if run_time > planned_production_time:
        raise ValueError("run time cannot exceed planned production time")
    if good_count > total_count:
        raise ValueError("good count cannot exceed total count")
    availability = run_time / planned_production_time
    performance = ideal_cycle_time * total_count / run_time if run_time else 0.0
    quality = good_count / total_count if total_count else 0.0
    if performance > 1 + 1e-12:
        raise ValueError("performance exceeds 1; verify ideal cycle time and count basis")
    return OeeResult(
        availability=availability,
        performance=performance,
        quality=quality,
        oee=availability * performance * quality,
        fully_productive_time=ideal_cycle_time * good_count,
    )


@dataclass(frozen=True)
class FlowResult:
    implied_wip: float | None
    implied_throughput: float | None
    implied_lead_time: float | None
    process_cycle_efficiency: float | None


def flow_metrics(
    *,
    wip: float | None = None,
    throughput: float | None = None,
    lead_time: float | None = None,
    value_added_time: float | None = None,
) -> FlowResult:
    """Apply Little's Law from exactly two measures and optionally calculate PCE."""
    supplied = {"wip": wip, "throughput": throughput, "lead time": lead_time}
    if sum(value is not None for value in supplied.values()) != 2:
        raise ValueError("provide exactly two of WIP, throughput, and lead time")
    for name, value in supplied.items():
        if value is not None:
            _positive(name, value)
    derived_wip = throughput * lead_time if wip is None else None
    derived_throughput = wip / lead_time if throughput is None else None
    derived_lead_time = wip / throughput if lead_time is None else None
    effective_lead_time = lead_time if lead_time is not None else derived_lead_time
    if value_added_time is not None:
        _nonnegative("value-added time", value_added_time)
        if effective_lead_time is None:
            raise ValueError("lead time must be supplied or derivable for PCE")
        if value_added_time > effective_lead_time:
            raise ValueError("value-added time cannot exceed lead time")
    return FlowResult(
        implied_wip=derived_wip,
        implied_throughput=derived_throughput,
        implied_lead_time=derived_lead_time,
        process_cycle_efficiency=(
            value_added_time / effective_lead_time
            if value_added_time is not None and effective_lead_time is not None else None
        ),
    )


def rolled_throughput_yield(step_yields: Sequence[float]) -> dict[str, float]:
    """Multiply first-pass yields expressed as proportions from zero to one."""
    if not step_yields:
        raise ValueError("at least one step yield is required")
    result = 1.0
    for value in step_yields:
        if not isfinite(value) or not 0 <= value <= 1:
            raise ValueError("step yields must be finite proportions from zero to one")
        result *= value
    return {"rolled_throughput_yield": result, "loss_probability": 1 - result}


@dataclass(frozen=True)
class QueueResult:
    utilization: float
    probability_wait: float
    average_queue_count: float
    average_system_count: float
    average_queue_time: float
    average_system_time: float


def mm1_queue(arrival_rate: float, service_rate: float) -> QueueResult:
    """Calculate steady-state M/M/1 measures for consistent time units."""
    _positive("arrival rate", arrival_rate)
    _positive("service rate", service_rate)
    if arrival_rate >= service_rate:
        raise ValueError("M/M/1 requires arrival rate below service rate")
    utilization = arrival_rate / service_rate
    queue_count = utilization**2 / (1 - utilization)
    return QueueResult(
        utilization=utilization,
        probability_wait=utilization,
        average_queue_count=queue_count,
        average_system_count=utilization / (1 - utilization),
        average_queue_time=queue_count / arrival_rate,
        average_system_time=1 / (service_rate - arrival_rate),
    )


def mmc_queue(arrival_rate: float, service_rate_per_server: float, servers: int) -> QueueResult:
    """Calculate steady-state M/M/c measures using Erlang C."""
    _positive("arrival rate", arrival_rate)
    _positive("service rate per server", service_rate_per_server)
    if isinstance(servers, bool) or not isinstance(servers, int) or servers <= 0:
        raise ValueError("servers must be a positive integer")
    offered_load = arrival_rate / service_rate_per_server
    utilization = offered_load / servers
    if utilization >= 1:
        raise ValueError("M/M/c requires arrival rate below total service capacity")
    series = fsum(offered_load**n / factorial(n) for n in range(servers))
    tail = offered_load**servers / (factorial(servers) * (1 - utilization))
    probability_zero = 1 / (series + tail)
    probability_wait = tail * probability_zero
    queue_count = probability_wait * utilization / (1 - utilization)
    queue_time = queue_count / arrival_rate
    return QueueResult(
        utilization=utilization,
        probability_wait=probability_wait,
        average_queue_count=queue_count,
        average_system_count=queue_count + offered_load,
        average_queue_time=queue_time,
        average_system_time=queue_time + 1 / service_rate_per_server,
    )


@dataclass(frozen=True)
class LearningCurveResult:
    exponent: float
    unit_values: tuple[float, ...]
    total_value: float
    average_value: float


def unit_learning_curve(first_unit_value: float, learning_rate: float, units: int) -> LearningCurveResult:
    """Apply the Crawford/unit learning model Y_x = Y_1 * x^b."""
    _positive("first-unit value", first_unit_value)
    if not isfinite(learning_rate) or not 0 < learning_rate <= 1:
        raise ValueError("learning rate must be a proportion above zero and at most one")
    if isinstance(units, bool) or not isinstance(units, int) or units <= 0:
        raise ValueError("units must be a positive integer")
    exponent = log(learning_rate) / log(2)
    values = tuple(first_unit_value * number**exponent for number in range(1, units + 1))
    total = fsum(values)
    return LearningCurveResult(exponent, values, total, total / units)
