# Integration contracts

This document defines the future adapter boundary. Implemented adapters must map external data to vendor-neutral events. The planned core types include `ProductionEvent`, `QualityEvent`, `EquipmentEvent`, `WorkInstruction`, and `EvidenceItem`; core contracts must not expose ERP or MES table names.

## Read-only adapter contract

Each adapter must provide:

```text
discover_capabilities() -> source and available entities
fetch(reference, query) -> source records plus retrieval timestamp
normalize(record) -> canonical event or evidence item
provenance(record) -> system, immutable reference, retrieved_at, hash
```

The adapter never creates a quality record, changes a recipe, or edits a control plan. Those future write operations require a separately approved command contract.

## Target adoption path

1. Map an authorized CSV extract to a declared fixture schema without storing controlled data in this repository.
2. Preserve the source hash and register the import as evidence in the future case service.
3. Create a case and select a process and metric.
4. Run implemented calculation methods and generate a noncanonical report.

Only the calculation methods exist today; case persistence and CSV/MES/QMS adapters remain unimplemented. Their implementation is an adapter project, not a redesign of the evidence model.
