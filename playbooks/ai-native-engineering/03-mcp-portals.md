# MCP portals

## Question answered

How can an agent discover and use organizational capabilities without receiving broad system access or leaking vendor-specific semantics into the agent workflow?

## Portal contract

Treat each MCP server as a bounded capability portal. Declare owner, users, resources/prompts/tools, transport, authentication, authorization scopes, data classification, input/output schemas, side effects, idempotency, timeouts, audit events, rate limits, versioning, and shutdown/revocation path.

## Tool design

- Expose domain verbs such as `assemble_evidence_packet`, not arbitrary SQL or generic shell access.
- Separate read, propose, approve, and execute capabilities.
- Return stable identities, provenance, freshness, state transition, and errors.
- Require explicit target and scope for every mutation.
- Make destructive, irreversible, safety-relevant, or controlled-record actions human-gated.
- Bind credentials/tokens to the intended server and never pass upstream tokens through another portal.
- Design degraded behavior for unavailable systems, partial results, and revoked access.

## Output

Portal manifest, threat model, capability catalog, schemas, authorization matrix, audit contract, conformance tests, and incident/revocation procedure.
