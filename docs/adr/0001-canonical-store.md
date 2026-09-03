# ADR 0001: Canonical evidence store is relational

**Status:** Accepted

## Decision

Use PostgreSQL as the future production canonical store for improvement cases, evidence, decisions, and audit events. Use JSON Schema for interchange and fixture validation. Case reports in Markdown or PDF are generated views. The clean-room guidance corpus remains Markdown-canonical until a separate corpus-storage decision supersedes it.

## Rationale

Improvement work requires relationships, provenance, concurrency, immutable audit events, permissions, and reliable queries across cases. JSONB may hold method-specific details, but stable cross-case concepts are relational.

## Consequence

The local fixture/test harness remains dependency-free. A future case-persistence implementation maps domain records to PostgreSQL rather than treating fixture files or generated case reports as authoritative.
