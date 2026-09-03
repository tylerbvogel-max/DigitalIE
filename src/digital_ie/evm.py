"""Readable earned value management calculations.

These functions implement arithmetic from public NASA, DOE, and DoD guidance.
They do not validate an EVMS, approve a baseline, or establish progress.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import fsum, isfinite
from typing import Sequence


@dataclass(frozen=True)
class EvmPerformanceResult:
    cost_variance: float
    schedule_variance: float
    cost_variance_percent: float | None
    schedule_variance_percent: float | None
    cost_performance_index: float | None
    schedule_performance_index: float | None
    percent_scheduled: float
    percent_complete: float
    percent_spent: float
    work_remaining: float
    management_eac: float | None
    variance_at_completion: float | None


@dataclass(frozen=True)
class EvmForecastResult:
    cumulative_cpi: float | None
    cumulative_spi: float | None
    recent_cpi: float | None
    work_remaining: float
    eac_cpi: float | None
    eac_composite: float | None
    eac_recent_cpi: float | None
    eac_management: float | None
    vac_cpi: float | None
    vac_composite: float | None
    vac_recent_cpi: float | None
    vac_management: float | None
    tcpi_bac: float | None
    tcpi_management_eac: float | None


@dataclass(frozen=True)
class CostVarianceResult:
    rate_or_price_variance: float
    volume_or_usage_variance: float
    total_cost_variance: float


def _require_finite_nonnegative(name: str, value: float) -> None:
    if not isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")


def _safe_ratio(numerator: float, denominator: float) -> float | None:
    return numerator / denominator if denominator > 0 else None


def _validate_evm_base(pv: float, ev: float, ac: float, bac: float) -> None:
    for name, value in (("PV", pv), ("EV", ev), ("AC", ac), ("BAC", bac)):
        _require_finite_nonnegative(name, value)
    if bac <= 0:
        raise ValueError("BAC must be positive")
    if pv > bac:
        raise ValueError("cumulative PV cannot exceed BAC for the declared baseline")
    if ev > bac:
        raise ValueError("cumulative EV cannot exceed BAC for the declared baseline")


def performance_snapshot(
    pv: float,
    ev: float,
    ac: float,
    bac: float,
    management_etc: float | None = None,
) -> EvmPerformanceResult:
    """Calculate cumulative EVM variances, indices, and overall status."""
    _validate_evm_base(pv, ev, ac, bac)
    if management_etc is not None:
        _require_finite_nonnegative("management ETC", management_etc)
    cost_variance = ev - ac
    schedule_variance = ev - pv
    management_eac = ac + management_etc if management_etc is not None else None
    variance_at_completion = bac - management_eac if management_eac is not None else None
    return EvmPerformanceResult(
        cost_variance=cost_variance,
        schedule_variance=schedule_variance,
        cost_variance_percent=_safe_ratio(100 * cost_variance, ev),
        schedule_variance_percent=_safe_ratio(100 * schedule_variance, pv),
        cost_performance_index=_safe_ratio(ev, ac),
        schedule_performance_index=_safe_ratio(ev, pv),
        percent_scheduled=100 * pv / bac,
        percent_complete=100 * ev / bac,
        percent_spent=100 * ac / bac,
        work_remaining=bac - ev,
        management_eac=management_eac,
        variance_at_completion=variance_at_completion,
    )


def forecast_at_completion(
    pv: float,
    ev: float,
    ac: float,
    bac: float,
    management_etc: float | None = None,
    recent_period_ev: Sequence[float] | None = None,
    recent_period_ac: Sequence[float] | None = None,
) -> EvmForecastResult:
    """Calculate assumption-based EAC, VAC, and TCPI alternatives."""
    _validate_evm_base(pv, ev, ac, bac)
    if management_etc is not None:
        _require_finite_nonnegative("management ETC", management_etc)
    cpi = _safe_ratio(ev, ac)
    spi = _safe_ratio(ev, pv)
    work_remaining = bac - ev
    eac_cpi = ac + work_remaining / cpi if cpi else None
    composite_factor = cpi * spi if cpi is not None and spi is not None else None
    eac_composite = ac + work_remaining / composite_factor if composite_factor else None
    recent_cpi = _recent_cpi(recent_period_ev, recent_period_ac)
    eac_recent = ac + work_remaining / recent_cpi if recent_cpi else None
    eac_management = ac + management_etc if management_etc is not None else None
    return EvmForecastResult(
        cumulative_cpi=cpi,
        cumulative_spi=spi,
        recent_cpi=recent_cpi,
        work_remaining=work_remaining,
        eac_cpi=eac_cpi,
        eac_composite=eac_composite,
        eac_recent_cpi=eac_recent,
        eac_management=eac_management,
        vac_cpi=bac - eac_cpi if eac_cpi is not None else None,
        vac_composite=bac - eac_composite if eac_composite is not None else None,
        vac_recent_cpi=bac - eac_recent if eac_recent is not None else None,
        vac_management=bac - eac_management if eac_management is not None else None,
        tcpi_bac=_safe_ratio(work_remaining, bac - ac),
        tcpi_management_eac=(
            _safe_ratio(work_remaining, eac_management - ac)
            if eac_management is not None else None
        ),
    )


def _recent_cpi(
    period_ev: Sequence[float] | None, period_ac: Sequence[float] | None
) -> float | None:
    if period_ev is None and period_ac is None:
        return None
    if period_ev is None or period_ac is None or len(period_ev) != len(period_ac):
        raise ValueError("recent-period EV and AC must both be supplied with equal length")
    if not period_ev:
        raise ValueError("recent-period EV and AC cannot be empty")
    for value in (*period_ev, *period_ac):
        _require_finite_nonnegative("recent-period value", value)
    return _safe_ratio(fsum(period_ev), fsum(period_ac))


def reconcile_periods(
    period_pv: Sequence[float],
    period_ev: Sequence[float],
    period_ac: Sequence[float],
    reported_cumulative_pv: float,
    reported_cumulative_ev: float,
    reported_cumulative_ac: float,
    tolerance: float = 0.01,
) -> dict[str, float | bool]:
    """Reconcile period sums to reported cumulative EVM values."""
    if not period_pv or len(period_pv) != len(period_ev) or len(period_ev) != len(period_ac):
        raise ValueError("PV, EV, and AC period series must have equal positive length")
    for value in (*period_pv, *period_ev, *period_ac):
        _require_finite_nonnegative("period value", value)
    for name, value in (
        ("reported cumulative PV", reported_cumulative_pv),
        ("reported cumulative EV", reported_cumulative_ev),
        ("reported cumulative AC", reported_cumulative_ac),
        ("tolerance", tolerance),
    ):
        _require_finite_nonnegative(name, value)
    calculated_pv, calculated_ev, calculated_ac = map(fsum, (period_pv, period_ev, period_ac))
    delta_pv = reported_cumulative_pv - calculated_pv
    delta_ev = reported_cumulative_ev - calculated_ev
    delta_ac = reported_cumulative_ac - calculated_ac
    return {
        "calculated_cumulative_pv": calculated_pv,
        "calculated_cumulative_ev": calculated_ev,
        "calculated_cumulative_ac": calculated_ac,
        "pv_reconciliation_delta": delta_pv,
        "ev_reconciliation_delta": delta_ev,
        "ac_reconciliation_delta": delta_ac,
        "within_tolerance": all(abs(delta) <= tolerance for delta in (delta_pv, delta_ev, delta_ac)),
    }


def schedule_execution(
    baseline_tasks_completed: int,
    baseline_tasks_due: int,
    period_tasks_completed_on_time: int,
    period_tasks_due: int,
) -> dict[str, float]:
    """Calculate baseline execution index and current-period hit rate."""
    values = (
        baseline_tasks_completed,
        baseline_tasks_due,
        period_tasks_completed_on_time,
        period_tasks_due,
    )
    if any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in values):
        raise ValueError("schedule execution inputs must be nonnegative integers")
    if baseline_tasks_due <= 0 or period_tasks_due <= 0:
        raise ValueError("schedule execution denominators must be positive")
    if baseline_tasks_completed > baseline_tasks_due:
        raise ValueError("completed baseline tasks cannot exceed baseline tasks due")
    if period_tasks_completed_on_time > period_tasks_due:
        raise ValueError("on-time period tasks cannot exceed period tasks due")
    return {
        "baseline_execution_index": baseline_tasks_completed / baseline_tasks_due,
        "hit_miss_task_percent": 100 * period_tasks_completed_on_time / period_tasks_due,
    }


def labor_cost_variance(
    budget_rate: float, actual_rate: float, earned_hours: float, actual_hours: float
) -> CostVarianceResult:
    """Decompose labor cost variance into rate and volume components."""
    for name, value in (
        ("budget rate", budget_rate),
        ("actual rate", actual_rate),
        ("earned hours", earned_hours),
        ("actual hours", actual_hours),
    ):
        _require_finite_nonnegative(name, value)
    rate_variance = (budget_rate - actual_rate) * actual_hours
    volume_variance = (earned_hours - actual_hours) * budget_rate
    return CostVarianceResult(
        rate_variance,
        volume_variance,
        rate_variance + volume_variance,
    )


def material_cost_variance(
    budget_unit_price: float,
    actual_unit_price: float,
    earned_quantity: float,
    actual_quantity: float,
) -> CostVarianceResult:
    """Decompose material cost variance into price and usage components."""
    for name, value in (
        ("budget unit price", budget_unit_price),
        ("actual unit price", actual_unit_price),
        ("earned quantity", earned_quantity),
        ("actual quantity", actual_quantity),
    ):
        _require_finite_nonnegative(name, value)
    price_variance = (budget_unit_price - actual_unit_price) * actual_quantity
    usage_variance = (earned_quantity - actual_quantity) * budget_unit_price
    return CostVarianceResult(
        price_variance,
        usage_variance,
        price_variance + usage_variance,
    )
