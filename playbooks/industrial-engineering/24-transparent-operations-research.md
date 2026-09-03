# Transparent operations research

## Question answered

What result follows from a small, fully declared location, scoring, assignment, or sequencing model—and what operational facts remain outside that model?

## Facility center of gravity

For coordinates \((x_i,y_i)\) and nonnegative flow or cost weights (w_i):

\[
x^*=\frac{\sum w_ix_i}{\sum w_i},\qquad
y^*=\frac{\sum w_iy_i}{\sum w_i}
\]

This screens an unconstrained planar location. It does not account for aisle topology, walls, utilities, hazardous separation, crane coverage, congestion, travel routing, expansion, or regulatory constraints.

## Weighted decision scoring

For criteria already transformed to a common direction and declared scale:

\[
\hat w_j=\frac{w_j}{\sum w_j},\qquad Score_i=\sum_j\hat w_js_{ij}
\]

The function ranks by score and uses the alternative name only as a deterministic tie break. It does not create criteria, normalize unlike raw measurements, set weights, or prove that criteria are independent. Preserve the raw evidence behind each score and run sensitivity cases.

## Bounded assignment

For cost (c_{ij}), assign each row exactly once to a unique column and minimize:

\[
TotalCost=\sum_i c_{i,a(i)}
\]

The dependency-free implementation enumerates every feasible assignment and therefore proves the optimum for the supplied matrix. It is deliberately capped at eight rows. It does not accept arbitrary expressions, soft constraints, forbidden pairs, capacities greater than one, or multi-objective tradeoffs. Larger or richer models belong in a governed solver service.

## Single-machine sequencing

The function compares three declared dispatching rules for jobs available at time zero with no setup time, preemption, machine downtime, or precedence constraints:

- `fcfs`: supplied order;
- `spt`: shortest processing time first;
- `edd`: earliest due date first.

For completion time (C_i) and due date (d_i):

\[
L_i=C_i-d_i,\qquad T_i=\max(0,L_i)
\]

It reports order, completion times, lateness, tardiness, makespan, average completion time, average and maximum tardiness, and late-job count. SPT tends to reduce mean completion time under this narrow model; EDD minimizes maximum lateness under the same assumptions. Neither claim transfers automatically to sequence-dependent setups, shared tooling, skills, material availability, priority classes, or multi-machine routing.

## Worked assignment

For the fictional cost matrix:

```text
      Resource 0  Resource 1  Resource 2
Job 0      9           2           7
Job 1      6           4           3
Job 2      5           8           1
```

Complete enumeration evaluates six assignments. The minimum is Job 0→Resource 1, Job 1→Resource 0, Job 2→Resource 2, with total cost 9.

## Output

Record objective, scope, units, decision variables, constraints represented, constraints omitted, source evidence, formula/method version, alternatives evaluated, result, sensitivity, feasibility review, and human decision. A mathematically optimal answer to the wrong model is still wrong.

Public coverage orientation: the [NCEES Industrial and Systems exam program](https://ncees.org/exams/pe-exam/industrial-and-systems/) identifies operations research, facilities, production systems, and engineering economics as professional competency areas. Facility, safety, program, and configuration authorities govern actual decisions.
