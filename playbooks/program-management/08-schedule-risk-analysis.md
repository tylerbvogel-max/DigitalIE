# Schedule network and risk analysis

## Purpose

Use a logic-linked schedule to calculate the earliest feasible completion,
identify activities controlling that date, expose available flexibility, and
quantify duration uncertainty. The arithmetic supports a scheduling decision;
it does not establish that the underlying integrated master schedule is valid.

## Minimum evidence contract

Record the schedule identifier and revision, status date, calendar and duration
units, scope boundary, activity identifiers, remaining durations, predecessor
logic, constraints, and source for each uncertainty range. Confirm that the
activity network is complete and current before interpreting its output.

The deterministic CPM kernel deliberately accepts only finish-to-start,
zero-lag relationships. Convert neither leads, lags, constraints, resources,
nor alternate calendars silently. Use an approved scheduling system when those
features affect the result.

## Critical path method

For activity `i` with duration `d_i` and finish-to-start predecessors `P_i`:

```text
ES_i = max(EF_j for j in P_i), or 0 when P_i is empty
EF_i = ES_i + d_i
Project duration = max(EF_i)
LF_i = min(LS_k for successor k), or project duration at a terminal activity
LS_i = LF_i - d_i
Total float_i = LS_i - ES_i = LF_i - EF_i
Free float_i = min(ES_k for successor k) - EF_i
```

The forward pass follows topological order. The backward pass reverses it. An
activity with zero total float is critical in this unconstrained model. Float
belongs to a path and is not automatically owned by an individual activity or
organization.

### Worked example

```text
A: duration 3, no predecessor
B: duration 4, predecessor A
C: duration 2, predecessor A
D: duration 5, predecessors B and C
```

The forward pass gives `EF_A=3`, `EF_B=7`, `EF_C=5`, and `EF_D=12`.
The project duration is 12. The backward pass gives activity C two units of
total and free float. Activities A, B, and D have zero total float and form the
controlling path in this model.

## Three-point PERT estimate

For optimistic `o`, most-likely `m`, and pessimistic `p` estimates:

```text
Expected duration = (o + 4m + p) / 6
Standard deviation = (p - o) / 6
Variance = ((p - o) / 6)^2
```

The order must satisfy `o <= m <= p`. For `o=2`, `m=5`, and `p=14`, the
expected duration is 6, the standard deviation is 2, and the variance is 4.
These expressions are a conventional approximation, not evidence that the
three inputs follow a beta distribution or are calibrated.

## Reproducible schedule simulation

For each iteration, sample every activity duration from the explicitly supplied
triangular distribution, rerun CPM, and retain project duration and the set of
critical activities. Report the sample mean, population standard deviation,
P50/P80/P90/P95, range, seed, iteration count, and criticality index:

```text
Criticality index_i = iterations where activity i has zero float / iterations
```

DigitalIE caps a run at 100,000 iterations and uses a local pseudorandom stream
with a required integer seed. The same inputs, code version, iteration count,
and seed reproduce the same result. A seed does not make the sampled
distributions correct.

## Reproducible cost simulation

Each base cost is sampled from an explicitly supplied triangular distribution.
An optional discrete risk adds its declared impact when a Bernoulli draw is
below its occurrence probability. The output reports mean, standard deviation,
range, and P50/P80/P90/P95 cost.

Do not add multiple impacts independently when they share a cause or are
correlated. The present kernel does not model correlation, escalation,
time-phased cost, or schedule-cost coupling.

## Interpretation and challenge questions

- Does the network capture all necessary work and valid logic?
- Are open ends, excessive lags, hard constraints, and unrealistic float known?
- Do uncertainty ranges reflect evidence and current remaining work?
- Are schedule and cost risks correlated or mutually exclusive?
- Which near-critical paths become controlling across simulations?
- Does the selected confidence date match the organization's risk appetite?

## Authority boundary

The calculations do not approve an integrated master schedule, establish a
contract date, assign contingency, authorize recovery action, or certify GAO
schedule-guide conformance. A scheduler and accountable program authority must
review the logic, calendars, constraints, assumptions, and selected confidence
level.

## Primary references

- [GAO Schedule Assessment Guide](https://www.gao.gov/products/gao-16-89g)
- [GAO Cost Estimating and Assessment Guide](https://www.gao.gov/products/gao-20-195g)
- [NASA Scheduling Guide for Program Managers](https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/Scheduling%20Guide%20for%20Program%20Managers%20Oct%202001.pdf)
