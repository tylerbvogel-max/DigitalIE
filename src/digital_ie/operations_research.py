"""Small, transparent operations-research calculations without a solver dependency."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from math import fsum, isfinite
from typing import Sequence


def _finite(name: str, value: float) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def facility_center_of_gravity(
    coordinates: Sequence[Sequence[float]], weights: Sequence[float]
) -> dict[str, float]:
    """Calculate a weighted planar center of gravity for candidate screening."""
    if not coordinates or len(coordinates) != len(weights):
        raise ValueError("coordinates and weights must have equal positive length")
    if any(len(point) != 2 for point in coordinates):
        raise ValueError("each coordinate must contain x and y")
    for point in coordinates:
        for value in point:
            _finite("coordinate", value)
    for weight in weights:
        if not isfinite(weight) or weight < 0:
            raise ValueError("weights must be finite and nonnegative")
    total_weight = fsum(weights)
    if total_weight == 0:
        raise ValueError("total weight must be positive")
    return {
        "x": fsum(point[0] * weight for point, weight in zip(coordinates, weights)) / total_weight,
        "y": fsum(point[1] * weight for point, weight in zip(coordinates, weights)) / total_weight,
        "total_weight": total_weight,
    }


def weighted_decision_scores(
    alternative_names: Sequence[str],
    scores: Sequence[Sequence[float]],
    weights: Sequence[float],
) -> dict[str, object]:
    """Rank alternatives whose criterion scores already share a declared scale."""
    if not alternative_names or len(alternative_names) != len(scores):
        raise ValueError("alternative names and score rows must have equal positive length")
    if not weights or any(len(row) != len(weights) for row in scores):
        raise ValueError("each score row must match the positive-length weight vector")
    if len(set(alternative_names)) != len(alternative_names) or any(not name for name in alternative_names):
        raise ValueError("alternative names must be unique and nonempty")
    for value in (*weights, *(entry for row in scores for entry in row)):
        if not isfinite(value) or value < 0:
            raise ValueError("scores and weights must be finite and nonnegative")
    total_weight = fsum(weights)
    if total_weight == 0:
        raise ValueError("total weight must be positive")
    normalized_weights = tuple(weight / total_weight for weight in weights)
    totals = {
        name: fsum(score * weight for score, weight in zip(row, normalized_weights))
        for name, row in zip(alternative_names, scores)
    }
    ranking = tuple(sorted(totals, key=lambda name: (-totals[name], name)))
    return {"normalized_weights": normalized_weights, "scores": totals, "ranking": ranking}


@dataclass(frozen=True)
class AssignmentResult:
    assignments: tuple[tuple[int, int], ...]
    total_cost: float
    alternatives_evaluated: int


def bounded_assignment(cost_matrix: Sequence[Sequence[float]]) -> AssignmentResult:
    """Solve a small rectangular assignment problem by complete enumeration."""
    if not cost_matrix or not cost_matrix[0]:
        raise ValueError("cost matrix cannot be empty")
    rows = len(cost_matrix)
    columns = len(cost_matrix[0])
    if rows > 8:
        raise ValueError("enumeration is limited to eight rows")
    if columns < rows or any(len(row) != columns for row in cost_matrix):
        raise ValueError("matrix must be rectangular with at least as many columns as rows")
    for value in (entry for row in cost_matrix for entry in row):
        _finite("assignment cost", value)
    best_columns = None
    best_cost = None
    evaluated = 0
    for selected in permutations(range(columns), rows):
        cost = fsum(cost_matrix[row][column] for row, column in enumerate(selected))
        evaluated += 1
        if best_cost is None or cost < best_cost:
            best_cost = cost
            best_columns = selected
    if best_columns is None or best_cost is None:
        raise RuntimeError("assignment enumeration produced no candidates")
    return AssignmentResult(
        assignments=tuple(enumerate(best_columns)),
        total_cost=best_cost,
        alternatives_evaluated=evaluated,
    )


@dataclass(frozen=True)
class SequenceResult:
    order: tuple[str, ...]
    completion_times: tuple[float, ...]
    lateness: tuple[float, ...]
    tardiness: tuple[float, ...]
    makespan: float
    average_completion_time: float
    average_tardiness: float
    maximum_tardiness: float
    jobs_late: int


def single_machine_sequence(
    job_names: Sequence[str],
    processing_times: Sequence[float],
    due_dates: Sequence[float],
    rule: str,
) -> SequenceResult:
    """Evaluate FCFS, shortest-processing-time, or earliest-due-date order."""
    if not job_names or len(job_names) != len(processing_times) or len(job_names) != len(due_dates):
        raise ValueError("job names, processing times, and due dates must have equal positive length")
    if len(set(job_names)) != len(job_names) or any(not name for name in job_names):
        raise ValueError("job names must be unique and nonempty")
    for value in processing_times:
        if not isfinite(value) or value <= 0:
            raise ValueError("processing times must be finite and positive")
    for value in due_dates:
        _finite("due date", value)
    if rule not in {"fcfs", "spt", "edd"}:
        raise ValueError("rule must be fcfs, spt, or edd")
    indices = list(range(len(job_names)))
    if rule == "spt":
        indices.sort(key=lambda index: (processing_times[index], index))
    elif rule == "edd":
        indices.sort(key=lambda index: (due_dates[index], index))
    elapsed = 0.0
    completion = []
    lateness = []
    tardiness = []
    for index in indices:
        elapsed += processing_times[index]
        job_lateness = elapsed - due_dates[index]
        completion.append(elapsed)
        lateness.append(job_lateness)
        tardiness.append(max(0.0, job_lateness))
    count = len(indices)
    return SequenceResult(
        order=tuple(job_names[index] for index in indices),
        completion_times=tuple(completion),
        lateness=tuple(lateness),
        tardiness=tuple(tardiness),
        makespan=elapsed,
        average_completion_time=fsum(completion) / count,
        average_tardiness=fsum(tardiness) / count,
        maximum_tardiness=max(tardiness),
        jobs_late=sum(value > 0 for value in tardiness),
    )
