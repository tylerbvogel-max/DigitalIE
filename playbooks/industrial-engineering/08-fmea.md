# FMEA: anticipate and prioritize process risk

## Question answered

What can fail, what happens if it does, what currently prevents or detects it, and which risks deserve action before the failure reaches a customer or downstream operation?

## When to use it

Use a process FMEA before a launch, transfer, significant change, recurring risk review, or when a root-cause case exposes a failure mode not previously controlled. It is prospective; use 5 Why/DMAIC to investigate an event that already happened.

## Build the chain

For each process step, identify the intended function/requirement, failure mode, effect, cause/mechanism, prevention control, detection control, and current evidence. Keep these distinct: an inspection is usually a detection control, not prevention.

| Step / function | Failure mode | Effect | Cause / mechanism | Prevention control | Detection control | Action |
|---|---|---|---|---|---|---|

## Risk prioritization

Score severity, occurrence, and detection only with team-defined, stable criteria. Severity belongs to the effect, not the likelihood. A high-severity item remains important even when rare. Use an action-priority rule or explicit risk matrix rather than pretending that identical RPN products represent identical risk.

If a local method requires the traditional risk priority number:

\[
RPN=Severity\times Occurrence\times Detection
\]

Example: \(10\times2\times2=40\) and \(4\times5\times2=40\). The identical product conceals materially different severity and occurrence patterns. Preserve the three ratings, rationale, and high-severity escalation; never use RPN alone as an interval-scale risk measure or automatic acceptance threshold.

Escalate safety, regulatory, customer-critical, and uncontrolled-escape risks. Actions must change prevention, detection, or consequence; reminders and retraining alone are insufficient.

## Exit

Each priority risk has an owner, due date, proposed control change, verification plan, and a linked control-plan update. Re-rate only after the action is actually implemented and verified.
