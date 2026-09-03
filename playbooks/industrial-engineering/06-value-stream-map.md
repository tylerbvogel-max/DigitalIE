# Value-stream mapping

## Question answered

How does value and information actually flow from trigger to customer, and where do delay, inventory, handoff, rework, and ambiguity accumulate?

## Map

For each step capture: trigger/input, work performed, output/customer, touch time, elapsed/queue time, WIP, first-pass yield/rework loop, handoff, information system, cadence, and owner. Walk the path instead of mapping solely from organizational charts.

Calculate total lead time and touch time from observed values; mark estimates. Investigate the gap for queues, approvals, handoffs, and rework.

## Flow calculations

\[
TotalLeadTime=\sum_j ElapsedTime_j, \qquad TotalTouchTime=\sum_j TouchTime_j
\]

\[
ProcessCycleEfficiency=\frac{TotalTouchTime}{TotalLeadTime}
\]

For a stable boundary and common units, Little's Law is:

\[
WIP=ThroughputRate\times LeadTime
\]

Rolled throughput yield across \(k\) steps, using first-pass yields \(FPY_j\):

\[
RTY=\prod_{j=1}^{k}FPY_j
\]

Example: a fictional case has 40 minutes touch time in 10 days elapsed time, using 8 hours/day: \(PCE=40/(10\times480)=0.00833=0.833\%\). At stable throughput of 6 units/day and 10-day lead time, Little's Law predicts 60 units average WIP. Three steps with FPY 0.95, 0.90, and 0.98 have \(RTY=0.8379\), despite no single step yielding below 90%.

## Diagnose before redesign

Ask whether waiting comes from capacity, release policy, batch size, approvals, missing information, changeovers, material availability, priorities, or defect/rework. Do not prescribe automation before finding the governing constraint.

## Exit

Choose one flow experiment with a measurable lead-time, WIP, yield, or handoff outcome and an owner.
