# DigitalIE

DigitalIE is a private, vendor-neutral field reference for learning and improving manufacturing operations. It supplies a clean reference model before local procedures, systems, and habits shape the diagnosis.

It keeps observation, hypothesis, validated cause, corrective action, and effectiveness result separate.

## How to use it in a new environment

1. Start with [the intake and challenge protocol](learning/intake-and-challenge-protocol.md), not a proposed fix.
2. Select a fit-for-purpose method from [the Industrial Engineering playbooks](playbooks/industrial-engineering/README.md).
3. Record observed practice separately from the reference model in [the gap ledger template](templates/reference-vs-reality.md).
4. Record each local deviation with its rationale, owner, and measured consequence.

## Process and agent views

The playbooks are the capability library. [Processes](processes/README.md) organize that library around work moving through the operation. [Agent cards](agents/README.md) define the evidence, allowed actions, specialist critics, and human decision gates for future agentic use.

## Current corpus

- Industrial Engineering: triage, Gemba, 5 Why, Ishikawa, Pareto/stratification, SPC, value-stream mapping, and DMAIC/PDCA.
- Aerospace manufacturing: quality/conformance, configuration/traceability, readiness, critical-process governance, production control, supplier quality, airworthiness interfaces, change control, and operations data/AI.
- Quality assurance: quality-system design, acceptance evidence, nonconformance, CAPA/8D, audit, document/record control, supplier quality, and quality metrics.
- Production management: daily management, schedule execution, constraint control, material/labor readiness, shift handoffs, visual performance, and recovery leadership.
- Program management, materials/supply chain, maintenance/reliability, and digital operations/data.
- Shared tools: problem framing, evidence standards, experiment design, and reference-versus-reality questioning.

## Repository map

- `playbooks/` — the primary, human-usable operational corpus.
- `processes/` — cross-functional work flows and handoff contracts.
- `agents/` — process-agent boundaries and orchestration patterns.
- `authority/` — human decision rights that agents cannot assume.
- `learning/` — first-contact and discovery patterns.
- `templates/` — reusable field guides and gap records.
- `docs/` — supporting architecture, ontology, integration contracts, and decisions.
- `profiles/` and `skills/` — concise harness-agnostic agent behavior cards.
- `schemas/`, `mcp/`, `adapters/`, `fixtures/`, `evals/` — optional future automation foundation.

The database, MCP, adapter, fixture, and evaluation directories are future-automation reference material. They are not required to use the corpus.
