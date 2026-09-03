"""Deterministic demand-planning and inventory calculations."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, fsum, isfinite, sqrt
from typing import Sequence


def _finite(name: str, value: float) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _nonnegative(name: str, value: float) -> None:
    _finite(name, value)
    if value < 0:
        raise ValueError(f"{name} must be nonnegative")


def moving_average(values: Sequence[float], window: int) -> dict[str, tuple[float | None, ...] | float]:
    """Return trailing fitted forecasts and the next-period moving average."""
    if not values:
        raise ValueError("values cannot be empty")
    if isinstance(window, bool) or not isinstance(window, int) or not 1 <= window <= len(values):
        raise ValueError("window must be an integer from one through the series length")
    for value in values:
        _finite("observation", value)
    fitted: list[float | None] = [None] * window
    for index in range(window, len(values)):
        fitted.append(fsum(values[index - window:index]) / window)
    return {
        "fitted_forecasts": tuple(fitted),
        "next_forecast": fsum(values[-window:]) / window,
    }


def simple_exponential_smoothing(
    values: Sequence[float], alpha: float, initial_forecast: float | None = None
) -> dict[str, tuple[float, ...] | float]:
    """Return one-step-ahead fitted forecasts and the next SES forecast."""
    if not values:
        raise ValueError("values cannot be empty")
    if not isfinite(alpha) or not 0 < alpha <= 1:
        raise ValueError("alpha must be above zero and at most one")
    for value in values:
        _finite("observation", value)
    if initial_forecast is not None:
        _finite("initial forecast", initial_forecast)
    forecast = values[0] if initial_forecast is None else initial_forecast
    fitted = []
    for actual in values:
        fitted.append(forecast)
        forecast = alpha * actual + (1 - alpha) * forecast
    return {"fitted_forecasts": tuple(fitted), "next_forecast": forecast}


@dataclass(frozen=True)
class ForecastAccuracyResult:
    errors: tuple[float, ...]
    mean_error: float
    mad: float
    mse: float
    rmse: float
    mape_percent: float | None
    tracking_signal: float | None
    mape_excluded_zero_actuals: int


def forecast_accuracy(actuals: Sequence[float], forecasts: Sequence[float]) -> ForecastAccuracyResult:
    """Calculate errors as actual minus forecast and common accuracy measures."""
    if not actuals or len(actuals) != len(forecasts):
        raise ValueError("actual and forecast series must have equal positive length")
    for value in (*actuals, *forecasts):
        _finite("forecast-series value", value)
    errors = tuple(actual - forecast for actual, forecast in zip(actuals, forecasts))
    count = len(errors)
    mean_error = fsum(errors) / count
    mad = fsum(abs(error) for error in errors) / count
    mse = fsum(error**2 for error in errors) / count
    percentage_errors = [abs(error / actual) for error, actual in zip(errors, actuals) if actual]
    mape = 100 * fsum(percentage_errors) / len(percentage_errors) if percentage_errors else None
    return ForecastAccuracyResult(
        errors=errors,
        mean_error=mean_error,
        mad=mad,
        mse=mse,
        rmse=sqrt(mse),
        mape_percent=mape,
        tracking_signal=fsum(errors) / mad if mad else None,
        mape_excluded_zero_actuals=count - len(percentage_errors),
    )


@dataclass(frozen=True)
class InventoryPolicyResult:
    economic_order_quantity: float
    orders_per_year: float
    cycle_stock: float
    annual_ordering_cost: float
    annual_cycle_stock_holding_cost: float


def economic_order_quantity(
    annual_demand: float, order_cost: float, annual_holding_cost_per_unit: float
) -> InventoryPolicyResult:
    """Calculate the classical EOQ policy without quantity discounts or shortages."""
    for name, value in (
        ("annual demand", annual_demand),
        ("order cost", order_cost),
        ("annual holding cost per unit", annual_holding_cost_per_unit),
    ):
        _nonnegative(name, value)
        if value == 0:
            raise ValueError(f"{name} must be positive")
    quantity = sqrt(2 * annual_demand * order_cost / annual_holding_cost_per_unit)
    return InventoryPolicyResult(
        economic_order_quantity=quantity,
        orders_per_year=annual_demand / quantity,
        cycle_stock=quantity / 2,
        annual_ordering_cost=annual_demand / quantity * order_cost,
        annual_cycle_stock_holding_cost=quantity / 2 * annual_holding_cost_per_unit,
    )


def reorder_point(
    mean_demand_per_period: float,
    lead_time_periods: float,
    demand_standard_deviation_per_period: float = 0,
    service_z: float = 0,
) -> dict[str, float]:
    """Calculate ROP assuming constant lead time and independent period demand."""
    _nonnegative("mean demand per period", mean_demand_per_period)
    _nonnegative("lead time periods", lead_time_periods)
    _nonnegative("demand standard deviation per period", demand_standard_deviation_per_period)
    _finite("service z", service_z)
    if service_z < 0:
        raise ValueError("service z must be nonnegative")
    expected = mean_demand_per_period * lead_time_periods
    lead_sigma = demand_standard_deviation_per_period * sqrt(lead_time_periods)
    safety_stock = service_z * lead_sigma
    return {
        "expected_lead_time_demand": expected,
        "lead_time_demand_standard_deviation": lead_sigma,
        "safety_stock": safety_stock,
        "reorder_point": expected + safety_stock,
    }


@dataclass(frozen=True)
class MrpResult:
    gross_requirements: tuple[float, ...]
    scheduled_receipts: tuple[float, ...]
    projected_available: tuple[float, ...]
    net_requirements: tuple[float, ...]
    planned_order_receipts: tuple[float, ...]
    planned_order_releases: tuple[float, ...]
    past_due_releases: tuple[dict[str, float | int], ...]


def mrp_netting(
    gross_requirements: Sequence[float],
    scheduled_receipts: Sequence[float],
    initial_available: float,
    lead_time_periods: int,
    safety_stock: float = 0,
    fixed_order_quantity: float | None = None,
) -> MrpResult:
    """Perform single-item, time-phased MRP netting."""
    if not gross_requirements or len(gross_requirements) != len(scheduled_receipts):
        raise ValueError("gross requirements and scheduled receipts must have equal positive length")
    for value in (*gross_requirements, *scheduled_receipts):
        _nonnegative("MRP period value", value)
    _nonnegative("initial available", initial_available)
    _nonnegative("safety stock", safety_stock)
    if isinstance(lead_time_periods, bool) or not isinstance(lead_time_periods, int) or lead_time_periods < 0:
        raise ValueError("lead time periods must be a nonnegative integer")
    if fixed_order_quantity is not None:
        _nonnegative("fixed order quantity", fixed_order_quantity)
        if fixed_order_quantity == 0:
            raise ValueError("fixed order quantity must be positive")
    periods = len(gross_requirements)
    available = initial_available
    projected = []
    net = [0.0] * periods
    receipts = [0.0] * periods
    releases = [0.0] * periods
    past_due = []
    for period in range(periods):
        before_plan = available + scheduled_receipts[period] - gross_requirements[period]
        if before_plan < safety_stock:
            net[period] = safety_stock - before_plan
            receipts[period] = (
                ceil(net[period] / fixed_order_quantity) * fixed_order_quantity
                if fixed_order_quantity is not None else net[period]
            )
            release_period = period - lead_time_periods
            if release_period >= 0:
                releases[release_period] += receipts[period]
            else:
                past_due.append({"receipt_period": period, "quantity": receipts[period]})
        available = before_plan + receipts[period]
        projected.append(available)
    return MrpResult(
        tuple(gross_requirements),
        tuple(scheduled_receipts),
        tuple(projected),
        tuple(net),
        tuple(receipts),
        tuple(releases),
        tuple(past_due),
    )
