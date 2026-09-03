"""Transparent periodic-cash-flow and manufacturing decision economics."""

from __future__ import annotations

from math import fsum, isfinite
from typing import Sequence


def _finite(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _rate(rate: float) -> float:
    result = _finite("rate", rate)
    if result <= -1:
        raise ValueError("rate must be greater than -1")
    return result


def _computed(name: str, operation) -> float:
    """Convert arithmetic overflow or a nonfinite result to a domain error."""
    try:
        result = float(operation())
    except (OverflowError, ZeroDivisionError) as error:
        raise ValueError(f"{name} is not finite for the supplied inputs") from error
    if not isfinite(result):
        raise ValueError(f"{name} is not finite for the supplied inputs")
    return result


def future_value(present_value: float, rate: float, periods: int) -> float:
    """Compound one present amount through a whole number of periods."""
    if isinstance(periods, bool) or not isinstance(periods, int) or periods < 0:
        raise ValueError("periods must be a nonnegative integer")
    amount = _finite("present value", present_value)
    discount_rate = _rate(rate)
    return _computed(
        "future value", lambda: amount * (1 + discount_rate) ** periods
    )


def present_value(future_value_amount: float, rate: float, periods: int) -> float:
    """Discount one future amount to period zero."""
    if isinstance(periods, bool) or not isinstance(periods, int) or periods < 0:
        raise ValueError("periods must be a nonnegative integer")
    amount = _finite("future value", future_value_amount)
    discount_rate = _rate(rate)
    return _computed(
        "present value", lambda: amount / (1 + discount_rate) ** periods
    )


def net_present_value(cash_flows: Sequence[float], rate: float) -> float:
    """Discount equally spaced cash flows, with the first at period zero."""
    if not cash_flows:
        raise ValueError("cash flows cannot be empty")
    discount_rate = _rate(rate)
    terms = [
        _computed(
            "discounted cash flow",
            lambda amount=amount, period=period: _finite("cash flow", amount)
            / (1 + discount_rate) ** period,
        )
        for period, amount in enumerate(cash_flows)
    ]
    return _computed(
        "net present value", lambda: fsum(terms)
    )


def equivalent_annual_value(net_present_amount: float, rate: float, periods: int) -> float:
    """Convert a present amount to an equivalent uniform end-period series."""
    amount = _finite("net present amount", net_present_amount)
    discount_rate = _rate(rate)
    if isinstance(periods, bool) or not isinstance(periods, int) or periods <= 0:
        raise ValueError("periods must be a positive integer")
    if discount_rate == 0:
        return amount / periods
    factor = _computed(
        "capital recovery factor",
        lambda: discount_rate
        * (1 + discount_rate) ** periods
        / ((1 + discount_rate) ** periods - 1),
    )
    return _computed("equivalent annual value", lambda: amount * factor)


def payback_period(cash_flows: Sequence[float], rate: float | None = None) -> float | None:
    """Return simple or discounted payback with uniform-within-period interpolation."""
    if len(cash_flows) < 2:
        raise ValueError("payback requires an initial flow and at least one later flow")
    discount_rate = _rate(rate) if rate is not None else None
    cumulative = _finite("cash flow", cash_flows[0])
    if cumulative >= 0:
        return 0.0
    for period, raw_amount in enumerate(cash_flows[1:], start=1):
        amount = _finite("cash flow", raw_amount)
        if discount_rate is not None:
            amount /= (1 + discount_rate) ** period
        prior = cumulative
        cumulative = _computed("cumulative cash flow", lambda: cumulative + amount)
        if cumulative >= 0 and amount > 0:
            return (period - 1) + (-prior / amount)
    return None


def internal_rate_of_return(
    cash_flows: Sequence[float],
    lower_rate: float = -0.9999,
    upper_rate: float = 10.0,
    tolerance: float = 1e-10,
    max_iterations: int = 200,
) -> float:
    """Find one bracketed periodic IRR using bounded bisection."""
    parsed_flows = [_finite("cash flow", item) for item in cash_flows]
    if (
        len(parsed_flows) < 2
        or not any(item < 0 for item in parsed_flows)
        or not any(item > 0 for item in parsed_flows)
    ):
        raise ValueError("IRR requires at least one negative and one positive cash flow")
    lower = _rate(lower_rate)
    upper = _rate(upper_rate)
    if lower >= upper:
        raise ValueError("lower rate must be less than upper rate")
    tolerance = _finite("tolerance", tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or not 1 <= max_iterations <= 10_000:
        raise ValueError("max iterations must be an integer from 1 through 10000")
    lower_value = net_present_value(parsed_flows, lower)
    upper_value = net_present_value(parsed_flows, upper)
    if lower_value == 0:
        return lower
    if upper_value == 0:
        return upper
    if lower_value * upper_value > 0:
        raise ValueError("IRR is not bracketed by the supplied rate bounds")
    for _ in range(max_iterations):
        midpoint = (lower + upper) / 2
        midpoint_value = net_present_value(parsed_flows, midpoint)
        if abs(midpoint_value) <= tolerance or upper - lower <= tolerance:
            return midpoint
        if lower_value * midpoint_value <= 0:
            upper = midpoint
        else:
            lower = midpoint
            lower_value = midpoint_value
    raise ValueError("IRR solver did not converge within max iterations")


def break_even_units(fixed_cost: float, unit_price: float, unit_variable_cost: float) -> float | None:
    """Return volume where revenue equals fixed plus variable cost."""
    fixed = _finite("fixed cost", fixed_cost)
    price = _finite("unit price", unit_price)
    variable = _finite("unit variable cost", unit_variable_cost)
    if fixed < 0 or price < 0 or variable < 0:
        raise ValueError("break-even inputs must be nonnegative")
    contribution = price - variable
    return fixed / contribution if contribution > 0 else None


def make_buy_analysis(
    quantity: float,
    make_fixed_cost: float,
    make_unit_cost: float,
    buy_unit_cost: float,
) -> dict[str, float | str | None]:
    """Compare relevant make and buy costs at one declared volume."""
    values = {
        "quantity": quantity,
        "make fixed cost": make_fixed_cost,
        "make unit cost": make_unit_cost,
        "buy unit cost": buy_unit_cost,
    }
    parsed = {name: _finite(name, value) for name, value in values.items()}
    if any(value < 0 for value in parsed.values()):
        raise ValueError("make-buy inputs must be nonnegative")
    make_total = _computed(
        "make total cost",
        lambda: parsed["make fixed cost"]
        + parsed["quantity"] * parsed["make unit cost"],
    )
    buy_total = _computed(
        "buy total cost",
        lambda: parsed["quantity"] * parsed["buy unit cost"],
    )
    denominator = parsed["buy unit cost"] - parsed["make unit cost"]
    crossover = (
        _computed(
            "crossover quantity", lambda: parsed["make fixed cost"] / denominator
        )
        if denominator > 0
        else None
    )
    preferred = "make" if make_total < buy_total else "buy" if buy_total < make_total else "equal"
    return {
        "make_total_cost": make_total,
        "buy_total_cost": buy_total,
        "cost_difference_make_minus_buy": make_total - buy_total,
        "crossover_quantity": crossover,
        "lower_relevant_cost": preferred,
    }


def life_cycle_cost(costs_by_period: Sequence[float], rate: float) -> float:
    """Present-value a cost-only lifecycle stream; costs are positive outlays."""
    if not costs_by_period:
        raise ValueError("lifecycle costs cannot be empty")
    if any(_finite("lifecycle cost", item) < 0 for item in costs_by_period):
        raise ValueError("lifecycle costs must be nonnegative")
    return -net_present_value([-item for item in costs_by_period], rate)


def npv_rate_sensitivity(cash_flows: Sequence[float], rates: Sequence[float]) -> dict[str, float]:
    """Return one-way NPV sensitivity across explicitly supplied rates."""
    if not rates:
        raise ValueError("rates cannot be empty")
    result: dict[str, float] = {}
    for rate in rates:
        parsed_rate = _rate(rate)
        key = format(parsed_rate, ".17g")
        if key in result:
            raise ValueError("rates must be unique")
        result[key] = net_present_value(cash_flows, parsed_rate)
    return result
