# Engineering economics and lifecycle decisions

## Purpose

Put alternatives that occur at different times onto a consistent economic
basis. Use the results to expose assumptions and tradeoffs, not to substitute
for approved accounting policy, estimating practice, or source-selection
authority.

## Minimum evidence contract

Record the analysis base date, service date, study period, cash-flow timing,
currency and price-year basis, nominal or real treatment, approved discount
rate, escalation assumptions, tax treatment, residual value, relevant-cost
boundary, quantities, and uncertainty ranges. Alternatives require the same
study period and consistent inflation treatment.

## Time value of money

For present amount `PV`, future amount `FV`, periodic rate `r`, and `n` periods:

```text
FV = PV(1 + r)^n
PV = FV / (1 + r)^n
NPV = sum(CF_t / (1 + r)^t) for t = 0 through n
```

Cash flow zero occurs at the base date. Later flows occur at period end. Use
positive amounts for receipts or savings and negative amounts for expenditures
when calculating NPV.

Equivalent annual value converts a present amount `P` into a uniform end-period
series:

```text
EAV = P * [r(1+r)^n / ((1+r)^n - 1)]
```

At `r=0`, `EAV=P/n`.

## Payback and discounted payback

Accumulate cash flows until the cumulative amount changes from negative to
nonnegative. DigitalIE interpolates within the recovery period by assuming the
recovering cash flow accrues uniformly:

```text
Payback = prior completed periods + unrecovered amount / recovery-period flow
```

Discounted payback first discounts each later flow. Payback ignores value after
recovery and is therefore a screening measure, not a complete economic merit
measure.

## Internal rate of return

IRR is a periodic rate where NPV is zero. DigitalIE uses bounded bisection and
returns a root only when the user-supplied bounds bracket a sign change. It does
not search unbounded space or hide nonconvergence.

Nonconventional cash flows may have multiple IRRs or none. Always examine the
cash-flow signs and compare NPV at the approved discount rate. The returned IRR
is one bracketed mathematical root, not an approval threshold.

## Break-even and make-or-buy arithmetic

For fixed cost `F`, selling price `P`, and variable unit cost `V`:

```text
Contribution margin = P - V
Break-even units = F / (P - V), only when P > V
```

For quantity `Q`:

```text
Make cost = make fixed cost + Q * make unit cost
Buy cost = Q * buy unit cost
Crossover quantity = make fixed cost / (buy unit cost - make unit cost)
```

The crossover exists in the usual positive-volume case only when buy unit cost
exceeds make unit cost. Relevant costs must exclude unavoidable allocations and
include opportunity, capacity, tooling, quality, logistics, obsolescence,
transition, and supply-risk consequences when they differ between alternatives.

## Lifecycle cost and sensitivity

Life-cycle cost is the present value of acquisition, installation, operation,
maintenance, downtime, replacement, disposal, and other included outlays:

```text
LCC = sum(Cost_t / (1 + r)^t)
```

One-way rate sensitivity reruns the same cash flows at each declared discount
rate. A decision should also test the assumptions most capable of reversing the
ranking: volume, yield, learning, utilization, labor, material, schedule,
residual value, and useful life.

## Worked example

For cash flows `[-1000, 600, 600]` and `r=10%`, NPV is approximately `41.3223`.
For make fixed cost 20,000, make unit cost 30, and buy unit cost 60, crossover
volume is approximately 666.67 units. At 1,000 units, make cost is 50,000 and
buy cost is 60,000 before nondifferential or omitted consequences.

## Authority boundary

The kernel does not select an approved discount rate, determine which costs are
relevant, validate an estimate basis, authorize capital, make a source-selection
decision, or establish accounting treatment. Finance, contracts, supply-chain,
engineering, quality, security, and accountable management review remain
necessary for the decision in scope.

## Primary references

- [NIST Handbook 135, Life Cycle Costing Manual](https://doi.org/10.6028/NIST.HB.135e2025)
- [DOE Cost Estimating Guide](https://www.energy.gov/documents/cost-estimating-guide)
- [GAO Cost Estimating and Assessment Guide](https://www.gao.gov/products/gao-20-195g)
