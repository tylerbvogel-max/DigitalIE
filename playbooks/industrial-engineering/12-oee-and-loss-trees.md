# OEE and loss trees

## Question answered

Where is planned production time being lost, and which loss mechanism is worth attacking first?

## Definitions

For a stable, clearly bounded asset/cell, define planned production time, planned downtime, unplanned downtime, ideal cycle time, total count, and good count. Then:

```text
Availability = run time / planned production time
Performance  = ideal cycle time × total count / run time
Quality      = good count / total count
OEE          = Availability × Performance × Quality
```

The arithmetic is easy; the operational definitions decide whether it is useful. Do not compare OEE across cells until calendars, ideal rates, microstop rules, and quality disposition are comparable.

## Worked example

For a fictional shift with 450 planned production minutes, 405 run minutes, 1.0 minute ideal cycle, 360 total units, and 342 good units:

```text
Availability = 405 / 450 = 0.900
Performance  = 1.0 × 360 / 405 = 0.8889
Quality      = 342 / 360 = 0.950
OEE          = 0.900 × 0.8889 × 0.950 = 0.760 = 76.0%
```

The multiplicative result is equivalent to \(IdealCycleTime\times GoodCount/PlannedProductionTime\) only when the definitions and boundary are consistent. Preserve component losses; the composite alone does not show the mechanism.

## Build a loss tree

Classify losses into planned versus unplanned, then use local mechanisms: breakdown, setup/changeover, waiting/starvation/blockage, minor stops, reduced speed, startup loss, scrap, rework, and schedule/engineering holds. Preserve both minutes and lost good units/dollars where possible.

## Questions

- Is the constraint asset actually the system constraint, or is it being starved/blocked?
- Is “planned” downtime a chosen policy hiding a capacity loss?
- Does ideal cycle time reflect a demonstrated sustainable condition?
- Are rework and quality losses counted once and consistently?

## Exit

Choose one loss branch with its mechanism unknown or poorly understood; use Gemba, Pareto, SPC, or a capacity analysis rather than optimizing the metric itself.
