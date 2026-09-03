# Production and flow calculations

## Question answered

What production pace, resource loading, equipment losses, flow relationships, queue behavior, and repeat-unit improvement follow from a declared operating model?

These calculations support investigation and scenario comparison. They do not establish demand validity, a labor standard, an achievable cycle, equipment entitlement, queue assumptions, or a production commitment.

## Input contract

Record the product family, process boundary, time window, time unit, demand source, available-time exclusions, cycle-time basis, yield definition, and data provenance. Never mix clock hours, labor hours, machine hours, pieces, lots, or dollars without an explicit conversion.

## Pace, capacity, and resources

For available production time (T), demand (D), and effective resource cycle (C):

\[
Takt=\frac{T}{D},\qquad Capacity=\frac{T}{C},\qquad Load=\frac{C}{Takt}
\]

\[
MinimumParallelResources=\left\lceil\frac{C}{Takt}\right\rceil
\]

Example: 420 available minutes, demand of 100 units, and an eight-minute effective cycle give a 4.2-minute takt, 52.5 units of capacity per resource, 1.905 resource load, and two resources before allowances. Confirm breaks, changeovers, planned maintenance, mix, variability, qualifications, and attendance separately.

## Existing line balance

For station loads (S_j), line cycle (C_L=\max(S_j)), total work (W=\sum S_j), and (m) stations:

\[
Efficiency=\frac{W}{mC_L},\qquad BalanceDelay=1-Efficiency
\]

\[
Smoothness=\sqrt{\sum_j(C_L-S_j)^2},\qquad OutputCapacity=\frac{T}{C_L}
\]

The calculator evaluates an assignment already supplied by a human or solver. It does not prove precedence feasibility, walking distance, ergonomic acceptability, skill coverage, or buffer sufficiency.

## Overall equipment effectiveness

\[
Availability=\frac{RunTime}{PlannedProductionTime}
\]

\[
Performance=\frac{IdealCycleTime\times TotalCount}{RunTime},\qquad
Quality=\frac{GoodCount}{TotalCount}
\]

\[
OEE=Availability\times Performance\times Quality
=\frac{IdealCycleTime\times GoodCount}{PlannedProductionTime}
\]

The implementation rejects performance above one because that normally signals inconsistent counts, time units, or ideal-cycle definition. Rework treatment and the definition of a good unit must be declared. NIST notes that OEE conventions vary and comparability must be established before benchmarking.

## Flow and yield

For a stable boundary and common long-run period, Little's Law is:

\[
WIP=Throughput\times LeadTime
\]

The function accepts exactly two terms and derives the third. Process-cycle efficiency is:

\[
PCE=\frac{ValueAddedTime}{LeadTime}
\]

For first-pass yields (Y_i):

\[
RTY=\prod_iY_i
\]

Do not use Little's Law across different boundaries or transient periods. RTY needs the same unit population and first-pass definition at each step.

## Queue approximations

`mm1_queue` assumes Poisson arrivals, exponential service, one server, first-come service, an unlimited population and queue, independence, and steady state with \(\lambda<\mu\). With \(\rho=\lambda/\mu\):

\[
L_q=\frac{\rho^2}{1-\rho},\quad L=\frac{\rho}{1-\rho},\quad
W_q=\frac{L_q}{\lambda},\quad W=\frac{1}{\mu-\lambda}
\]

`mmc_queue` applies Erlang C to identical parallel servers and requires \(\lambda<c\mu\). It calculates utilization, probability of waiting, queue/system counts, and queue/system time. Both functions fail on unstable loading. Manufacturing arrivals and service times are often scheduled, batched, blocked, or non-exponential; validate the stochastic model before acting on its output.

## Unit learning curve

For first-unit effort (Y_1), unit number (x), and learning rate (r):

\[
b=\frac{\log(r)}{\log(2)},\qquad Y_x=Y_1x^b
\]

At a fictional 80-percent unit curve and 100 hours for unit one, unit two is 80 hours and unit four is 64 hours. The function returns each unit and their sum; it implements the unit/Crawford convention, not the cumulative-average/Wright convention. NASA warns that learning-curve applicability can be weak for low-quantity space production. Configuration changes, breaks in production, automation, rate, workforce turnover, and supplier content must be analyzed.

## Output

Preserve declared scope and units, raw inputs, formula version, results, undefined values, assumption checks, sensitivity cases, and human conclusion in a calculation record. Pair unfavorable metrics with Gemba evidence and a loss tree rather than declaring cause from arithmetic.

Primary public orientation: [NIST manufacturing KPI/OEE discussion](https://www.nist.gov/system/files/documents/2017/04/18/04_bernstein_applying_visual_variables.pdf), [U.S. Air Force rapid-improvement guide](https://media.defense.gov/2007/Aug/13/2001453362/-1/-1/0/AFSO21RIE.pdf), [NASA learning-curve guidance](https://ntrs.nasa.gov/citations/19760006882), and the [NASA Cost Estimating Handbook](https://www.nasa.gov/ocfo/ppc-corner/nasa-cost-estimating-handbook-ceh/).
