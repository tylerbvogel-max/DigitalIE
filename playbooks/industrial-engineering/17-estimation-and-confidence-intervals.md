# Estimation and confidence intervals

## Question answered

What population quantity is being estimated, how uncertain is the estimate, and which assumptions make the interval defensible?

## Estimators, bias, and precision

An estimator \(\hat{\theta}\) is unbiased for \(\theta\) when:

\[
Bias(\hat{\theta})=E[\hat{\theta}]-\theta=0
\]

Mean squared error combines bias and variance:

\[
MSE(\hat{\theta})=Var(\hat{\theta})+Bias(\hat{\theta})^2
\]

The sample mean \(\bar{x}\) is an unbiased estimator of population mean \(\mu\) under the sampling model. The sample variance using \(n-1\),

\[
s^2=\frac{\sum(x_i-\bar{x})^2}{n-1},
\]

is unbiased for \(\sigma^2\) under independent identical sampling. Dividing by \(n\) estimates the variance of the observed sample descriptively but is biased downward as an estimator of population variance.

## Standard error of the mean

If population standard deviation is known:

\[
SE(\bar{x})=\frac{\sigma}{\sqrt{n}}
\]

When it is unknown, estimate it with \(s/\sqrt{n}\). Standard deviation describes variation among individual observations; standard error describes sampling variation of an estimator. More correlated measurements do not create the information of the same number of independent measurements.

## Confidence interval for one population mean

Known \(\sigma\), using a normal critical value:

\[
\bar{x}\pm z_{1-\alpha/2}\frac{\sigma}{\sqrt{n}}
\]

Unknown \(\sigma\), using Student's t with \(n-1\) degrees of freedom:

\[
\bar{x}\pm t_{1-\alpha/2,n-1}\frac{s}{\sqrt{n}}
\]

Use the z form only when \(\sigma\) is genuinely known from an applicable population/process model, not merely because the sample is large. The t procedure assumes independent observations and is sensitive to strong non-normality/outliers at small \(n\).

## Worked examples

For cycle times \(8,9,10,10,11,12\): \(\bar{x}=10\), \(s=1.414\), \(n=6\), and \(SE=1.414/\sqrt6=0.577\). With \(t_{0.975,5}=2.571\):

\[
10\pm2.571(0.577)=10\pm1.484=[8.516,11.484]
\]

If a genuinely known \(\sigma=1.2\), \(n=36\), and \(\bar{x}=10.4\), a 95% z interval is:

\[
10.4\pm1.96\frac{1.2}{6}=10.4\pm0.392=[10.008,10.792]
\]

A 95% interval is produced by a method that captures the fixed population parameter in 95% of repeated samples under the assumptions. It does not assign 95% probability to the parameter after this interval is observed.

## Proportion estimate and interval

For \(x\) events in \(n\) eligible trials, \(\hat p=x/n\). The large-sample standard error is:

\[
SE(\hat p)=\sqrt{\frac{\hat p(1-\hat p)}{n}}
\]

For small counts or proportions near 0 or 1, avoid the simple Wald interval \(\hat p\pm zSE\). Use an agreed Wilson or exact method and record the method/software. The Wilson interval is:

\[
\frac{\hat p+z^2/(2n)\ \pm\ z\sqrt{\hat p(1-\hat p)/n+z^2/(4n^2)}}{1+z^2/n}
\]

## Required interpretation

Report estimate, confidence level, interval method, sample size, sampling unit, independence/representativeness limits, practical threshold, missing/excluded records, and whether the interval is narrow enough for the decision.
