# DigitalIE

**Digital Industrial Engineering** is a vendor-neutral, evidence-first reference architecture for continuous improvement in manufacturing. It is intentionally a clean-room model: the core represents sound problem-solving practice, while adapters translate plant-specific systems into that core.

## What it protects

DigitalIE separates an observation, a hypothesis, a validated causal claim, a corrective action, and an effectiveness result. A language model may facilitate each stage; it may not silently turn an assumption into a root cause.

## The first demonstration

The included `assembly-torque-failure` fixture follows a final-assembly torque issue from containment through Gemba observations, competing hypotheses, a test, and an effectiveness check. Run it with:

```bash
python -m unittest discover -s tests -v
```

## Repository map

- `docs/` — architecture, ontology, integration contracts, and decisions.
- `schemas/` — canonical JSON Schemas for portable interchange.
- `profiles/` and `skills/` — harness-agnostic agent behavior and methods.
- `mcp/` — tool contract; its verbs enforce the evidence model.
- `adapters/` — source-to-canonical translations, starting with CSV.
- `fixtures/` and `evals/` — reproducible cases and behavioral checks.

## Boundary

This repository is not an MES, QMS, historian, or autonomous process-control system. Early integrations are read-only. Any plant-system write requires an identified human approver and an audit event.
