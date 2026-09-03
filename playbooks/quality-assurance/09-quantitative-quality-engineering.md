# Quantitative Quality Engineering

Use this playbook to turn quality evidence into reproducible calculations. The
calculator supplies arithmetic; the improvement case retains the sampling
rationale, process definition, source records, engineering interpretation, and
human disposition.

## Entry conditions

Before calculating, identify the characteristic or defect definition, process
boundary, time order, product/configuration, measurement system, sampling frame,
units, and applicable specification revision. Never substitute control limits
for specifications. Do not calculate capability until process stability and the
distributional model have been assessed.

## Control charts

For observations in time order, the moving range is

`MR[i] = abs(x[i] - x[i-1])`.

For the conventional moving range of two, `sigma_within = MR_bar / 1.128` and
the Individuals limits are `x_bar +/- 3 sigma_within`. The MR limits use
`D3 * MR_bar` and `D4 * MR_bar`; the defaults in the kernel are `D3 = 0` and
`D4 = 3.267` for ranges of two.

For equal rational subgroups:

- X-bar/R: `UCLx = x_double_bar + A2*R_bar`,
  `LCLx = x_double_bar - A2*R_bar`; range limits are `D3*R_bar` and
  `D4*R_bar`.
- X-bar/S: `UCLx = x_double_bar + A3*s_bar`,
  `LCLx = x_double_bar - A3*s_bar`; standard-deviation limits are
  `B3*s_bar` and `B4*s_bar`.

The caller supplies subgroup constants so a controlled source can govern them.
The calculator does not select subgroup size or rational-subgroup strategy.

Attribute charts use three-sigma limits, clipped at the natural lower bound and,
for proportions, the upper bound of one:

- p chart: `p_bar = total nonconforming / total inspected` and limits for each
  sample `p_bar +/- 3*sqrt(p_bar*(1-p_bar)/n[i])`.
- np chart: center `n*p_bar`; limits `n*p_bar +/- 3*sqrt(n*p_bar*(1-p_bar))`.
- c chart: center `c_bar`; limits `c_bar +/- 3*sqrt(c_bar)` for equal inspection
  opportunity.
- u chart: `u_bar = total nonconformities / total inspection units`; limits
  `u_bar +/- 3*sqrt(u_bar/n[i])`.

Signals identify evidence requiring investigation. They do not prove a cause or
authorize stopping, accepting, or releasing product.

## Capability and performance

Given specification limits `LSL < USL`, process mean `mu`, within-process
standard deviation `sigma_w`, and overall standard deviation `sigma_o`:

```text
Cp  = (USL - LSL) / (6*sigma_w)
Cpk = min((USL-mu)/(3*sigma_w), (mu-LSL)/(3*sigma_w))
Pp  = (USL - LSL) / (6*sigma_o)
Ppk = min((USL-mu)/(3*sigma_o), (mu-LSL)/(3*sigma_o))
```

Example: `mu=10.2`, `LSL=8`, `USL=12`, `sigma_w=0.5`, and `sigma_o=0.6`
produce `Cp=1.333`, `Cpk=1.200`, `Pp=1.111`, and `Ppk=1.000`.
These indices do not prove stability, normality, adequate measurement, or
conformance of an individual unit.

## Yield metrics

```text
unit yield = conforming units / total units
DPU  = defects / units
DPO  = defects / (units * opportunities per unit)
DPMO = DPO * 1,000,000
RTY  = product of each process-step first-pass yield
```

An opportunity definition must be stable and meaningful before comparing DPO or
DPMO. Do not infer a sigma level or apply an unstated mean shift.

## Crossed Gage R&R

The kernel accepts a balanced `part × operator × replicate` array and performs a
two-factor random-effects ANOVA with interaction. It estimates repeatability,
operator, part-by-operator interaction, reproducibility, total Gage R&R, and
part-to-part variance. Negative method-of-moments components are truncated to
zero and remain visible through the component results.

Use representative parts spanning the operating range, randomized measurement
order, trained operators, normal measurement practice, and at least two
replicates. The implemented model retains interaction; it does not automatically
pool an insignificant interaction. Study variation is reported as six times the
Gage R&R standard deviation. Acceptance thresholds must come from the governing
measurement plan and engineering risk—not from this calculator.

## Tolerance accumulation

For symmetric component tolerance magnitudes `t[i]`:

```text
worst case = sum(t[i])
RSS        = sqrt(sum(t[i]^2))
```

Worst case assumes every component reaches its adverse extreme. RSS requires a
defensible independent, centered variation model. Correlation, asymmetric
tolerances, geometric effects, datum structure, thermal response, and nonlinear
sensitivity require a richer engineering model.

## Acceptance-sampling operating characteristic

For a single sample of `n`, acceptance number `c`, and independent Bernoulli
fraction nonconforming `p`, the binomial probability of acceptance is:

`P(accept) = sum(comb(n,d) * p^d * (1-p)^(n-d), d=0..c)`.

Example: `n=10`, `c=1`, and `p=0.10` gives `P(accept)=0.7361`. This function
evaluates a declared plan. It does not select a standards-based plan, establish
AQL/LTPD, or replace finite-lot hypergeometric analysis when sampling without
replacement is material.

## Two-level full factorial effects

For `k` factors coded `-1/+1`, the complete design contains `2^k` unique runs.
For a factor or interaction column `x`, its effect is

`effect = sum(y*x) / 2^(k-1)`.

The intercept is the response mean. For responses generated by
`y = 10 + 3A + 2B + AB`, the reported effects are `A=6`, `B=4`, and `A:B=2`.
With one observation per treatment combination, there is no pure-error estimate:
the calculator therefore reports effects but no significance tests. Randomize
run order, guard against time trends, verify the measurement system, select safe
factor ranges, and use confirmation runs before changing a controlled process.

## Required output record

Record the calculation version and exact inputs, result, data provenance,
excluded observations, assumptions checked, assumptions unverified, signal or
decision being considered, approver, and links to retained evidence. Attach the
record to the relevant improvement, nonconformance, qualification, or control
case.

## Public references

- [NIST Individuals Control Charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc322.htm)
- [NIST X-bar, R, and S Control Charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc321.htm)
- [NIST Proportions Control Charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc332.htm)
- [NIST Counts Control Charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc331.htm)
- [NIST Process Capability](https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc16.htm)
- [NIST Gauge R&R Studies](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc4.htm)
- [NIST Single Sampling Plans](https://www.itl.nist.gov/div898/handbook/pmc/section2/pmc23.htm)
- [NIST Two-Level Full Factorial Designs](https://www.itl.nist.gov/div898/handbook/pri/section3/pri333.htm)
- [NIST Combined Standard Uncertainty](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty)
- [ASQ Quality Body of Knowledge](https://asq.org/quality-resources/about-the-quality-body-of-knowledge)
