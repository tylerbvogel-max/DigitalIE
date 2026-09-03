# Evaluation and observability

## Question answered

Can the organization prove an agent behaves acceptably before release and detect when behavior, context, tools, or environment changes afterward?

## Evaluation stack

- Deterministic unit, schema, permission, and policy checks
- Scenario fixtures for normal, missing, conflicting, stale, malicious, and high-consequence conditions
- End-to-end tool and state-transition tests
- Human domain review for judgment-dependent outcomes
- Regression sets built from failures without importing protected data
- Runtime monitoring for input mix, tool calls, approvals, overrides, errors, latency, cost, and outcome

Version the model, instructions, skills, context/retrieval policy, tools, dependencies, and evaluation set. Re-evaluate when any behavior-bearing component changes.

## Output

Capability-specific acceptance thresholds, failure taxonomy, evaluation receipts, release comparison, runtime tripwires, incident-to-fixture loop, and retirement criteria.
