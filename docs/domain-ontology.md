# Domain ontology

## Epistemic ladder

`source evidence → observation → hypothesis → validation test → verified cause → corrective action → effectiveness review`

These are separate entities. A claim may be rejected; rejected claims remain part of the historical record.

| Entity | Meaning | Example |
|---|---|---|
| Evidence item | Retrieved or recorded source material | MES export, calibration record, photo |
| Observation | What a person or instrument observed | Tool displayed a low-battery warning |
| Hypothesis | Testable explanatory claim | Battery voltage causes torque variance |
| Validation test | Predicted discriminating test | Compare defects before/after verified battery swap |
| Verified cause | Approved conclusion supported by tests | Voltage drop caused false torque completion |
| Action | Owned change intended to address a cause | Add pre-shift battery verification |
| Effectiveness review | Measured post-change result | 30 days with no recurrence at target volume |

## Invariants

- `hypothesis.status = verified` represents a verified cause and requires linked evidence, a validation result, and human approval.
- An observation may cite a source but may not be promoted automatically.
- An analysis records inputs, filters, method, parameters, and output version.
- A control limit and a specification limit are distinct concepts.
- Source records are append-only; corrections create a superseding record.
