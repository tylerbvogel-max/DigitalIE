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
