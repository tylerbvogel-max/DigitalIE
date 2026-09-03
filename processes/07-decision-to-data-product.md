# Decision to data product

**Trigger:** a decision is slow, disputed, manual, or based on fragmented evidence.

1. Name user, decision, action window, current source records, error cost, and authority boundary.
2. Trace data authority, keys, definitions, transformations, latency, access, and reconciliation requirements.
3. Build the smallest view, alert, workflow, or agent that reduces the stated decision friction.
4. Test against real cases, including stale data, missing records, and plausible wrong recommendations.
5. Monitor use, decision outcome, data quality, and harmful failure modes; retire products that do not improve a decision.

**Outputs:** data contract, lineage map, evaluated decision aid, human review rule, and operating owner.

**Calls:** Digital Operations & Data plus the functional playbook for the decision domain.

## Process contract

| State | Minimum evidence | Exit condition |
|---|---|---|
| Decision framed | user, action, deadline, authority, error cost | measurable decision friction and owner confirmed |
| Source/lineage | sources, keys, grain, definitions, timing, access | authoritative/reconciled contract and blind spots documented |
| Prototype | smallest useful output and human review rule | representative cases and failure tests defined |
| Evaluation | normal, stale, missing, conflicting, and high-consequence fixtures | measured benefit and harmful-failure bounds reviewed |
| Operated | owner, monitoring, access, correction, retirement plan | use/outcome and data/model drift visible |
| Retired/revised | trigger or failed value/risk threshold | consumers notified and controlled dependencies resolved |

**Decision gates:** data access, controlled-record change, production direction, product disposition/release, technical compliance, and automated action remain separately authorized.

**Measures:** decision latency, evidence-assembly time, reconciliation failures, freshness/coverage, human override with reason, false reassurance, harmful recommendation, use-to-action conversion, and outcome benefit.
