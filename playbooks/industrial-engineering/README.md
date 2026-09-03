# Industrial Engineering field playbooks

Choose the method from the problem shape.

| Situation | Start here | Common misuse |
|---|---|---|
| Immediate safety/quality/delivery abnormality | [Triage and framing](00-triage-and-framing.md) | Full RCA before containment |
| Need to understand actual work | [Gemba](01-gemba.md) | A conference-room process map |
| Narrow, repeatable effect | [5 Why](02-five-whys.md) | Proof of a single cause |
| Many plausible contributors | [Ishikawa](03-ishikawa.md) | A root-cause conclusion |
| Defects/delay concentrated in categories | [Pareto](04-pareto-and-stratification.md) | A causal explanation |
| Variation through time | [SPC](05-spc.md) | Specifications or capability |
| Excess lead time, queues, rework, handoffs | [Value-stream map](06-value-stream-map.md) | A system anatomy diagram |
| Chronic cross-functional gap | [DMAIC / PDCA](07-dmaic-pdca.md) | A bureaucratic phase checklist |
| Anticipate failure before release/change | [FMEA](08-fmea.md) | A paperwork-only risk score |
| Doubt whether data is trustworthy enough to decide | [MSA](09-measurement-system-analysis.md) | A one-time calibration check |
| Need to sustain a verified improvement | [Control plan](10-control-plan.md) | A document without a reaction path |
| Actual work differs from intended work | [Standard work](11-standard-work.md) | A policy or training deck |
| Need a loss language for an asset/cell | [OEE and loss tree](12-oee-and-loss-trees.md) | A complete measure of business performance |
| Missed output / overload / uneven flow | [Capacity and line balancing](13-capacity-and-line-balancing.md) | Headcount arithmetic alone |
| A technically sound change is not sticking | [Change management](14-change-management.md) | Announcement or compliance theater |
| Need distribution, center, spread, or an honest graph | [Descriptive statistics and graphs](15-descriptive-statistics-and-graphs.md) | Averages without raw shape, time order, or denominator |
| Need to calculate uncertainty for events or measurements | [Probability and random variables](16-probability-and-random-variables.md) | Assuming independence or a distribution from convenience |
| Need an estimate, standard error, or confidence interval | [Estimation and confidence intervals](17-estimation-and-confidence-intervals.md) | Treating confidence as certainty or standard deviation as standard error |
| Need to test or compare means, proportions, or categories | [Hypothesis tests and comparisons](18-hypothesis-tests-and-comparisons.md) | P-value as effect size, causality, or product acceptance |
| Need correlation, regression, model significance, or residual analysis | [Correlation and regression](19-correlation-and-regression.md) | Correlation as causality or R² as model validity |
| Resources, routes, sequences, or policies interact through constraints | [Operations-research modeling](20-operations-research-modeling.md) | An optimum mistaken for operational truth |
| Human capability or station design affects safety, quality, or flow | [Human factors, ergonomics, and work measurement](21-human-factors-ergonomics-and-work-measurement.md) | Blaming a person for a system-design problem |
| Equipment, material, people, and support flow require a physical arrangement | [Facility layout and material handling](22-facility-layout-and-material-handling.md) | A flow score that hides safety or control constraints |
| Need deterministic pace, OEE, flow, queue, yield, or learning arithmetic | [Production and flow calculations](23-production-flow-calculations.md) | A narrow model treated as production entitlement |
| Need a transparent location, scoring, assignment, or dispatch model | [Transparent operations research](24-transparent-operations-research.md) | An optimum for an incomplete model |

Each playbook ends with a next action, owner, and measure.

## Statistical calculation standard

For a material calculation, preserve the evidence dataset and report population/estimand, sampling unit, operational definition, units, filters/missingness, study design, selected equation, substituted values, unrounded result, software/function/version, assumptions/diagnostics, uncertainty/effect, and decision boundary. Use the [statistical analysis record](../../templates/statistical-analysis-record.md).

The dependency-free [calculation kernel](../../src/digital_ie/statistics.py) implements and regression-tests documented descriptive, discrete-probability, t-statistic, Welch comparison, chi-square, runs, ANOVA, correlation, and simple-regression equations. It verifies arithmetic only; it cannot establish measurement fitness, sampling validity, model assumptions, causality, specification conformance, or decision authority.

Primary orientation reference: [NIST/SEMATECH e-Handbook of Statistical Methods](https://www.itl.nist.gov/div898/handbook/). Local approved procedures and qualified statistical/domain review govern consequential applications.
