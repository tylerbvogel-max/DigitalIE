# DigitalIE

DigitalIE is a private, vendor-neutral field reference for learning and improving manufacturing operations. It supplies a clean reference model before local procedures, systems, and habits shape the diagnosis.

It keeps observation, hypothesis, validated cause, corrective action, and effectiveness result separate.

## How to use it in a new environment

1. Start with [the process router](framework/start-here.md) and name the decision or abnormal condition.
2. Use [the intake and challenge protocol](learning/intake-and-challenge-protocol.md), not a proposed fix.
3. Select a fit-for-purpose method from the capability playbooks.
4. Keep real records in employer-approved systems and apply [the information boundary](framework/information-boundary.md).
5. Record sanitized observed practice separately from the reference model using [the gap ledger](templates/reference-vs-reality.md) or [local-observation template](templates/local-observation.md).
6. Define the baseline, intervention mechanism, authority, and effectiveness measure before calling an improvement successful.

Read [the operating thesis](docs/operating-thesis.md) for the outcomes DigitalIE is intended to improve and the authority it does not assume.

For internal AI-enabled application development, use the [AI-native manufacturing program north star](docs/ai-native-program-north-star.md) to guide platform, governance, and adoption decisions.

## Process and agent views

The playbooks are the capability library. [Processes](processes/README.md) organize that library around work moving through the operation. [Agent cards](agents/README.md) define the evidence, allowed actions, specialist critics, and human decision gates for future agentic use.

## Current corpus

- Industrial Engineering: triage, Gemba, causal methods, Pareto, SPC, flow/capacity, MSA, FMEA/control, descriptive statistics, probability, inference, comparisons, ANOVA, correlation, and regression.
- Aerospace manufacturing: quality/conformance, configuration/traceability, readiness, critical-process governance, production control, supplier quality, airworthiness interfaces, change control, and operations data/AI.
- Quality assurance: quality-system design, acceptance evidence, nonconformance, CAPA/8D, audit, document/record control, supplier quality, and quality metrics.
- Production management: daily management, schedule execution, constraint control, material/labor readiness, shift handoffs, visual performance, and recovery leadership.
- Program management, materials/supply chain, maintenance/reliability, and digital operations/data.
- Technical management: requirements/verification, configuration, interfaces, technical risk, technical data, and formal decision analysis.
- AI-native engineering: skills, context engineering, MCP portals, agent-ready repositories, agentic review/security, parallel orchestration, software factories, and evaluation.
- Shared tools: problem framing, evidence standards, experiment design, and reference-versus-reality questioning.

## Repository map

- `playbooks/` — the primary, human-usable operational corpus.
- `processes/` — cross-functional work flows and handoff contracts.
- `agents/` — process-agent boundaries and orchestration patterns.
- `authority/` — human decision rights that agents cannot assume.
- `learning/` — first-contact and discovery patterns.
- `framework/` — information boundary, content authority, vocabulary, case lifecycle, contribution control, and corpus health.
- `operating-system/` — daily management, cross-functional reviews, and benefits realization.
- `local-observations/`, `candidates/`, and `references/` — governed learning intake and source register.
- `templates/` — reusable field guides and gap records.
- `docs/` — supporting architecture, ontology, integration contracts, and decisions.
- `profiles/` and `skills/` — concise harness-agnostic agent behavior cards.
- `schemas/`, `mcp/`, `adapters/`, `fixtures/`, `evals/` — optional future automation foundation.

The database, MCP, adapter, fixture, and evaluation directories are future-automation reference material. They are not required to use the corpus.
