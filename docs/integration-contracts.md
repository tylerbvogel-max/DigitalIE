# Integration contracts

Adapters map external data to vendor-neutral events. The core speaks in `ProductionEvent`, `QualityEvent`, `EquipmentEvent`, `WorkInstruction`, and `EvidenceItem`; it does not speak in ERP or MES table names.

## Read-only adapter contract

Each adapter must provide:

```text
discover_capabilities() -> source and available entities
fetch(reference, query) -> source records plus retrieval timestamp
normalize(record) -> canonical event or evidence item
provenance(record) -> system, immutable reference, retrieved_at, hash
```

The adapter never creates a quality record, changes a recipe, or edits a control plan. Those future write operations require a separately approved command contract.

## Five-minute adoption path

1. Map a CSV extract to the canonical fixture columns.
2. Attach the import as an evidence item.
3. Create a case and select a process and metric.
4. Run the existing methods and reporting workflow.

Deeper MES/QMS integration is an adapter project, not a redesign of the evidence model.
