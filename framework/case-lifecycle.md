# Case lifecycle

An improvement case moves through controlled states. A chat or report is a view of the case, not the case itself.

| State | Entry condition | Exit condition |
|---|---|---|
| Intake | Trigger and affected outcome are recorded | Owner, process route, scope hypothesis, and immediate safety/containment need are assigned |
| Evidence gathering | Sources and observations are being assembled | Minimum evidence for analysis is present or the missing-evidence decision is escalated |
| Contained / analysis | Immediate exposure is controlled where required | Discriminating hypotheses and tests are defined |
| Decision pending | Evidence packet and alternatives are complete | Authorized decision is recorded |
| Action in progress | Approved action has owner, due date, and expected mechanism | Implementation evidence is complete |
| Effectiveness review | Measurement window and success criteria are active | Result and residual risk are decided |
| Closed | Required records, decisions, actions, and result are complete | Reopen only on recurrence, new evidence, or failed effectiveness |
| Superseded | A better-scoped case replaces this case | Replacement case and rationale are linked |
| Reopened | Recurrence, new evidence, or failed effectiveness invalidates closure | Case returns to the applicable active state with the new trigger recorded |

`Superseded` and `Reopened` preserve rather than overwrite prior history. State changes require actor, timestamp, rationale, and source references.

These are the canonical `case.status` values, serialized in lowercase kebab case. State names inside individual process-contract tables are route-specific phases; they do not replace or silently mutate the case lifecycle.
