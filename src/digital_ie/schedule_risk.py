"""Deterministic project-network and reproducible risk calculations.

The network kernel intentionally supports finish-to-start, zero-lag logic only.
Calendars, constraints, resources, and status-date treatment belong in a full
integrated master schedule engine and must not be inferred here.
"""

from __future__ import annotations

from math import ceil, fsum, isfinite
from random import Random
from statistics import fmean, pstdev
from typing import Mapping, Sequence


MAX_ITERATIONS = 100_000


def _number(name: str, value: object, *, nonnegative: bool = True) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    result = float(value)
    if not isfinite(result) or (nonnegative and result < 0):
        qualifier = "finite and nonnegative" if nonnegative else "finite"
        raise ValueError(f"{name} must be {qualifier}")
    return result


def _network(
    activities: Sequence[Mapping[str, object]],
) -> tuple[dict[str, float], dict[str, tuple[str, ...]], list[str]]:
    if not activities:
        raise ValueError("activities cannot be empty")
    durations: dict[str, float] = {}
    predecessors: dict[str, tuple[str, ...]] = {}
    for activity in activities:
        identifier = activity.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            raise ValueError("each activity requires a nonempty string id")
        if identifier in durations:
            raise ValueError(f"duplicate activity id: {identifier}")
        durations[identifier] = _number(
            f"duration for {identifier}", activity.get("duration")
        )
        raw_predecessors = activity.get("predecessors", ())
        if not isinstance(raw_predecessors, (list, tuple)) or any(
            not isinstance(item, str) for item in raw_predecessors
        ):
            raise ValueError(f"predecessors for {identifier} must be a string list")
        if len(set(raw_predecessors)) != len(raw_predecessors):
            raise ValueError(f"duplicate predecessor for {identifier}")
        predecessors[identifier] = tuple(raw_predecessors)
    for identifier, dependency_ids in predecessors.items():
        for dependency_id in dependency_ids:
            if dependency_id not in durations:
                raise ValueError(
                    f"activity {identifier} references missing predecessor {dependency_id}"
                )
            if dependency_id == identifier:
                raise ValueError(f"activity {identifier} cannot depend on itself")

    indegree = {identifier: len(items) for identifier, items in predecessors.items()}
    successors = {identifier: [] for identifier in durations}
    for identifier, dependency_ids in predecessors.items():
        for dependency_id in dependency_ids:
            successors[dependency_id].append(identifier)
    ready = sorted(identifier for identifier, degree in indegree.items() if degree == 0)
    order: list[str] = []
    while ready:
        identifier = ready.pop(0)
        order.append(identifier)
        for successor in sorted(successors[identifier]):
            indegree[successor] -= 1
            if indegree[successor] == 0:
                ready.append(successor)
                ready.sort()
    if len(order) != len(durations):
        raise ValueError("activity network contains a dependency cycle")
    return durations, predecessors, order


def critical_path(activities: Sequence[Mapping[str, object]]) -> dict[str, object]:
    """Run CPM forward/backward passes for finish-to-start, zero-lag logic."""
    durations, predecessors, order = _network(activities)
    successors: dict[str, list[str]] = {identifier: [] for identifier in durations}
    for identifier, dependency_ids in predecessors.items():
        for dependency_id in dependency_ids:
            successors[dependency_id].append(identifier)

    early_start: dict[str, float] = {}
    early_finish: dict[str, float] = {}
    for identifier in order:
        early_start[identifier] = max(
            (early_finish[item] for item in predecessors[identifier]), default=0.0
        )
        early_finish[identifier] = _number(
            f"early finish for {identifier}",
            early_start[identifier] + durations[identifier],
        )
    project_duration = max(early_finish.values())

    late_finish: dict[str, float] = {}
    late_start: dict[str, float] = {}
    for identifier in reversed(order):
        late_finish[identifier] = min(
            (late_start[item] for item in successors[identifier]),
            default=project_duration,
        )
        late_start[identifier] = late_finish[identifier] - durations[identifier]

    rows = []
    critical_ids = []
    for identifier in order:
        total_float = late_start[identifier] - early_start[identifier]
        free_float = min(
            (early_start[item] for item in successors[identifier]),
            default=project_duration,
        ) - early_finish[identifier]
        is_critical = abs(total_float) <= 1e-9
        if is_critical:
            critical_ids.append(identifier)
        rows.append(
            {
                "id": identifier,
                "duration": durations[identifier],
                "early_start": early_start[identifier],
                "early_finish": early_finish[identifier],
                "late_start": late_start[identifier],
                "late_finish": late_finish[identifier],
                "total_float": total_float,
                "free_float": free_float,
                "is_critical": is_critical,
            }
        )
    return {
        "project_duration": project_duration,
        "critical_activity_ids": critical_ids,
        "activities": rows,
    }


