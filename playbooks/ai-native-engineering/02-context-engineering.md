# Context engineering

## Question answered

What is the smallest high-signal context that lets an agent act correctly at this step, and how is that context refreshed over a long-running task?

## Context layers

1. Standing policy and authority boundaries
2. Task intent, scope, definition of done, and current state
3. Repository/system map and applicable local instructions
4. Retrieved evidence with provenance and freshness
5. Tool contracts and observed results
6. Working memory: decisions, assumptions, unresolved questions, and handoff state

## Control rules

- Retrieve just in time; do not front-load an entire corpus.
- Distinguish instructions from untrusted content and observed tool output.
- Prefer authoritative artifacts over summaries; cite the exact source used.
- Compact by preserving decisions, evidence links, failures, and open state—not conversational texture.
- Detect stale context when source revisions, permissions, or task state change.
- Measure whether injected context was used and whether it improved the decision.

## Output

Context contract, retrieval routes, precedence rules, compaction/handoff format, freshness checks, and evaluation cases for missing, excessive, conflicting, and malicious context.
