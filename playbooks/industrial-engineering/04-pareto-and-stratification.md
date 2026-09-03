# Pareto and stratification

## Question answered

Where is the loss concentrated, and what meaningful categories distinguish it?

## Procedure

1. Define event and denominator: defect count, defect rate, delay minutes, dollars, or rework hours.
2. Select a window long enough to avoid a one-off narrative.
3. Stratify by process/station, product/configuration, defect code, shift, supplier/material lot, equipment, time, and operator role when appropriate.
4. Confirm categories are complete, mutually understood, and not hiding an “other” bucket that should be investigated.
5. Use frequency and impact separately when they tell different stories.

## Calculations

For category \(j\) with count or impact \(x_j\):

\[
Share_j=\frac{x_j}{\sum_k x_k}, \qquad CumulativeShare_j=\frac{\sum_{k=1}^{j}x_{(k)}}{\sum_k x_k}
\]

where \(x_{(k)}\) is ordered from largest to smallest. For a defect rate use \(r_j=d_j/N_j\), with category-specific defects \(d_j\) and eligible exposure \(N_j\); do not rank raw defect count as though exposure were equal.

Example: fictional rework hours \(A=40,B=25,C=20,D=15\), total \(100\). Shares are 40%, 25%, 20%, 15%; cumulative shares are 40%, 65%, 85%, 100%. The first three contain 85% of hours, but this does not show whether they have the highest rate or share a cause.

## Questions that prevent bad inference

- Is the apparent leader simply the highest-volume product or station?
- Did the categorization method change during the window?
- Is the numerator paired with a valid exposure denominator?
- Does a category indicate a mechanism or merely where to look next?

## Exit

Name the vital few investigation targets and the stratification cuts that should inform Gemba and hypothesis generation.