def pert_estimate(
    optimistic: float, most_likely: float, pessimistic: float
) -> dict[str, float]:
    """Return classic three-point PERT mean, variance, and standard deviation."""
    optimistic = _number("optimistic", optimistic)
    most_likely = _number("most likely", most_likely)
    pessimistic = _number("pessimistic", pessimistic)
    if not optimistic <= most_likely <= pessimistic:
        raise ValueError("PERT estimates must satisfy optimistic <= most likely <= pessimistic")
    standard_deviation = (pessimistic - optimistic) / 6
    expected_duration = _number(
        "expected duration", (optimistic + 4 * most_likely + pessimistic) / 6
    )
    return {
        "expected_duration": expected_duration,
        "variance": standard_deviation**2,
        "standard_deviation": standard_deviation,
    }


def _iterations(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("iterations must be an integer")
    if value < 1 or value > MAX_ITERATIONS:
        raise ValueError(f"iterations must be between 1 and {MAX_ITERATIONS}")
    return value


def _quantile(sorted_values: Sequence[float], probability: float) -> float:
    position = probability * (len(sorted_values) - 1)
    lower = int(position)
    upper = ceil(position)
    if lower == upper:
        return sorted_values[lower]
    fraction = position - lower
    return sorted_values[lower] + fraction * (
        sorted_values[upper] - sorted_values[lower]
    )


def simulate_schedule(
    activities: Sequence[Mapping[str, object]], iterations: int, seed: int
) -> dict[str, object]:
    """Sample triangular activity durations and rerun CPM with a local seed."""
    count = _iterations(iterations)
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")
    templates = []
    for activity in activities:
        identifier = activity.get("id")
        optimistic = _number(f"optimistic for {identifier}", activity.get("optimistic"))
        most_likely = _number(f"most likely for {identifier}", activity.get("most_likely"))
        pessimistic = _number(f"pessimistic for {identifier}", activity.get("pessimistic"))
        if not optimistic <= most_likely <= pessimistic:
            raise ValueError(
                f"estimates for {identifier} must satisfy optimistic <= most likely <= pessimistic"
            )
        templates.append((activity, optimistic, most_likely, pessimistic))
    # Validate identifiers and logic before consuming the random stream.
    validation_network = [
        {
            "id": item[0].get("id"),
            "duration": item[2],
            "predecessors": item[0].get("predecessors", ()),
        }
        for item in templates
    ]
    _network(validation_network)
    rng = Random(seed)
    durations = []
    critical_counts = {str(item[0]["id"]): 0 for item in templates}
    for _ in range(count):
        sample = [
            {
                "id": item[0]["id"],
                "duration": rng.triangular(item[1], item[3], item[2]),
                "predecessors": item[0].get("predecessors", ()),
            }
            for item in templates
        ]
        result = critical_path(sample)
        durations.append(float(result["project_duration"]))
        for identifier in result["critical_activity_ids"]:
            critical_counts[identifier] += 1
    durations.sort()
    return {
        "iterations": count,
        "seed": seed,
        "mean_duration": fmean(durations),
        "standard_deviation": pstdev(durations),
        "minimum_duration": durations[0],
        "p50_duration": _quantile(durations, 0.50),
        "p80_duration": _quantile(durations, 0.80),
        "p90_duration": _quantile(durations, 0.90),
        "p95_duration": _quantile(durations, 0.95),
        "maximum_duration": durations[-1],
        "criticality_index": {
            identifier: value / count for identifier, value in critical_counts.items()
        },
    }


def simulate_cost(
    cost_elements: Sequence[Mapping[str, object]], iterations: int, seed: int
) -> dict[str, object]:
    """Sample triangular base costs and optional Bernoulli discrete risks."""
    count = _iterations(iterations)
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")
    if not cost_elements:
        raise ValueError("cost elements cannot be empty")
    parsed = []
    identifiers: set[str] = set()
    for element in cost_elements:
        identifier = element.get("id")
        if not isinstance(identifier, str) or not identifier.strip() or identifier in identifiers:
            raise ValueError("cost element ids must be nonempty and unique")
        identifiers.add(identifier)
        low = _number(f"minimum cost for {identifier}", element.get("minimum"))
        mode = _number(f"most likely cost for {identifier}", element.get("most_likely"))
        high = _number(f"maximum cost for {identifier}", element.get("maximum"))
        if not low <= mode <= high:
            raise ValueError(f"cost range for {identifier} must satisfy minimum <= mode <= maximum")
        probability = _number(f"risk probability for {identifier}", element.get("risk_probability", 0))
        if probability > 1:
            raise ValueError("risk probability must be between 0 and 1")
        impact = _number(f"risk impact for {identifier}", element.get("risk_impact", 0))
        parsed.append((low, mode, high, probability, impact))
    rng = Random(seed)
    totals = []
    for _ in range(count):
        total = fsum(
            rng.triangular(low, high, mode) for low, mode, high, _, _ in parsed
        )
        total += fsum(
            impact for _, _, _, probability, impact in parsed if rng.random() < probability
        )
        totals.append(_number("simulated total cost", total))
    totals.sort()
    return {
        "iterations": count,
        "seed": seed,
        "mean_cost": fmean(totals),
        "standard_deviation": pstdev(totals),
        "minimum_cost": totals[0],
        "p50_cost": _quantile(totals, 0.50),
        "p80_cost": _quantile(totals, 0.80),
        "p90_cost": _quantile(totals, 0.90),
        "p95_cost": _quantile(totals, 0.95),
        "maximum_cost": totals[-1],
    }
