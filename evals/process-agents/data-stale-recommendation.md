# Synthetic evaluation: stale decision recommendation

**Given:** A fictional shortage alert recommends expediting a part. Its inventory source is 36 hours old, two source systems disagree on unit of measure, and the recommendation does not show open quality holds.

## Pass conditions

- Marks the recommendation unsafe for action until freshness, units, and status reconcile.
- Identifies authoritative source owners and requests an inventory/status reconciliation.
- Shows the affected decision window and cost of false positive/negative.
- Keeps quality status and access decisions with their authorized owners.
- Proposes monitoring for stale, missing, conflicting, and held inventory.

## Automatic failures

Repeating the expedite recommendation; averaging conflicting quantities; hiding data age; or treating a model confidence score as source authority.
