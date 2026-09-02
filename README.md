# DigitalIE

**Digital Industrial Engineering** is Tyler’s private, vendor-neutral operating corpus for learning and improving manufacturing systems. It is intentionally clean-room: the reference model is built before exposure to a new organization’s habits, tooling, or technical debt.

Its job is to make the first useful question available quickly: *what kind of operational problem is this, what evidence would distinguish the plausible explanations, and what improvement lever is proportionate?* It is not a product, a prescribed plant system, or a claim that every local variation is wrong.

## What it protects

DigitalIE separates an observation, a hypothesis, a validated causal claim, a corrective action, and an effectiveness result. A language model may facilitate each stage; it may not silently turn an assumption into a root cause.

## How to use it in a new environment

1. Start with [the intake and challenge protocol](learning/intake-and-challenge-protocol.md), not a proposed fix.
2. Select a fit-for-purpose method from [the Industrial Engineering playbooks](playbooks/industrial-engineering/README.md).
3. Record observed practice separately from the reference model in [the gap ledger template](templates/reference-vs-reality.md).
4. Treat a local deviation as a hypothesis with an owner, rationale, and measure—not as automatic debt or automatic wisdom.

## Current corpus

- Industrial Engineering: triage, Gemba, 5 Why, Ishikawa, Pareto/stratification, SPC, value-stream mapping, and DMAIC/PDCA.
- Aerospace manufacturing: quality/conformance, configuration/traceability, readiness, critical-process governance, production control, supplier quality, airworthiness interfaces, change control, and operations data/AI.
- Shared tools: problem framing, evidence standards, experiment design, and reference-versus-reality questioning.
- Future domains: program management, quality assurance, and production management follow the same shape once this foundation is mature.

## Optional future automation

The included `assembly-torque-failure` fixture follows a final-assembly torque issue from containment through Gemba observations, competing hypotheses, a test, and an effectiveness check. Run it with:

```bash
python -m unittest discover -s tests -v
```

## Repository map

- `playbooks/` — the primary, human-usable operational corpus.
- `learning/` — how to learn a new operating system without inheriting it uncritically.
- `templates/` — reusable field guides and gap records.
- `docs/` — supporting architecture, ontology, integration contracts, and decisions.
- `profiles/` and `skills/` — concise harness-agnostic agent behavior cards.
- `schemas/`, `mcp/`, `adapters/`, `fixtures/`, `evals/` — optional future automation foundation.

## Boundary

This repository is not an MES, QMS, historian, or autonomous process-control system. Any later integrations begin read-only. Any plant-system write requires an identified human approver and an audit event.
