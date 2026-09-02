# ADR 0001: Canonical evidence store is relational

**Status:** Accepted

## Decision

Use PostgreSQL as the production canonical store. Use JSON Schema for interchange and fixture validation. Markdown and PDFs are generated views.

## Rationale

Improvement work requires relationships, provenance, concurrency, immutable audit events, permissions, and reliable queries across cases. JSONB may hold method-specific details, but stable cross-case concepts are relational.

## Consequence

The local fixture/test harness remains dependency-free. A future persistence implementation maps this model to PostgreSQL rather than treating files as authoritative.
