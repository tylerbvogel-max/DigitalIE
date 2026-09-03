# DigitalIE MCP contract

The MCP exposes domain verbs, never arbitrary SQL or unrestricted plant writes.

## Implemented calculation portal

The [calculator portal](calculator-portal.yaml) is implemented as a dependency-free local stdio server. Its method registry exposes typed descriptive, probability, inference, comparison, sequence, and regression calculations backed by the readable Python equations—not by model-generated expressions. It supports current stateless MCP discovery and legacy initialization for harness compatibility.

From the repository root:

```bash
PYTHONPATH=src python3 -m digital_ie.calculator_mcp
```

Or install it into an isolated environment:

```bash
python3 -m venv .venv
.venv/bin/pip install .
.venv/bin/digitalie-calculator-mcp
```

For an installed package, configure the harness command as the absolute path to `.venv/bin/digitalie-calculator-mcp`. Each MCP tool is read-only and idempotent and returns a [calculation receipt](../schemas/calculation-receipt.schema.json). Optional `context` fields attach the result to a case, analysis, evidence IDs, units, and purpose. Missing context is reported rather than invented.

The calculation identifier is content-addressed from method version and numeric inputs. Context is excluded so attaching the same arithmetic to a case does not change its identity. The caller owns storage, timestamps, actor identity, and approval events.

Material quantitative claims should use this portal or another identified validated computation tool. The agent may explain the equation and result, but must not silently replace or alter the returned value.

The server deliberately does not evaluate arbitrary expressions, access files or databases, calculate unimplemented p-values, or make acceptance/disposition decisions.

### Harness configuration shape

```json
{
  "mcpServers": {
    "digitalie-calculator": {
      "command": "python3",
      "args": ["-m", "digital_ie.calculator_mcp"],
      "env": { "PYTHONPATH": "/absolute/path/to/DigitalIE/src" }
    }
  }
}
```

Replace the path with the local clone. Harness configuration syntax may differ; the command and stdio behavior remain the same.

## Future case-management portal

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

Future case-management tool responses return stable IDs, provenance, and state transitions. That service layer will authorize every write and append an audit event.

## Portal governance

Treat this server as a bounded capability portal, not a generic connection to the evidence store. Use the [portal manifest](portal-manifest.template.yaml) to declare ownership, transport, data classification, capabilities, schemas, authorization scopes, side effects, idempotency, human gates, audit events, timeouts, degraded behavior, and revocation.

Read, propose, approve, and execute capabilities remain separate. An MCP client or server must not pass an upstream token through to another resource. Production mutations require exact target/scope, authorized approval, attributable audit, and a safe retry/rollback rule.
