# Parallel agent orchestration

## Question answered

When should work be split across agents, how are collisions prevented, and how are results integrated without multiplying unverified claims?

## Parallelization test

Delegate only when tasks have separable objectives, bounded inputs, declared write ownership, independent acceptance criteria, and useful work that can proceed concurrently. Keep tightly coupled design decisions and shared-file edits serial unless isolated worktrees or explicit ownership make them safe.

## Work contract

Each task packet contains objective, scope, non-goals, authoritative context, permitted tools/actions, owned files/resources, dependencies, output format, evidence required, stop conditions, and merge owner.

Use a coordinator for decomposition, dependency tracking, conflict detection, integration, and final verification. Worker completion is a proposal until the coordinator validates the artifact against the shared definition of done.

## Measures

Cycle-time reduction, coordination overhead, collision/rework rate, verification failure, context duplication, idle dependency time, and cost per accepted outcome.
