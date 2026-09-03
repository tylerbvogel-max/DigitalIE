# Production flow calculations

**Use when:** a case needs reproducible takt, capacity, line-balance, OEE, Little's Law, PCE, RTY, queue, or repeat-unit learning arithmetic.

**Do:** declare product family, process boundary, observation horizon, common units, demand and time exclusions, count/yield definitions, data provenance, and model assumptions; call the deterministic calculation; preserve its receipt; compare scenarios; then use Gemba and loss evidence to interpret the result.

**Stop when:** demand or the process boundary is disputed; time bases differ; an OEE factor exceeds its physical bounds; flow is not stable; arrivals/service do not plausibly match the selected queue; the learning-curve convention is unspecified; or a calculated resource count is being treated as an approved staffing plan.

**Output:** scope and units, inputs and provenance, named model, assumption verdict, calculation receipt, sensitivities, observed losses, operational implications, owner, and human authority. See [the production-flow playbook](../playbooks/industrial-engineering/23-production-flow-calculations.md).
