# Next items: governed corpus kernel

> Status, 2026-09-03: the initial governed kernel, source/observation intake, canonical vocabulary, case lifecycle, technical-management family, process contracts, operating cadence, agent fixtures, and baseline corpus fitness checks are implemented. Remaining work is refinement and controlled metadata rollout, not another unbounded content expansion.

The capability library, process plane, agent cards, and authority matrix are established. The next work is not another functional domain. It is the lightweight governance that lets DigitalIE absorb real experience without turning a local workaround into universal guidance.

## Objective

Make DigitalIE safe to extend over years while it remains Markdown-first and private. A captured observation may be easy to add; a change to baseline guidance must remain attributable, scoped, reviewable, and reversible.

## Sequence

### 1. Information boundary

Create `framework/information-boundary.md` before capturing workplace observations.

- Permit only public references, generic patterns, and sanitized lessons in this repository.
- Exclude controlled, proprietary, customer, export-controlled, personally identifiable, and identifiable production data.
- Keep employer records, source documents, screenshots, system exports, and actual case files in employer-approved systems.
- Add a redaction checklist and a stop/escalate rule for uncertain information.

**Acceptance:** a future user can decide whether a proposed note belongs here before committing it.

### 2. Content classes, scope, and source register

Create `framework/content-classes.md`, `framework/scope-and-authority.md`, and `references/README.md`.

| Class | Purpose | Promotion rule |
|---|---|---|
| Reference | External source-backed fact or method | Never becomes local policy by itself |
| Baseline | DigitalIE clean-room model | Revised by explicit corpus decision |
| Local observation | Sanitized description of an observed practice | Cannot change baseline directly |
| Adopted practice | Local method with evidence, owner, scope, and review date | Requires explicit promotion record |

Every reference entry needs canonical ID, source/version, URL or local citation, applicable scope, status, last-reviewed date, and supersession link.

**Acceptance:** any claim can be classified, scoped, sourced, and retired without deleting its history.

### 3. Local learning loop

Create `local-observations/README.md`, `candidates/README.md`, and `templates/local-observation.md`.

```text
Observation → candidate → review → adopted practice or rejected/superseded
```

The candidate record captures observed practice, reference expectation, local rationale, sanitized evidence, consequence, scope, owner, and review date. It must state whether the difference is a necessary adaptation, deliberate tradeoff, workaround, historical scar, or likely defect.

**Acceptance:** an observation is searchable and useful without being mistaken for approved practice.

### 4. Canonical process-case vocabulary

Create `framework/canonical-vocabulary.md` and `framework/case-lifecycle.md`.

Use stable meanings for: `Commitment`, `Work Item`, `Product/Configuration`, `Evidence`, `Exception`, `Change`, `Asset`, `Decision`, `Action`, and `Outcome`.

Define a lightweight case lifecycle: `intake → evidence gathering → contained/analysis → decision pending → action in progress → effectiveness review → closed`, with `superseded` and `reopened` available at any appropriate point.

**Acceptance:** every process agent and template uses the same terms and can hand a case to another process without semantic loss.

### 5. Contribution and supersession lifecycle

Create `framework/contribution-lifecycle.md`, `templates/new-playbook.md`, `templates/new-process.md`, and `templates/new-agent-card.md`.

Require purpose, trigger, scope, source/evidence class, owners/authority boundary, related content, review cadence, and change rationale. Prefer an amendment or supersession record over silent rewrite when the guidance changes materially.

**Acceptance:** a contributor can place new knowledge correctly and reviewers can identify why it changed.

### 6. Corpus health

Create `framework/corpus-health.md`; later add a dependency-free `scripts/corpus_health.py` only when manual checks become friction.

Checks should include broken internal links, orphaned index entries, duplicate titles, required metadata, stale source reviews, missing authority gates on agent cards, missing outputs/handoffs on process maps, and references to superseded material.

**Acceptance:** health checks identify specific repair work; they do not score prose for vanity.

### 7. Agent evaluation and process fixtures

Create `evals/process-agents/` with synthetic, non-proprietary cases for every process agent.

Required failure cases: missing configuration, ambiguous authority, incomplete source evidence, quality escape with uncertain scope, unsafe expedite, stale metric, data-access request, and conflicting functional recommendations.

An agent passes when it preserves evidence, identifies the right process, invokes the right critics, and stops at the decision gate. It does not pass by producing a polished answer.

**Acceptance:** each agent card has at least one normal case, one missing-data case, and one authority-boundary case.

### 8. Navigation and usage rhythm

Create `framework/start-here.md` as the first router: commitment, ready-work, build/acceptance, exception, change, recovery, asset loss, or decision-data problem. Add a monthly corpus review: new observations, candidate promotions, source review dates, stale content, duplicate concepts, and agent evaluation failures.

**Acceptance:** the corpus can be used during an operational event in under two minutes, and reviewed without rereading the repository.

## Explicit non-goals

- No Corvus graph, embeddings, database, hooks, or automatic promotion.
- No employer operational data in this private repository.
- No automatic authority elevation from an AI summary or a single observed case.
- No new playbook family until recurring use exposes a real coverage gap.

## First implementation slice

Items 1–3 are complete. Vocabulary/case lifecycle and initial evaluation fixtures are also complete. Next:

1. Roll required front matter across governed content in small reviewed batches and make schema validation a CI gate only after the corpus is conformant.
2. Add at least four adversarial fixtures for every process agent, including critic conflict and authority-pressure cases.
3. Generate a metadata-driven catalog and coverage view; keep Markdown canonical.
4. Exercise the process contracts against synthetic end-to-end cases and tighten ambiguous handoffs.
5. Defer runtime agents, PostgreSQL, embeddings, and write-capable integrations until a real case workload justifies them.

## AI-native maturation backlog

The AI-native family is scaffolded. Mature it through observed use rather than technology catalog growth:

1. Build at least one synthetic end-to-end fixture for skill invocation, context compaction, MCP authorization failure, parallel-agent collision, review escape, and runtime rollback.
2. Add a machine-validated MCP portal manifest schema and conformance probe when the first real portal is implemented.
3. Create a golden agent-ready repository only after two or more codebases demonstrate the same setup, architecture, evaluation, and delivery pattern.
4. Define risk tiers and minimum release evidence from actual workflow consequences; do not guess universal autonomy levels.
5. Keep model/provider-specific guidance in adapters or references while the core contracts remain vendor-neutral.
