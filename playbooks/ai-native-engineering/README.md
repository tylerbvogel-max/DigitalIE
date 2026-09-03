# AI-native engineering playbooks

AI-native engineering designs work so humans and agents can jointly discover, change, verify, and operate systems without surrendering authority or traceability.

| Need | Start here |
|---|---|
| Package repeatable expert behavior | [Skill engineering](01-skill-engineering.md) |
| Supply the right information at the right time | [Context engineering](02-context-engineering.md) |
| Expose systems safely to agents | [MCP portals](03-mcp-portals.md) |
| Make a repository legible and changeable by agents | [Agent-ready codebases](04-agent-ready-codebases.md) |
| Review machine-produced changes rigorously | [Agentic code review](05-agentic-code-review.md) |
| Threat-model agent behavior and tool access | [Agentic security](06-agentic-security.md) |
| Split work across background agents | [Parallel agent orchestration](07-parallel-agent-orchestration.md) |
| Turn delivery into a repeatable production system | [Software factories](08-software-factories.md) |
| Prove behavior and detect regression | [Evaluation and observability](09-evaluation-and-observability.md) |

## Governing model

```text
Intent → scoped context → plan → bounded tools → change
       → independent verification → human gate → release
       → runtime evidence → evaluation → improved skill/context
```

Use deterministic automation when rules are stable and inspectable. Use an agent when the work requires interpretation, tool selection, multi-step adaptation, or unstructured evidence. Do not add an agent merely to make an existing script conversational.
