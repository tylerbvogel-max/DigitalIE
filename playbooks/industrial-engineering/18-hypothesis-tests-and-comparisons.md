# Hypothesis tests and comparisons

## Question answered

Is the observed difference inconsistent with a declared null model, how large is the effect, and is the comparison operationally meaningful?

## Test discipline

Before calculation state population, response, groups/pairs, null \(H_0\), alternative \(H_a\), significance level \(\alpha\), practical effect threshold, sampling/assignment, independence structure, distribution/variance assumptions, missing-data rule, and planned test. Do not choose one- versus two-sided testing after seeing the result.

A p-value is the probability, assuming \(H_0\) and the model, of a result at least as incompatible with \(H_0\) as observed. It is not the probability that \(H_0\) is true, the probability the result occurred by chance, or effect size.

## One population mean

Known \(\sigma\):

\[
z=\frac{\bar{x}-\mu_0}{\sigma/\sqrt n}
\]

Unknown \(\sigma\):

\[
t=\frac{\bar{x}-\mu_0}{s/\sqrt n}, \qquad df=n-1
\]

For a two-sided level-\(\alpha\) test, reject when \(|z|>z_{1-\alpha/2}\) or \(|t|>t_{1-\alpha/2,df}\), equivalently when \(p<\alpha\). “Fail to reject” does not establish equality.

## Comparing two population means

For independent groups, default to Welch's t test unless a defensible common-variance model is established:

\[
t=\frac{\bar{x}_1-\bar{x}_2-\Delta_0}{\sqrt{s_1^2/n_1+s_2^2/n_2}}
\]

\[
df\approx\frac{(s_1^2/n_1+s_2^2/n_2)^2}{(s_1^2/n_1)^2/(n_1-1)+(s_2^2/n_2)^2/(n_2-1)}
\]

For paired observations, calculate differences \(d_i=x_{i,after}-x_{i,before}\) and test:

\[
t=\frac{\bar d-\Delta_0}{s_d/\sqrt n}, \qquad df=n-1
\]

Pairing must represent the same unit or justified match; treating paired observations as independent wastes information, while false pairing corrupts it.

## Comparing proportions

One-sample null \(p=p_0\):

\[
z=\frac{\hat p-p_0}{\sqrt{p_0(1-p_0)/n}}
\]

For two independent proportions under \(H_0:p_1=p_2\), pooled \(\hat p=(x_1+x_2)/(n_1+n_2)\):

\[
z=\frac{\hat p_1-\hat p_2}{\sqrt{\hat p(1-\hat p)(1/n_1+1/n_2)}}
\]

Use an exact or otherwise appropriate small-sample method when expected event counts are insufficient for the normal approximation. Report the risk difference and interval, not only a p-value.

## Chi-square test of categorical association

For observed contingency counts \(O_{ij}\), expected under independence:

\[
E_{ij}=\frac{(\text{row }i\text{ total})(\text{column }j\text{ total})}{N}
\]

\[
\chi^2=\sum_i\sum_j\frac{(O_{ij}-E_{ij})^2}{E_{ij}}, \qquad df=(r-1)(c-1)
\]

Example for outcome by two fictional process settings, \(O=[[18,2],[12,8]]\). Expected counts are \([[15,5],[15,5]]\), so \(\chi^2=4.8\), \(df=1\), and \(p\approx0.028\). This is evidence of association under the sampling model, not proof the setting caused the outcome.

## One-way analysis of variance

For \(k\) groups with group means \(\bar{x}_j\), sizes \(n_j\), and grand mean \(\bar{x}\):

\[
SS_B=\sum_{j=1}^k n_j(\bar{x}_j-\bar{x})^2
\]

\[
SS_W=\sum_{j=1}^k\sum_i(x_{ij}-\bar{x}_j)^2
\]

\[
MS_B=\frac{SS_B}{k-1}, \quad MS_W=\frac{SS_W}{N-k}, \quad F=\frac{MS_B}{MS_W}
\]

For fictional groups \([8,9,10]\), \([11,12,13]\), and \([9,10,11]\): \(SS_B=14\), \(SS_W=6\), \(df=(2,6)\), \(MS_B=7\), \(MS_W=1\), \(F=7\), and \(p\approx0.027\). The omnibus result says at least one population mean differs; use a planned contrast or multiplicity-controlled post-hoc procedure to locate differences.

Classical one-way ANOVA assumes independent errors, constant within-group variance, and approximately normal errors for small samples. Plot group data and residuals. Use a justified robust/nonparametric design when assumptions fail; do not select it only because a normality pretest crossed 0.05.

## Errors, power, and output

Type I error rejects a true \(H_0\) with probability \(\alpha\). Type II error fails to reject a false \(H_0\) with probability \(\beta\); power is \(1-\beta\) for a specified effect/model. Sample-size planning requires the smallest important effect, variability/event rate, \(\alpha\), desired power, and design structure.

Report hypothesis, design, test/statistic/df, estimate and effect size, confidence interval, exact p-value, assumptions/diagnostics, multiplicity treatment, practical threshold, and decision. Statistical significance never overrides product specifications or authorized acceptance.
