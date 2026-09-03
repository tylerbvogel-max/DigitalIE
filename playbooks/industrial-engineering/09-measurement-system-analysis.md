# Measurement-system analysis (MSA)

## Question answered

Is the measurement system adequate for the decision we are about to make?

Do this before capability claims, tight process comparisons, or root-cause claims that rest on a measured difference. A calibrated instrument can still be unfit for the decision.

## Start with the decision

State what the measure will decide: accept/reject a part, detect process shift, compare alternatives, or estimate a continuous characteristic. Then define resolution, range, environmental conditions, part presentation, appraiser method, sampling, and traceability.

## Select the study

| Situation | Study |
|---|---|
| Continuous measurement, multiple appraisers | Gage R&R: repeatability and reproducibility |
| Pass/fail or defect classification | Attribute agreement / false accept and false reject |
| Concern over time | Stability study / control chart of reference artifact |
| Concern across range | Bias and linearity study |
| Consumptive or one-off test | Nested, destructive, or alternate validation design |

## Interpret operationally

Compare measurement variation with tolerance, expected process variation, and decision risk. Review appraiser-by-part interaction, bias, resolution, and cost of bad decisions. If the system cannot distinguish the change, improve the measure or redesign the experiment.

## Core quantities

For repeated measurement of a reference value \(x_{ref}\):

\[
Bias=\bar{x}_{observed}-x_{ref}
\]

For variance-component estimates from an appropriate crossed/nested/ANOVA study:

\[
\sigma_{GRR}=\sqrt{\sigma_{repeatability}^2+\sigma_{reproducibility}^2}
\]

\[
\sigma_{total}=\sqrt{\sigma_{part}^2+\sigma_{GRR}^2}, \quad \%StudyVariation=100\frac{\sigma_{GRR}}{\sigma_{total}}
\]

\[
ndc=1.41\frac{\sigma_{part}}{\sigma_{GRR}}
\]

Example: if a justified study estimates \(\sigma_{GRR}=0.8\) and \(\sigma_{part}=3.0\), then \(\sigma_{total}=\sqrt{0.8^2+3.0^2}=3.105\), percent study variation is 25.8%, and \(ndc=5.29\) (report the locally defined integer convention). These numbers require operational judgment against the intended decision; a universal percent cutoff does not replace false-accept/false-reject risk.

## Exit

Publish the operational definition and evidence that the measure is fit for the intended decision; otherwise label downstream findings as provisional.
