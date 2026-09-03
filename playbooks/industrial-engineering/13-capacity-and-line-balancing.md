# Capacity and line balancing

## Question answered

Can the system meet required demand reliably, where is the governing constraint, and how should work be distributed without creating more WIP and hidden instability?

## Establish the math

Define demand by product mix and time period, available time after planned losses, takt time, actual cycle time by step, yield/rework, changeover, staffing/skill constraints, and equipment availability. Calculate effective capacity with observed—not nameplate—performance. Show assumptions about mix, sequencing, and overtime.

\[
TaktTime=\frac{NetAvailableProductionTime}{CustomerDemand}
\]

\[
TheoreticalMinimumOperators=\frac{TotalManualWorkContent}{TaktTime}
\]

For a bounded resource with net scheduled time \(T\), observed availability \(A\), demonstrated cycle time \(CT\), and first-pass yield \(Y\):

\[
ExpectedGoodCapacity=\frac{T\times A}{CT}\times Y
\]

Example: 420 net minutes, demand 70 units, and 15 minutes manual work content give takt \(6\) min/unit and theoretical minimum \(2.5\), meaning at least 3 operators before balance, walking, interference, relief, mix, and variability allowances. An asset at \(A=0.90\), \(CT=5\) min/unit, and \(Y=0.95\) has expected good capacity \((420\times0.90/5)\times0.95=71.82\) units under those assumptions.

## Find the constraint

The longest cycle-time step is not automatically the constraint. Observe starvation, blockage, queue accumulation, schedule priority, downtime, batch rules, and shared-resource conflicts. The governing constraint is the resource that limits system throughput under current conditions.

## Balance deliberately

Consider work-content redistribution, staffing to takt, parallelization, cross-training, changeover reduction, buffer policy, and release policy. Evaluate each against safety, quality, ergonomic load, qualification, and product-mix variability. Do not “balance” by moving an invisible burden or creating an unmanageable handoff.

## Exit

Produce a demand/capacity view with explicit assumptions, a verified constraint hypothesis, and one controlled change predicted to improve throughput, lead time, or schedule adherence.
