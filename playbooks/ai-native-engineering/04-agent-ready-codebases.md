# Agent-ready codebases

## Question answered

Can a competent agent understand the system, make a bounded change, verify it, and hand it off without guessing hidden conventions?

## Required views

- System context, containers, components, and ownership
- Behavioral sequence/event flows for consequential paths
- Runtime and deployment topology
- Domain boundaries and authoritative data ownership
- ADRs for consequential choices
- Fitness functions that detect architecture and safety drift
- Delivery value stream showing wait, handoff, rework, and feedback

## Repository contract

Provide a fast start path, local instructions nearest the code they govern, deterministic setup, small composable modules, typed/stable interfaces, discoverable tests, representative fixtures, structured logs, explicit configuration, reproducible commands, and narrow permissions. Keep generated artifacts identified and regeneration commands adjacent.

## Output

Architecture manifest, instruction hierarchy, change/test map, ownership map, verification commands, fixtures, and known-risk register.
