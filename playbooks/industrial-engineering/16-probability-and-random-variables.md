# Probability and random variables

## Question answered

What uncertainty model connects possible observations to their likelihood, and is that model defensible for the manufacturing mechanism and sampling process?

## Probability rules

For event \(A\), \(0\le P(A)\le1\) and \(P(A^c)=1-P(A)\).

\[
P(A\cup B)=P(A)+P(B)-P(A\cap B)
\]

\[
P(A\mid B)=\frac{P(A\cap B)}{P(B)}, \qquad P(A\cap B)=P(A\mid B)P(B)
\]

If \(A\) and \(B\) are independent, \(P(A\cap B)=P(A)P(B)\). Do not infer independence because two labels are different.

Bayes' rule updates a cause/event probability after evidence \(B\):

\[
P(A\mid B)=\frac{P(B\mid A)P(A)}{P(B)}
\]

## Random variables

For a discrete random variable \(X\) with probability mass \(p(x)\):

\[
E[X]=\sum_x xp(x), \qquad Var(X)=E[(X-\mu)^2]=E[X^2]-\mu^2
\]

For a continuous random variable with density \(f(x)\):

\[
P(a\le X\le b)=\int_a^b f(x)\,dx, \quad F(x)=P(X\le x)=\int_{-\infty}^{x} f(t)\,dt
\]

For the normal model \(X\sim N(\mu,\sigma^2)\), standardize with:

\[
Z=\frac{X-\mu}{\sigma}
\]

## Common manufacturing models

| Model | Parameters and formulas | Plausible use |
|---|---|---|
| Bernoulli | \(X\in\{0,1\}\), \(P(X=1)=p\), \(E[X]=p\), \(Var(X)=p(1-p)\) | one unit conforming/nonconforming under a stable definition |
| Binomial | \(X\sim Bin(n,p)\), \(P(X=x)={n\choose x}p^x(1-p)^{n-x}\), \(E[X]=np\), \(Var(X)=np(1-p)\) | count of nonconforming units in fixed \(n\), independent and common \(p\) |
| Hypergeometric | \(P(X=x)=\frac{{K\choose x}{N-K\choose n-x}}{{N\choose n}}\), \(E[X]=nK/N\) | successes in a sample of \(n\) drawn without replacement from a finite lot of \(N\) containing \(K\) successes |
| Poisson | \(P(X=x)=e^{-\lambda}\lambda^x/x!\), \(E[X]=Var(X)=\lambda\) | event count over constant exposure when occurrence assumptions are credible |
| Normal | density determined by \(\mu,\sigma\) | continuous output produced by many small effects; validate shape/tails |

## Worked examples

If the stable probability of a nonconforming unit were \(p=0.02\), then for ten independent units:

\[
P(X\ge1)=1-P(X=0)=1-(0.98)^{10}=0.1829
\]

This is not permission to assume a 2% constant defect probability. Configuration mix, batches, tools, shifts, and common-cause events can violate identical and independent trials.

If a finite lot has \(N=20\) units including \(K=3\) nonconforming units, the probability that a sample of \(n=5\) contains exactly \(x=1\) nonconforming unit is:

\[
P(X=1)=\frac{{3\choose1}{17\choose4}}{{20\choose5}}=0.4605
\]

This model is descriptive unless \(K\) is known. Acceptance-sampling plans require the applicable approved plan, risks, and authority; this equation does not create an acceptance rule.

For a Poisson rate \(r\) per exposure unit and exposure \(t\), use \(\lambda=rt\). Do not compare raw event counts across unequal hours, units, opportunities, or inspected surface area.

For \(X\sim N(50,2^2)\), an observation of 54 has \(z=(54-50)/2=2\). The z-score locates the observation within the assumed distribution; it does not determine conformance unless 54 is compared with an applicable specification.

## Central limit theorem

For independent observations from a population with finite mean \(\mu\) and variance \(\sigma^2\), the sample mean approaches a normal distribution as \(n\) grows:

\[
\bar{X}\approx N\left(\mu,\frac{\sigma^2}{n}\right)
\]

The approximation rate depends on skew, tails, dependence, and sampling design; “\(n\ge30\)” is not a universal release rule. The theorem concerns the distribution of sample means, not the shape of individual measurements.

## Output

Event/random-variable definition, assumed distribution, parameter source, independence/exposure justification, probability calculation, sensitivity to assumptions, and operational interpretation.
