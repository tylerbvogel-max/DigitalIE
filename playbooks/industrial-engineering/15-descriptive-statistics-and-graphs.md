# Descriptive statistics and graphs

## Question answered

What does the observed dataset contain, where is it centered, how much does it vary, and which graphical view exposes its shape or operating pattern?

## Calculation record first

Record population of interest, sampling/collection method, unit of analysis, operational definition, measurement unit, time order, exclusions, missing-data treatment, subgroup/stratum, and immutable input reference. Preserve full precision in calculation and round only the reported result.

Let observations be \(x_1,\ldots,x_n\).

## Data type and collection design

Classify the response before selecting arithmetic or a graph:

| Data structure | Examples | Valid treatment |
|---|---|---|
| Nominal category | defect family, supplier, machine ID | counts, proportions, mode; no numeric ordering |
| Ordinal category | severity band, inspection rating | ordered counts/quantiles; spacing between levels is not assumed equal |
| Interval measure | temperature in °C | differences are meaningful; ratios to the arbitrary zero are not |
| Ratio measure | duration, mass, length, count | differences and ratios are meaningful when the measurement model is valid |

Also distinguish discrete counts from continuous measurements and preserve censoring, rounding, detection limits, and repeated measurements. Numeric codes assigned to categories do not turn them into quantitative measurements.

Describe how observations entered the dataset. A simple random sample gives eligible units a defined selection probability; stratified sampling deliberately represents important strata; cluster sampling selects natural groups and ordinarily requires cluster-aware analysis. Convenience samples, dashboard extracts, and completed units may systematically omit work in queue, scrap, rework, or inaccessible conditions. Random sampling supports population inference; random assignment supports causal attribution. One does not substitute for the other.

## Frequency distribution

For category or bin \(j\):

\[
f_j = \text{count in }j, \qquad p_j = \frac{f_j}{n}, \qquad F_j = \sum_{k\le j} f_k
\]

Use mutually exclusive, collectively exhaustive categories. For histograms, disclose bin boundaries and keep them constant across comparisons. Counts answer volume; relative frequency answers composition; a rate requires an exposure denominator.

Example for defect counts \(A=12\), \(B=5\), \(C=3\), with \(n=20\): relative frequencies are \(0.60,0.25,0.15\), and ordered cumulative relative frequencies are \(0.60,0.85,1.00\). Ordering categories for a Pareto view is an analytical display choice, not an ordinal measurement scale.

## Central tendency

\[
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
\]

\[
\bar{x}_w=\frac{\sum_i w_i x_i}{\sum_i w_i}
\]

The median is the ordered middle value, or the mean of the two middle values for even \(n\). The mode is the most frequent value/category. Use the median with strong skew or outliers; use a weighted mean only when weights have an explicit operational meaning.

For a symmetric trim removing \(g\) observations from each tail after ordering,

\[
\bar{x}_{trim}=\frac{1}{n-2g}\sum_{i=g+1}^{n-g}x_{(i)}
\]

State \(g\) or the trim percentage. A trimmed mean is a predeclared robustness summary, not permission to hide inconvenient observations.

## Dispersion

\[
R=x_{\max}-x_{\min}
\]

\[
s^2=\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}, \qquad s=\sqrt{s^2}
\]

For a complete population, replace \(n-1\) with \(N\) and use \(\mu\) and \(\sigma\). The interquartile range is \(IQR=Q_3-Q_1\). For a positive ratio-scale measure, \(CV=s/\bar{x}\); do not use CV when zero is arbitrary or the mean is near zero.

Quantile algorithms differ across software. Record the method when a quartile or percentile affects a decision.

## Worked example

Cycle times in minutes: \(8,9,10,10,11,12\).

```text
n = 6
mean = 60 / 6 = 10.000
median = (10 + 10) / 2 = 10.000
mode = 10
range = 12 - 8 = 4
sum of squared deviations = 10
sample variance = 10 / (6 - 1) = 2.000 min²
sample standard deviation = sqrt(2) = 1.414 min
```

The calculation describes these six observations. It does not prove that the process is stable, normally distributed, capable, or representative of future production.

## Graph selection

| Question | Graph | Required discipline |
|---|---|---|
| What is the distribution shape? | histogram, dot plot, ECDF | show units, bin rule where applicable, and sample size |
| Where are center, spread, and outliers? | box plot plus raw points | state quartile convention; investigate rather than delete outliers |
| How does the measure move through time? | run chart or control chart | preserve sequence; do not use an unordered bar chart |
| Which categories dominate count or impact? | Pareto chart | disclose denominator, ordering, and “other” composition |
| Do two continuous variables move together? | scatterplot | show raw points and meaningful strata before fitting |
| Do groups differ? | interval/box/dot plot by group | show within-group variation and sample size |
| Does a fitted model miss structure? | residual plots | plot residual versus fit, order, and relevant factors |

Axes start at a meaningful origin for magnitude comparisons; truncation must be visible. Do not use dual axes, 3-D decoration, or area/volume encodings that distort comparisons.

## Output

Reproducible dataset reference, frequency table, selected statistics with units, graph with declared construction, anomalies/strata, and the next decision or test.
