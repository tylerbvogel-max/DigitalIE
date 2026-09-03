# Statistical process control

## Question answered

Is observed variation consistent with the process’s usual behavior, or is there evidence of a special cause requiring investigation?

## Before calculation

- Confirm the measurement definition and system are fit for purpose.
- Preserve raw data and document extraction/filtering.
- Select rational subgroups based on how the process produces variation.
- Choose a chart appropriate to data type and subgrouping.
- Separate specifications (customer/design acceptability) from control limits (process behavior).

## Interpretation discipline

A control-chart signal is evidence that something atypical occurred. It does not identify the cause. A stable process may still be incapable of meeting specification; an unstable process is not meaningfully summarized by a single capability number.

## Required analysis record

Metric definition, population/window, sampling/subgroup rule, chart and rule set, limits, exclusions, missing-data treatment, detected signals, and reproducible input reference.

## Core equations

For an Individuals–Moving Range chart with sequential observations:

\[
MR_i=|x_i-x_{i-1}|, \quad \hat\sigma=\bar{MR}/d_2
\]

For moving ranges of two, \(d_2=1.128\):

\[
UCL_X=\bar{x}+3\hat\sigma, \quad CL_X=\bar{x}, \quad LCL_X=\bar{x}-3\hat\sigma
\]

\[
UCL_{MR}=3.267\bar{MR}, \quad CL_{MR}=\bar{MR}, \quad LCL_{MR}=0
\]

For \(m\) rational subgroups of constant size \(n\):

\[
\bar{\bar{x}}=\frac{1}{m}\sum_j\bar{x}_j, \quad \bar R=\frac{1}{m}\sum_jR_j
\]

\[
UCL_{\bar X}=\bar{\bar{x}}+A_2\bar R, \quad LCL_{\bar X}=\bar{\bar{x}}-A_2\bar R
\]

\[
UCL_R=D_4\bar R, \quad LCL_R=D_3\bar R
\]

Use published constants for the exact subgroup size and verify them in the calculation record. Analyze the dispersion chart before the center chart.

For fraction nonconforming with sample-specific size \(n_i\), \(\bar p=\sum d_i/\sum n_i\):

\[
UCL_i=\bar p+3\sqrt{\frac{\bar p(1-\bar p)}{n_i}}, \quad LCL_i=\max\left(0,\bar p-3\sqrt{\frac{\bar p(1-\bar p)}{n_i}}\right)
\]

## Worked Individuals example

For fictional values \(10.1,9.9,10.2,10.0,9.8\), \(\bar x=10.0\), moving ranges are \(0.2,0.3,0.2,0.2\), and \(\bar{MR}=0.225\). Thus \(\hat\sigma=0.225/1.128=0.1995\), giving individual limits approximately \([9.4015,10.5985]\), and \(UCL_{MR}=3.267(0.225)=0.7351\). These preliminary limits do not establish control with five points; they demonstrate the calculation.

## Capability after stability

For a stable process with applicable two-sided specifications:

\[
C_p=\frac{USL-LSL}{6\hat\sigma}, \quad C_{pk}=\min\left(\frac{USL-\bar{x}}{3\hat\sigma},\frac{\bar{x}-LSL}{3\hat\sigma}\right)
\]

State whether \(\hat\sigma\) estimates within-subgroup or overall variation. Do not compute a reassuring capability index for an unstable process, mixed distribution, inappropriate specification, or unfit measurement system.

## Exit

Either establish a stable baseline/control plan or direct Gemba and hypothesis testing toward a specific special-cause period or condition.
