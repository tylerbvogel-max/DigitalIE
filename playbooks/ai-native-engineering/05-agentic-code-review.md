# Agentic code review

## Question answered

How is an agent-produced change challenged for correctness, security, architecture, operations, and unintended scope before it becomes trusted?

## Review sequence

1. Reconstruct intent, acceptance criteria, authority, and changed surfaces.
2. Inspect the diff before accepting the agent's narrative.
3. Trace behavior through callers, consumers, data, permissions, deployment, rollback, and observability.
4. Run the narrowest decisive tests, then relevant regression and architecture checks.
5. Add or strengthen a fixture that would fail before the fix and pass after it.
6. Separate blocking defects, risks, questions, and optional improvements.
7. Verify the final state and report evidence, residual risk, and untested boundaries.

Use independent reviewer context for high-risk changes so the critic does not inherit the implementer's assumptions. Never use model agreement as verification.

## Output

Evidence-ranked findings with file/line location, mechanism, impact, reproduction, required fix, verification receipt, and residual risk.
