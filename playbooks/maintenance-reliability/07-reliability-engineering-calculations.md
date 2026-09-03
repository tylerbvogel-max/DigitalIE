# Reliability engineering calculations

## Purpose

Calculate transparent reliability and maintainability measures, life-model
values, simple system reliability, and zero-failure demonstration quantities.
Keep observed metrics, probabilistic models, and requirements distinct.

## Minimum evidence contract

Record the item and configuration, repairable/nonrepairable classification,
mission definition, operating and downtime boundaries, failure definition,
censoring, test environment, population, units, data provenance, model and
parameter source, independence assumptions, and confidence requirement.

## Observed repairable-item metrics

For accumulated operating time `T`, observed failures `r`, and accumulated
repair time `D`:

```text
Observed failure rate = r / T
Observed MTBF = T / r
Observed MTTR = D / r
Observed inherent availability = T / (T + D)
```

For nonrepairable items, observed `MTTF = total time on test / failures` under
the declared censoring and pooling basis. When `r=0`, the observed failure rate
is zero but MTBF, MTTF, and MTTR are undefined;
zero failures do not prove infinite life. If administrative and logistics delay
are excluded, do not label the resulting ratio operational availability. When
all included downtime is known:

```text
Operational availability = uptime / (uptime + total downtime)
```

For declared MTBF and MTTR:

```text
Inherent availability = MTBF / (MTBF + MTTR)
```

## Exponential life model

For constant failure rate `lambda`, time `t`, and `MTTF=1/lambda`:

```text
Reliability R(t) = exp(-lambda*t)
CDF F(t) = 1 - R(t)
Hazard h(t) = lambda
Cumulative hazard H(t) = lambda*t
```

Use only when a constant-hazard model is defensible. It generally does not
represent infant mortality or wear-out.

## Two-parameter Weibull model

For scale `eta`, shape `beta`, time `t`, and zero location:

```text
R(t) = exp(-(t/eta)^beta)
F(t) = 1 - R(t)
h(t) = (beta/eta)(t/eta)^(beta-1)
H(t) = (t/eta)^beta
Mean life = eta * Gamma(1 + 1/beta)
```

Shape below one indicates decreasing hazard, shape one reduces to exponential,
and shape above one indicates increasing hazard within the model. At time zero
with shape below one, hazard and density are singular; DigitalIE returns them as
undefined rather than emitting infinity into a calculation receipt.

Parameter values must come from a documented fit or approved engineering basis.
The calculator does not fit censored life data or validate a distribution.

## Independent system models

For component reliabilities `R_i`:

```text
Series: R_system = product(R_i)
Active parallel: R_system = 1 - product(1 - R_i)
```

DigitalIE calculates heterogeneous `k-out-of-n` reliability by convolving the
success/failure probability of each component and summing the probabilities of
at least `k` successes. This includes active parallel at `k=1` and series at
`k=n`.

These formulas require statistically independent component outcomes and a
correct success logic model. They do not represent common-cause failures,
dormant failures, imperfect switching, repair, dependency, or load sharing.

## Zero-failure demonstrations

For independent identical units, a fixed mission, reliability requirement `R`,
confidence `C`, and acceptance only with zero failures:

```text
Binomial sample size n = ceil(ln(1-C) / ln(R))
```

For accumulated test time under an exponential constant-hazard model, MTBF
requirement `theta`, confidence `C`, and zero failures:

```text
Required accumulated test time T = -theta * ln(1-C)
```

At `R=0.90` and `C=0.90`, the zero-failure binomial plan requires 22 units.
At an MTBF requirement of 1,000 hours and 90% confidence, the exponential plan
requires approximately 2,302.585 accumulated test hours.

These are narrow zero-failure plans. They do not design a general acceptance
test, account for Weibull uncertainty, permit failures, set producer/consumer
risk pairs, establish acceleration factors, or replace an approved test plan.

## Authority boundary

The calculator does not decide what constitutes a failure, select a life model,
declare independence, approve a qualification plan, accept hardware, defer
maintenance, or certify reliability compliance. Reliability engineering,
quality, safety, test, design authority, and program approval remain external.

## Primary references

- [NIST Engineering Statistics Handbook: exponential model](https://www.itl.nist.gov/div898/handbook/apr/section1/apr161.htm)
- [NIST Engineering Statistics Handbook: series model](https://www.itl.nist.gov/div898/handbook/apr/section1/apr182.htm)
- [NIST Engineering Statistics Handbook: parallel model](https://www.itl.nist.gov/div898/handbook/apr/section1/apr183.htm)
- [NIST Engineering Statistics Handbook: reliability test planning](https://www.itl.nist.gov/div898/handbook/apr/section3/apr3.htm)
