# Agentic security

## Question answered

What can influence the agent, what can the agent reach or change, and how will unsafe intent, compromised context, or excessive authority be contained?

## Threat surfaces

System/user instructions, retrieved documents, repository content, tool metadata/results, MCP servers, credentials, model/provider boundary, memory, logs, generated code, dependencies, CI/CD, and human approval interfaces.

## Controls

- Apply least privilege, task-scoped credentials, environment separation, secret isolation, and deny-by-default tools.
- Treat retrieved/tool content as untrusted data unless explicitly authoritative.
- Prevent prompt-injected content from redefining authority or tool policy.
- Require exact-target confirmation and approval for destructive or irreversible effects.
- Validate inputs/outputs deterministically where possible; sandbox execution and limit time, network, retries, and spend.
- Preserve attributable audit events without logging secrets or controlled content.
- Maintain kill, revoke, rollback, incident, and evidence-preservation paths.
- Evaluate exfiltration, confused-deputy, privilege escalation, dependency poisoning, prompt injection, and unsafe autonomy.

## Output

Threat model, capability/permission matrix, trust-boundary diagram, controls, abuse fixtures, monitoring, incident runbook, and residual-risk decision.
