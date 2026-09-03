"""Deterministic quality-engineering calculations.

The functions expose arithmetic, not acceptance authority. Control-chart,
capability, measurement-system, sampling, and experiment conclusions still
depend on valid study design and process knowledge.
"""

from __future__ import annotations

from itertools import combinations
from math import comb, fsum, isfinite, sqrt
from statistics import mean, stdev
from typing import Sequence


def _number(name: str, value: float, *, minimum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    result = float(value)
    if not isfinite(result) or (minimum is not None and result < minimum):
        qualifier = f" and at least {minimum}" if minimum is not None else ""
        raise ValueError(f"{name} must be finite{qualifier}")
    return result


def _count(name: str, value: int, *, positive: bool = False) -> int:
    lower = 1 if positive else 0
    if isinstance(value, bool) or not isinstance(value, int) or value < lower:
        qualifier = "positive" if positive else "nonnegative"
        raise ValueError(f"{name} must be a {qualifier} integer")
    return value


def _series(name: str, values: Sequence[float], *, minimum_length: int = 1) -> list[float]:
    if len(values) < minimum_length:
        raise ValueError(f"{name} must contain at least {minimum_length} values")
    return [_number(f"{name}[{index}]", value) for index, value in enumerate(values)]


def individuals_moving_range(
    values: Sequence[float],
    *,
    d2: float = 1.128,
    mr_lower_factor: float = 0.0,
    mr_upper_factor: float = 3.267,
) -> dict[str, object]:
    """Calculate Individuals and moving-range chart center lines and limits."""
    observations = _series("values", values, minimum_length=2)
    d2_value = _number("d2", d2, minimum=0.0)
    if d2_value == 0:
        raise ValueError("d2 must be positive")
    lower_factor = _number("MR lower factor", mr_lower_factor, minimum=0.0)
    upper_factor = _number("MR upper factor", mr_upper_factor, minimum=0.0)
    moving_ranges = [abs(current - prior) for prior, current in zip(observations, observations[1:])]
    center = mean(observations)
    mr_center = mean(moving_ranges)
    sigma = mr_center / d2_value
    return {
        "individual_values": observations,
        "moving_ranges": moving_ranges,
        "individual_center_line": center,
        "individual_lower_control_limit": center - 3 * sigma,
        "individual_upper_control_limit": center + 3 * sigma,
        "estimated_within_sigma": sigma,
        "moving_range_center_line": mr_center,
        "moving_range_lower_control_limit": lower_factor * mr_center,
        "moving_range_upper_control_limit": upper_factor * mr_center,
    }


def _balanced_subgroups(subgroups: Sequence[Sequence[float]]) -> list[list[float]]:
    if len(subgroups) < 2:
        raise ValueError("at least two subgroups are required")
    rows = [_series(f"subgroups[{index}]", row, minimum_length=2) for index, row in enumerate(subgroups)]
    if len({len(row) for row in rows}) != 1:
        raise ValueError("subgroups must have equal size")
    return rows


def xbar_r_chart(
    subgroups: Sequence[Sequence[float]],
    *,
    a2: float,
    d3: float,
    d4: float,
    d2: float | None = None,
) -> dict[str, object]:
    """Calculate X-bar and R chart limits using caller-supplied constants."""
    rows = _balanced_subgroups(subgroups)
    constants = [_number(name, value, minimum=0.0) for name, value in (("A2", a2), ("D3", d3), ("D4", d4))]
    subgroup_means = [mean(row) for row in rows]
    subgroup_ranges = [max(row) - min(row) for row in rows]
    grand_mean = mean(subgroup_means)
    average_range = mean(subgroup_ranges)
    result: dict[str, object] = {
        "subgroup_size": len(rows[0]),
        "subgroup_means": subgroup_means,
        "subgroup_ranges": subgroup_ranges,
        "xbar_center_line": grand_mean,
        "xbar_lower_control_limit": grand_mean - constants[0] * average_range,
        "xbar_upper_control_limit": grand_mean + constants[0] * average_range,
        "range_center_line": average_range,
        "range_lower_control_limit": constants[1] * average_range,
        "range_upper_control_limit": constants[2] * average_range,
    }
    if d2 is not None:
        d2_value = _number("d2", d2, minimum=0.0)
        if d2_value == 0:
            raise ValueError("d2 must be positive")
        result["estimated_within_sigma"] = average_range / d2_value
    return result


def xbar_s_chart(
    subgroups: Sequence[Sequence[float]], *, a3: float, b3: float, b4: float
) -> dict[str, object]:
    """Calculate X-bar and S chart limits using caller-supplied constants."""
    rows = _balanced_subgroups(subgroups)
    constants = [_number(name, value, minimum=0.0) for name, value in (("A3", a3), ("B3", b3), ("B4", b4))]
    subgroup_means = [mean(row) for row in rows]
    subgroup_stdevs = [stdev(row) for row in rows]
    grand_mean = mean(subgroup_means)
    average_stdev = mean(subgroup_stdevs)
    return {
        "subgroup_size": len(rows[0]),
        "subgroup_means": subgroup_means,
        "subgroup_standard_deviations": subgroup_stdevs,
        "xbar_center_line": grand_mean,
        "xbar_lower_control_limit": grand_mean - constants[0] * average_stdev,
        "xbar_upper_control_limit": grand_mean + constants[0] * average_stdev,
        "standard_deviation_center_line": average_stdev,
        "standard_deviation_lower_control_limit": constants[1] * average_stdev,
        "standard_deviation_upper_control_limit": constants[2] * average_stdev,
    }


def p_chart(nonconforming: Sequence[int], sample_sizes: Sequence[int], *, sigma_width: float = 3.0) -> dict[str, object]:
    """Calculate p-chart proportions and possibly varying control limits."""
    if not nonconforming or len(nonconforming) != len(sample_sizes):
        raise ValueError("counts and sample sizes must have equal positive length")
    counts = [_count(f"nonconforming[{index}]", value) for index, value in enumerate(nonconforming)]
    sizes = [_count(f"sample_sizes[{index}]", value, positive=True) for index, value in enumerate(sample_sizes)]
    if any(count > size for count, size in zip(counts, sizes)):
        raise ValueError("nonconforming count cannot exceed its sample size")
    width = _number("sigma width", sigma_width, minimum=0.0)
    p_bar = fsum(counts) / fsum(sizes)
    proportions = [count / size for count, size in zip(counts, sizes)]
    standard_errors = [sqrt(p_bar * (1 - p_bar) / size) for size in sizes]
    return {
        "proportions": proportions,
        "center_line": p_bar,
        "lower_control_limits": [max(0.0, p_bar - width * error) for error in standard_errors],
        "upper_control_limits": [min(1.0, p_bar + width * error) for error in standard_errors],
    }


def np_chart(nonconforming: Sequence[int], sample_size: int, *, sigma_width: float = 3.0) -> dict[str, object]:
    """Calculate an np chart for constant sample size."""
    size = _count("sample size", sample_size, positive=True)
    counts = [_count(f"nonconforming[{index}]", value) for index, value in enumerate(nonconforming)]
    if not counts or any(value > size for value in counts):
        raise ValueError("counts must be nonempty and cannot exceed sample size")
    width = _number("sigma width", sigma_width, minimum=0.0)
    p_bar = fsum(counts) / (len(counts) * size)
    center = size * p_bar
    spread = width * sqrt(size * p_bar * (1 - p_bar))
    return {
        "counts": counts,
        "fraction_nonconforming": p_bar,
        "center_line": center,
        "lower_control_limit": max(0.0, center - spread),
        "upper_control_limit": min(float(size), center + spread),
    }


def c_chart(nonconformities: Sequence[int], *, sigma_width: float = 3.0) -> dict[str, object]:
    """Calculate a c chart for equal inspection opportunities."""
    counts = [_count(f"nonconformities[{index}]", value) for index, value in enumerate(nonconformities)]
    if not counts:
        raise ValueError("nonconformities cannot be empty")
    width = _number("sigma width", sigma_width, minimum=0.0)
    center = mean(counts)
    spread = width * sqrt(center)
    return {
        "counts": counts,
        "center_line": center,
        "lower_control_limit": max(0.0, center - spread),
        "upper_control_limit": center + spread,
    }


def u_chart(nonconformities: Sequence[int], inspection_units: Sequence[float], *, sigma_width: float = 3.0) -> dict[str, object]:
    """Calculate a u chart for varying inspection-unit exposure."""
    if not nonconformities or len(nonconformities) != len(inspection_units):
        raise ValueError("counts and inspection units must have equal positive length")
    counts = [_count(f"nonconformities[{index}]", value) for index, value in enumerate(nonconformities)]
    units = [_number(f"inspection_units[{index}]", value, minimum=0.0) for index, value in enumerate(inspection_units)]
    if any(value == 0 for value in units):
        raise ValueError("inspection units must be positive")
    width = _number("sigma width", sigma_width, minimum=0.0)
    u_bar = fsum(counts) / fsum(units)
    rates = [count / unit for count, unit in zip(counts, units)]
    errors = [sqrt(u_bar / unit) for unit in units]
    return {
        "nonconformities_per_unit": rates,
        "center_line": u_bar,
        "lower_control_limits": [max(0.0, u_bar - width * error) for error in errors],
        "upper_control_limits": [u_bar + width * error for error in errors],
    }


def capability_indices(
    *, mean_value: float, within_sigma: float, overall_sigma: float, lsl: float, usl: float
) -> dict[str, float]:
    """Calculate two-sided Cp/Cpk and Pp/Ppk from declared sigma estimates."""
    process_mean = _number("mean", mean_value)
    within = _number("within sigma", within_sigma, minimum=0.0)
    overall = _number("overall sigma", overall_sigma, minimum=0.0)
    lower = _number("LSL", lsl)
    upper = _number("USL", usl)
    if within == 0 or overall == 0:
        raise ValueError("sigma estimates must be positive")
    if lower >= upper:
        raise ValueError("LSL must be less than USL")
    return {
        "cp": (upper - lower) / (6 * within),
        "cpk": min((upper - process_mean) / (3 * within), (process_mean - lower) / (3 * within)),
        "pp": (upper - lower) / (6 * overall),
        "ppk": min((upper - process_mean) / (3 * overall), (process_mean - lower) / (3 * overall)),
    }


def yield_metrics(
    *,
    units: int,
    defects: int,
    opportunities_per_unit: int,
    step_yields: Sequence[float],
    conforming_units: int | None = None,
) -> dict[str, float | None]:
    """Calculate unit yield, DPU, DPO, DPMO, and rolled throughput yield."""
    unit_count = _count("units", units, positive=True)
    defect_count = _count("defects", defects)
    opportunities = _count("opportunities per unit", opportunities_per_unit, positive=True)
    yields = _series("step yields", step_yields)
    if any(value < 0 or value > 1 for value in yields):
        raise ValueError("step yields must be proportions from zero through one")
    conforming = None
    if conforming_units is not None:
        conforming = _count("conforming units", conforming_units)
        if conforming > unit_count:
            raise ValueError("conforming units cannot exceed total units")
    dpu = defect_count / unit_count
    dpo = defect_count / (unit_count * opportunities)
    return {
        "unit_yield": conforming / unit_count if conforming is not None else None,
        "defects_per_unit": dpu,
        "defects_per_opportunity": dpo,
        "defects_per_million_opportunities": dpo * 1_000_000,
        "rolled_throughput_yield": _product(yields),
    }


def _product(values: Sequence[float]) -> float:
    result = 1.0
    for value in values:
        result *= value
    return result


def crossed_gage_rr_anova(measurements: Sequence[Sequence[Sequence[float]]]) -> dict[str, float | int]:
    """Estimate variance components for a balanced crossed part/operator study."""
    data, part_count, operator_count, repeat_count = _gage_data(measurements)
    means = _gage_means(data, operator_count)
    grand, part_means, operator_means, cell_means = means
    ss_part = operator_count * repeat_count * fsum((value - grand) ** 2 for value in part_means)
    ss_operator = part_count * repeat_count * fsum((value - grand) ** 2 for value in operator_means)
    ss_interaction = repeat_count * fsum(
        (cell_means[p][o] - part_means[p] - operator_means[o] + grand) ** 2
        for p in range(part_count)
        for o in range(operator_count)
    )
    ss_repeat = fsum(
        (value - cell_means[p][o]) ** 2
        for p in range(part_count)
        for o in range(operator_count)
        for value in data[p][o]
    )
    mean_squares = (
        ss_part / (part_count - 1),
        ss_operator / (operator_count - 1),
        ss_interaction / ((part_count - 1) * (operator_count - 1)),
        ss_repeat / (part_count * operator_count * (repeat_count - 1)),
    )
    return _gage_components(part_count, operator_count, repeat_count, mean_squares)


def _gage_data(
    measurements: Sequence[Sequence[Sequence[float]]],
) -> tuple[list[list[list[float]]], int, int, int]:
    part_count = len(measurements)
    if part_count < 2:
        raise ValueError("at least two parts are required")
    operator_count = len(measurements[0])
    if operator_count < 2:
        raise ValueError("at least two operators are required")
    repeat_count = len(measurements[0][0]) if measurements[0] else 0
    if repeat_count < 2:
        raise ValueError("at least two replicates are required")
    data: list[list[list[float]]] = []
    for part_index, part in enumerate(measurements):
        if len(part) != operator_count:
            raise ValueError("each part must have the same operators")
        cells = []
        for operator_index, cell in enumerate(part):
            if len(cell) != repeat_count:
                raise ValueError("each part/operator cell must have equal replicates")
            cells.append(_series(f"measurements[{part_index}][{operator_index}]", cell, minimum_length=2))
        data.append(cells)
    return data, part_count, operator_count, repeat_count


def _gage_means(
    data: Sequence[Sequence[Sequence[float]]], operator_count: int
) -> tuple[float, list[float], list[float], list[list[float]]]:
    flat = [value for part in data for cell in part for value in cell]
    grand = mean(flat)
    part_means = [mean([value for cell in part for value in cell]) for part in data]
    operator_means = [mean([value for part in data for value in part[index]]) for index in range(operator_count)]
    cell_means = [[mean(cell) for cell in part] for part in data]
    return grand, part_means, operator_means, cell_means


def _gage_components(
    part_count: int,
    operator_count: int,
    repeat_count: int,
    mean_squares: tuple[float, float, float, float],
) -> dict[str, float | int]:
    ms_part, ms_operator, ms_interaction, ms_repeat = mean_squares
    variance_repeatability = ms_repeat
    variance_interaction = max((ms_interaction - ms_repeat) / repeat_count, 0.0)
    variance_operator = max((ms_operator - ms_interaction) / (part_count * repeat_count), 0.0)
    variance_reproducibility = variance_operator + variance_interaction
    variance_gage = variance_repeatability + variance_reproducibility
    variance_part = max((ms_part - ms_interaction) / (operator_count * repeat_count), 0.0)
    variance_total = variance_gage + variance_part
    return {
        "parts": part_count,
        "operators": operator_count,
        "replicates": repeat_count,
        "part_degrees_of_freedom": part_count - 1,
        "operator_degrees_of_freedom": operator_count - 1,
        "interaction_degrees_of_freedom": (part_count - 1) * (operator_count - 1),
        "repeatability_degrees_of_freedom": part_count * operator_count * (repeat_count - 1),
        "part_sum_of_squares": ms_part * (part_count - 1),
        "operator_sum_of_squares": ms_operator * (operator_count - 1),
        "interaction_sum_of_squares": ms_interaction * (part_count - 1) * (operator_count - 1),
        "repeatability_sum_of_squares": ms_repeat * part_count * operator_count * (repeat_count - 1),
        "part_mean_square": ms_part,
        "operator_mean_square": ms_operator,
        "interaction_mean_square": ms_interaction,
        "repeatability_mean_square": ms_repeat,
        "repeatability_variance": variance_repeatability,
        "operator_variance": variance_operator,
        "part_operator_interaction_variance": variance_interaction,
        "reproducibility_variance": variance_reproducibility,
        "gage_rr_variance": variance_gage,
        "part_to_part_variance": variance_part,
        "total_variance": variance_total,
        "gage_rr_standard_deviation": sqrt(variance_gage),
        "study_variation_6_sigma": 6 * sqrt(variance_gage),
        "percent_contribution_gage_rr": 100 * variance_gage / variance_total if variance_total else 0.0,
        "percent_study_variation_gage_rr": (
            100 * sqrt(variance_gage / variance_total) if variance_total else 0.0
        ),
    }


def tolerance_stack(component_tolerances: Sequence[float]) -> dict[str, float]:
    """Calculate symmetric worst-case and RSS assembly tolerances."""
    tolerances = _series("component tolerances", component_tolerances)
    if any(value < 0 for value in tolerances):
        raise ValueError("component tolerances must be nonnegative magnitudes")
    return {
        "worst_case_tolerance": fsum(tolerances),
        "root_sum_square_tolerance": sqrt(fsum(value * value for value in tolerances)),
    }


def single_sampling_oc(sample_size: int, acceptance_number: int, fraction_nonconforming: float) -> dict[str, float | int]:
    """Calculate binomial probability of accepting an (n, c) sampling plan."""
    size = _count("sample size", sample_size, positive=True)
    acceptance = _count("acceptance number", acceptance_number)
    fraction = _number("fraction nonconforming", fraction_nonconforming, minimum=0.0)
    if acceptance > size:
        raise ValueError("acceptance number cannot exceed sample size")
    if fraction > 1:
        raise ValueError("fraction nonconforming cannot exceed one")
    probability = fsum(
        comb(size, defects) * fraction**defects * (1 - fraction) ** (size - defects)
        for defects in range(acceptance + 1)
    )
    return {
        "sample_size": size,
        "acceptance_number": acceptance,
        "fraction_nonconforming": fraction,
        "probability_of_acceptance": probability,
        "probability_of_rejection": 1 - probability,
    }


def two_level_full_factorial_effects(
    design: Sequence[Sequence[int]], responses: Sequence[float], factor_names: Sequence[str]
) -> dict[str, object]:
    """Calculate all effects for an unreplicated complete two-level factorial."""
    factor_count = len(factor_names)
    invalid_names = any(not isinstance(name, str) or not name.strip() for name in factor_names)
    if factor_count < 1 or invalid_names or len(set(factor_names)) != factor_count:
        raise ValueError("factor names must be nonempty and unique")
    expected_runs = 2**factor_count
    if len(design) != expected_runs or len(responses) != expected_runs:
        raise ValueError("a full two-level design requires 2^k rows and matching responses")
    rows: list[tuple[int, ...]] = []
    for index, row in enumerate(design):
        coded = tuple(row)
        invalid_level = any(isinstance(value, bool) or value not in (-1, 1) for value in coded)
        if len(coded) != factor_count or invalid_level:
            raise ValueError(f"design row {index} must contain one -1/+1 value per factor")
        rows.append(coded)
    if len(set(rows)) != expected_runs:
        raise ValueError("design must contain each level combination exactly once")
    observed = _series("responses", responses, minimum_length=expected_runs)
    effects: dict[str, float] = {}
    for order in range(1, factor_count + 1):
        for indices in combinations(range(factor_count), order):
            label = ":".join(factor_names[index] for index in indices)
            contrast = fsum(
                response * _product([row[index] for index in indices])
                for row, response in zip(rows, observed)
            )
            effects[label] = contrast / (expected_runs / 2)
    return {"intercept": mean(observed), "effects": effects, "run_count": expected_runs}
