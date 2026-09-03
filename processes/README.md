# Process plane

Use this directory when the work crosses functional boundaries. Each process calls the relevant playbooks; it does not replace them.

```text
Commitment → ready work → build → verify → release → learn
                  ↘ exception / change / recovery ↗
```

| Trigger | Process |
|---|---|
| New commitment or demand change | [Commitment to ready work](01-commitment-to-ready-work.md) |
| Product is released to manufacture | [Build to acceptance](02-build-to-acceptance.md) |
| Abnormal condition or failed requirement | [Exception to disposition](03-exception-to-disposition.md) |
| Design, process, supplier, or document change | [Change to effective control](04-change-to-effective-control.md) |
| Threatened output or commitment | [Constraint to recovery](05-constraint-to-recovery.md) |
| Asset loss or repeat downtime | [Asset loss to reliability action](06-asset-loss-to-reliability-action.md) |
| Slow, disputed, or poorly informed decision | [Decision to data product](07-decision-to-data-product.md) |
| Repeated work may benefit from AI or software automation | [Intent to verified AI capability](08-intent-to-verified-capability.md) |
| A design, transfer, process, or technology must become stable production | [Design to production capability](09-design-to-production-capability.md) |
