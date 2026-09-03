# Agent threat model

## System and assets

| Field | Record |
|---|---|
| Users and affected parties | |
| Protected data, systems, decisions, credentials, and operations | |
| Deployment zone and environment | |
| Model/provider and data boundary | |

## Trust and capability map

| Source/tool | Trust class | Read reach | Write/side effect | Credential | Human gate | Audit |
|---|---|---|---|---|---|---|

## Abuse cases

Evaluate prompt injection, data exfiltration, confused deputy, privilege escalation, tool/schema manipulation, token misuse, malicious repository/dependency, unsafe generated code, denial/cost exhaustion, memory poisoning, approval spoofing, and destructive-target ambiguity.

## Controls and residual risk

| Threat | Prevent | Detect | Contain/revoke | Recover/rollback | Owner | Residual decision |
|---|---|---|---|---|---|---|
