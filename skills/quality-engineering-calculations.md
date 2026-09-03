# Quality Engineering Calculations

## Purpose

Select, frame, run, and explain deterministic quality calculations without
turning arithmetic into product disposition or process-change authority.

## Use when

- monitoring variable or attribute process data;
- separating capability from longer-term performance;
- quantifying yield or defect opportunity rates;
- evaluating a balanced crossed measurement-system study;
- comparing deterministic tolerance accumulation methods;
- evaluating a declared single-sampling plan's OC probability; or
- estimating effects from a complete two-level factorial experiment.

## Method

1. Open or identify the durable case and the decision it supports.
2. Establish the characteristic, operational definition, scope, configuration,
   status period, units, source records, and applicable specification revision.
3. Confirm measurement-system adequacy before interpreting process variation.
4. Choose the method from the data-generating mechanism, not from the desired
   conclusion. Preserve time order for control charts and run order for DOE.
5. Supply controlled chart constants and acceptance-plan parameters explicitly.
6. Call the deterministic calculator and retain exact inputs and its receipt.
7. Check assumptions: rational subgrouping, independence, stability,
   distribution, equal opportunity, balanced study design, and model form.
8. Explain the result in process language, distinguish signals from causes, and
   identify what evidence would falsify the interpretation.
9. Route acceptance, release, process change, baseline change, or qualification
   decisions to the authorized human and governing procedure.

## Tool selection

- Individuals and moving range: sequential continuous observations with no
  rational subgroup.
- X-bar/R or X-bar/S: equal rational subgroups; analyze dispersion before the
  mean chart.
- p/np: nonconforming units under a binomial model; np requires constant `n`.
- c/u: nonconformities under a Poisson model; c requires equal opportunity.
- Cp/Cpk/Pp/Ppk: stable process with defensible within and overall sigma inputs.
- Gage R&R: crossed, balanced parts/operators/replicates with interaction.
- Binomial OC: declared `(n,c)` plan and large-lot/independent approximation.
- Factorial effects: all `2^k` unique coded combinations are present.

## Stop conditions

Stop and request evidence when definitions changed, data were aggregated out of
time order, traceability is missing, subgrouping is unjustified, the measurement
system is unsuitable, a specification or sampling parameter is unofficial, or
the proposed conclusion exceeds the method's assumptions.

## Authority boundary

This skill may calculate, compare, expose assumptions, and recommend further
investigation. It may not accept or reject product, approve a sampling plan,
declare a process qualified or capable, alter a control plan or specification,
release an inspection operation, or authorize a production-process change.

## Primary reference

Use [Quantitative Quality Engineering](../playbooks/quality-assurance/09-quantitative-quality-engineering.md)
for formulas, worked examples, limits, and public sources.
