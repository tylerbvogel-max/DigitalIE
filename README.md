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

- Industrial Engineering: improvement methods, statistical inference, production/flow calculations, operations research, work design, ergonomics, facilities, and material handling.
- Aerospace manufacturing: conformance/configuration, readiness, critical processes, producibility, material/process qualification, technology insertion, supplier quality, and airworthiness interfaces.
- Quality assurance: quality systems and quantitative SPC, capability, Gage R&R, yield, tolerance, sampling, and factorial methods.
- Production management: daily execution, constraints, readiness, OEE, capacity, queues, line balance, learning, and recovery.
- Program management: integrated planning, schedule networks/risk simulation, EVM, engineering economics, governance, change, and recovery.
- Materials/supply chain: demand, forecasting, inventory policy, MRP integrity/netting, shortages, supplier flow, and logistics.
- Maintenance/reliability: asset/work management, observed reliability, availability, life models, system reliability, and demonstration planning.
- Technical management: requirements, configuration, interfaces, technical risk/data, decision analysis, and test/evaluation strategy.
- Digital operations/data: decision products, metric contracts, lineage, integration, dashboards, AI support, and data governance.
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
- `schemas/`, `fixtures/`, and `evals/` — conformance contracts and synthetic verification material.
- `mcp/` and `adapters/` — the implemented calculation portal plus future case-management and source-adapter boundaries.

The local [Calculation MCP](mcp/README.md) is implemented and requires no database. Case-management persistence, source adapters, and most evaluation material remain future automation; none is required to use the human-readable corpus.
