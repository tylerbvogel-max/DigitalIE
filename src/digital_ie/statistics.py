"""Transparent statistical calculations used by DigitalIE examples.

These functions calculate statistics; they do not validate sampling, measurement,
distributional assumptions, causal interpretation, or decision authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, sqrt
from typing import Sequence


@dataclass(frozen=True)
class RegressionResult:
    intercept: float
    slope: float
    correlation: float
    determination: float
    residuals: tuple[float, ...]
    sse: float
    ssr: float
    mse: float
    slope_standard_error: float
    slope_t: float


@dataclass(frozen=True)
class AnovaResult:
    grand_mean: float
    between_sum_squares: float
    within_sum_squares: float
    between_degrees_freedom: int
    within_degrees_freedom: int
    f_statistic: float


def _require_size(values: Sequence[float], minimum: int, name: str) -> None:
    if len(values) < minimum:
        raise ValueError(f"{name} requires at least {minimum} observations")


def mean(values: Sequence[float]) -> float:
    _require_size(values, 1, "mean")
    return fsum(values) / len(values)


def sample_variance(values: Sequence[float]) -> float:
    _require_size(values, 2, "sample variance")
    center = mean(values)
    return fsum((value - center) ** 2 for value in values) / (len(values) - 1)


def sample_standard_deviation(values: Sequence[float]) -> float:
    return sqrt(sample_variance(values))


def standard_error_mean(values: Sequence[float]) -> float:
    return sample_standard_deviation(values) / sqrt(len(values))


def one_sample_z_statistic(sample_mean: float, null_mean: float, sigma: float, n: int) -> float:
    if sigma <= 0 or n <= 0:
        raise ValueError("sigma and n must be positive")
    return (sample_mean - null_mean) / (sigma / sqrt(n))


def one_sample_t_statistic(values: Sequence[float], null_mean: float) -> float:
    standard_error = standard_error_mean(values)
    if standard_error == 0:
        raise ValueError("one-sample t requires nonzero sample variation")
    return (mean(values) - null_mean) / standard_error


def paired_t_statistic(
    before: Sequence[float], after: Sequence[float], null_difference: float = 0.0
) -> float:
    if len(before) != len(after):
        raise ValueError("paired t samples must have equal length")
    differences = tuple(after_value - before_value for before_value, after_value in zip(before, after))
    return one_sample_t_statistic(differences, null_difference)


def one_proportion_z_statistic(events: int, n: int, null_proportion: float) -> float:
    if n <= 0 or events < 0 or events > n or not 0 < null_proportion < 1:
        raise ValueError("proportion inputs require 0 <= events <= n and 0 < p0 < 1")
    observed = events / n
    return (observed - null_proportion) / sqrt(null_proportion * (1 - null_proportion) / n)


def two_proportion_z_statistic(events_1: int, n_1: int, events_2: int, n_2: int) -> float:
    if n_1 <= 0 or n_2 <= 0 or not 0 <= events_1 <= n_1 or not 0 <= events_2 <= n_2:
        raise ValueError("two-proportion inputs require valid event counts and positive samples")
    pooled = (events_1 + events_2) / (n_1 + n_2)
    standard_error = sqrt(pooled * (1 - pooled) * (1 / n_1 + 1 / n_2))
    if standard_error == 0:
        raise ValueError("two-proportion z requires nonzero pooled standard error")
    return (events_1 / n_1 - events_2 / n_2) / standard_error


def wilson_proportion_interval(events: int, n: int, z_critical: float) -> tuple[float, float]:
    if n <= 0 or events < 0 or events > n or z_critical <= 0:
        raise ValueError("Wilson interval requires valid counts and positive critical value")
    proportion = events / n
    denominator = 1 + z_critical**2 / n
    center = (proportion + z_critical**2 / (2 * n)) / denominator
    half_width = z_critical * sqrt(
        proportion * (1 - proportion) / n + z_critical**2 / (4 * n**2)
    ) / denominator
    return center - half_width, center + half_width


def welch_t_statistic(
    first: Sequence[float], second: Sequence[float], null_difference: float = 0.0
) -> tuple[float, float]:
    _require_size(first, 2, "Welch t first group")
    _require_size(second, 2, "Welch t second group")
    first_term = sample_variance(first) / len(first)
    second_term = sample_variance(second) / len(second)
    standard_error = sqrt(first_term + second_term)
    if standard_error == 0:
        raise ValueError("Welch t requires nonzero estimated standard error")
    statistic = (mean(first) - mean(second) - null_difference) / standard_error
    numerator = (first_term + second_term) ** 2
    denominator = first_term**2 / (len(first) - 1) + second_term**2 / (len(second) - 1)
    return statistic, numerator / denominator


def chi_square_independence(observed: Sequence[Sequence[int]]) -> tuple[float, int]:
    if len(observed) < 2 or any(len(row) < 2 for row in observed):
        raise ValueError("chi-square table requires at least two rows and columns")
    column_count = len(observed[0])
    if any(len(row) != column_count for row in observed):
        raise ValueError("chi-square table must be rectangular")
    if any(value < 0 for row in observed for value in row):
        raise ValueError("chi-square counts cannot be negative")
    row_totals = tuple(fsum(row) for row in observed)
    column_totals = tuple(fsum(row[column] for row in observed) for column in range(column_count))
    total = fsum(row_totals)
    if total <= 0 or any(value <= 0 for value in row_totals + column_totals):
        raise ValueError("chi-square table margins must be positive")
    statistic = 0.0
    for row_index, row in enumerate(observed):
        for column_index, actual in enumerate(row):
            expected = row_totals[row_index] * column_totals[column_index] / total
            statistic += (actual - expected) ** 2 / expected
    return statistic, (len(observed) - 1) * (column_count - 1)


def one_way_anova(groups: Sequence[Sequence[float]]) -> AnovaResult:
    if len(groups) < 2 or any(len(group) < 2 for group in groups):
        raise ValueError("ANOVA requires at least two groups with two observations each")
    all_values = tuple(value for group in groups for value in group)
    grand_mean = mean(all_values)
    between = fsum(len(group) * (mean(group) - grand_mean) ** 2 for group in groups)
    within = fsum(fsum((value - mean(group)) ** 2 for value in group) for group in groups)
    between_df = len(groups) - 1
    within_df = len(all_values) - len(groups)
    within_mean_square = within / within_df
    if within_mean_square == 0:
        raise ValueError("ANOVA F statistic requires nonzero within-group variation")
    f_statistic = (between / between_df) / within_mean_square
    return AnovaResult(grand_mean, between, within, between_df, within_df, f_statistic)


def simple_linear_regression(x: Sequence[float], y: Sequence[float]) -> RegressionResult:
    if len(x) != len(y):
        raise ValueError("regression x and y must have equal length")
    _require_size(x, 3, "simple linear regression")
    x_mean, y_mean = mean(x), mean(y)
    sxx = fsum((value - x_mean) ** 2 for value in x)
    syy = fsum((value - y_mean) ** 2 for value in y)
    sxy = fsum((x_value - x_mean) * (y_value - y_mean) for x_value, y_value in zip(x, y))
    if sxx == 0 or syy == 0:
        raise ValueError("regression requires variation in x and y")
    slope = sxy / sxx
    intercept = y_mean - slope * x_mean
    fitted = tuple(intercept + slope * value for value in x)
    residuals = tuple(actual - predicted for actual, predicted in zip(y, fitted))
    sse = fsum(value**2 for value in residuals)
    ssr = fsum((value - y_mean) ** 2 for value in fitted)
    mse = sse / (len(x) - 2)
    slope_standard_error = sqrt(mse / sxx)
    correlation = sxy / sqrt(sxx * syy)
    slope_t = slope / slope_standard_error if slope_standard_error else float("inf")
    return RegressionResult(
        intercept, slope, correlation, correlation**2, residuals, sse, ssr,
        mse, slope_standard_error, slope_t,
    )
