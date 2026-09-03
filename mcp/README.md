# DigitalIE MCP contract

The MCP exposes domain verbs, never arbitrary SQL or unrestricted plant writes.

| Tool | Effect |
|---|---|
| `create_case` | Open a case in triage with a problem statement and owner |
| `record_observation` | Append an attributed observation linked to evidence where available |
| `attach_evidence` | Register immutable evidence and its provenance |
| `propose_hypothesis` | Create a testable causal claim; defaults to `proposed` |
| `record_validation_result` | Attach test outcome and supporting/rejecting evidence |
| `verify_root_cause` | Requires evidence, validation, and human approver |
| `run_analysis` | Run a versioned statistical or flow analysis against declared inputs |
| `create_action` | Assign a corrective action and effectiveness metric |
| `record_effectiveness_review` | Record post-change measured outcome |
| `render_case_report` | Generate a noncanonical report projection |

Tool responses return stable IDs, provenance, and state transitions. The future service layer authorizes every write and appends an audit event.

## Portal governance

Treat this server as a bounded capability portal, not a generic connection to the evidence store. Use the [portal manifest](portal-manifest.template.yaml) to declare ownership, transport, data classification, capabilities, schemas, authorization scopes, side effects, idempotency, human gates, audit events, timeouts, degraded behavior, and revocation.

Read, propose, approve, and execute capabilities remain separate. An MCP client or server must not pass an upstream token through to another resource. Production mutations require exact target/scope, authorized approval, attributable audit, and a safe retry/rollback rule.
