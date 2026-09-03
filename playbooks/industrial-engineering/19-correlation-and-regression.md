# Correlation and simple linear regression

## Question answered

How strongly do two continuous variables move together under a linear model, what change in response is associated with a change in predictor, and what structure remains unexplained?

## Begin with the graph and mechanism

Plot paired raw observations \((x_i,y_i)\) in process/time order and by meaningful strata. Confirm pairing, units, measurement suitability, range, missingness, temporal direction, and plausible mechanism. A pooled trend can reverse within product, machine, or shift strata.

## Pearson linear correlation

Define:

\[
S_{xx}=\sum(x_i-\bar{x})^2, \quad S_{yy}=\sum(y_i-\bar{y})^2, \quad S_{xy}=\sum(x_i-\bar{x})(y_i-\bar{y})
\]

\[
r=\frac{S_{xy}}{\sqrt{S_{xx}S_{yy}}}, \qquad -1\le r\le1
\]

Pearson \(r\) measures linear association. It can be near zero for a strong nonlinear relationship and can be dominated by one influential point. Correlation does not establish causality, agreement, or interchangeability.

## Hypothesis test for linear correlation

For \(H_0:\rho=0\) under independent bivariate-normal sampling:

\[
t=r\sqrt{\frac{n-2}{1-r^2}}, \qquad df=n-2
\]

Reject according to the preselected alternative and significance level. A test of zero correlation does not validate linearity or prove a useful effect.

## Simple linear regression

Model:

\[
y_i=\beta_0+\beta_1x_i+\varepsilon_i
\]

Least-squares estimates:

\[
b_1=\frac{S_{xy}}{S_{xx}}, \qquad b_0=\bar{y}-b_1\bar{x}
\]

Prediction and residual:

\[
\hat y_i=b_0+b_1x_i, \qquad e_i=y_i-\hat y_i
\]

The slope estimates response change per unit of \(x\) within the observed design/range. The intercept may lack physical meaning when \(x=0\) is outside that range.

## Model significance and determination

\[
SST=\sum(y_i-\bar y)^2, \quad SSE=\sum(y_i-\hat y_i)^2, \quad SSR=\sum(\hat y_i-\bar y)^2
\]

With an intercept, \(SST=SSR+SSE\) and:

\[
R^2=\frac{SSR}{SST}=1-\frac{SSE}{SST}
\]

For simple regression:

\[
MSE=\frac{SSE}{n-2}, \quad SE(b_1)=\sqrt{\frac{MSE}{S_{xx}}}, \quad t=\frac{b_1-\beta_{1,0}}{SE(b_1)}
\]

The overall regression test of \(H_0:\beta_1=0\) uses:

\[
F=\frac{MSR}{MSE}=\frac{SSR/1}{SSE/(n-2)}
\]

In simple regression, \(F=t^2\). \(R^2\) is the sample fraction of response variation explained by the fitted linear model; it is not prediction accuracy, causal contribution, or probability the model is correct.

## Worked example

For fictional paired observations \(x=[1,2,3,4,5]\), \(y=[2,4,5,4,8]\):

```text
x̄ = 3.0, ȳ = 4.6
Sxx = 10.0, Syy = 19.2, Sxy = 12.0
b1 = 12 / 10 = 1.2
b0 = 4.6 - 1.2(3) = 1.0
fitted model: ŷ = 1.0 + 1.2x
r = 0.8660; R² = 0.7500
residuals = [-0.2, 0.6, 0.4, -1.8, 1.0]
SSE = 4.8; SSR = 14.4; MSE = 1.6
SE(b1) = 0.4; t = 3.0 with df = 3; F = 9.0
```

With only five observations, the two-sided slope test has \(p\approx0.058\). A seemingly large \(R^2\) does not erase the small sample, residual pattern, or uncertainty.

## Residual diagnostics

Check residuals versus fitted value, predictor, time/order, and important omitted factors; use a normal probability plot for inference at small sample sizes. Investigate curvature, changing spread, autocorrelation, clusters, and influential observations. Do not delete a point solely because it weakens significance.

Inference assumes a correctly specified linear mean, independent zero-mean errors, constant error variance, and approximately normal errors for small-sample tests/intervals. Prediction outside the observed \(x\) range is extrapolation and must be labeled.

## Output

Paired-data reference, scatterplot/strata, model equation with units and valid range, \(r\), slope/intercept intervals, test statistic/df/p-value, \(R^2\), residual diagnostics, influential-point sensitivity, prediction uncertainty, mechanism limits, and decision relevance.
