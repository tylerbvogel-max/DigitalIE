# Digital thread model

The improvement-case ontology explains how knowledge becomes a verified cause and effective action. This model explains which operational objects the evidence concerns.

```text
Commitment
  → Requirement
    → Product / configuration item / effectivity
      → Process plan / work instruction / operation
        → Material, serial, lot, tool, asset, person qualification
          → Inspection characteristic / test / acceptance evidence
            → Exception / disposition / change
              → Delivered and maintained configuration
```

## Identity contract

Every operational object needs:

- stable vendor-neutral type and identity;
- authoritative source and source identity;
- revision/status/effectivity when applicable;
- lifecycle owner and decision authority;
- valid-time and record-time where history matters;
- upstream/downstream relationships with relationship meaning;
- provenance and confidence for derived relationships; and
- retention, access, and supersession rules.

## Required traversals

The implementation should eventually answer:

- Which requirements and approved definition governed this serial/lot at this operation?
- What material, tooling, software, personnel qualification, process, and inspection evidence contributed to it?
- Which WIP, stock, supplier orders, instructions, tests, and delivered products are affected by this proposed or discovered change?
- What authoritative decision created the current status?
- Can a suspect source lot, process run, tool state, software revision, or evidence defect be traced forward to exposed product?

## Data authority

DigitalIE does not become the master of product data. Adapters preserve authoritative source identifiers and retrieval provenance. Conflicting sources produce a reconciliation case; the integration layer must not select a winner silently.
