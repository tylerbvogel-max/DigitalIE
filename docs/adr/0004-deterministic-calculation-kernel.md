# ADR 0004: Deterministic calculation kernel behind a thin MCP adapter

## Status

Accepted.

## Context

DigitalIE agents must reason about operational questions but language models are not reliable arithmetic engines. Statistical and manufacturing equations are deterministic, must be reproducible, and may support consequential recommendations. Putting formulas only in prompts leaves calculation execution and transcription exposed to model error. Putting the formulas only inside an MCP server would make the protocol adapter the mathematical source of truth and hinder direct testing or reuse.

## Decision

Maintain equations as readable, tested Python functions in the protocol-neutral calculation kernel. Register bounded, versioned domain methods that return content-addressed calculation receipts. Expose those same methods through a dependency-free, read-only MCP stdio adapter.

The model selects a candidate method, supplies declared inputs, and interprets the receipt. The kernel validates mechanical input constraints and performs arithmetic. It does not validate evidence provenance, study design, assumptions that require domain judgment, causality, specification conformance, or decision authority.

The MCP exposes named calculations rather than arbitrary expressions, Python execution, SQL, file access, network access, or plant-system writes. A material result belongs with the improvement case and its immutable evidence references; the conversation is not its durable record.

## Consequences

- Equations remain inspectable by a person and executable without MCP.
- Codex, Claude Code, and other MCP clients can invoke identical operations.
- Every result identifies method version, formula, inputs, intermediates, outputs, unresolved assumptions, and authority boundary.
- Identical method versions and numeric inputs produce the same content-addressed calculation identifier.
- Adding a method requires a readable implementation, contract, worked example or fixture, boundary tests, and an independent reference check.
- Statistical distribution tails and p-values that require qualified numerical libraries are not approximated casually; they remain absent until implemented and cross-validated.
