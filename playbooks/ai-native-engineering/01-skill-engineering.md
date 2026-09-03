# Skill engineering

## Question answered

How should reusable expert behavior be packaged so an agent invokes it correctly, follows it completely, and can be evaluated independently of a particular model or chat?

## Skill contract

A skill defines trigger conditions, purpose, required context, procedure, allowed tools, authority boundaries, outputs, failure behavior, verification, and supporting resources. Keep its entry instructions compact; route to references, templates, and scripts only when needed.

## Design rules

- Use one coherent capability per skill and explicit positive/negative triggers.
- Put stable procedure in the skill; keep case evidence outside it.
- Prefer executable scripts and templates for deterministic work.
- State what must be read completely before action.
- Define stop conditions for missing evidence, authority, access, or unsafe scope.
- Version behavior changes and retain adversarial examples that motivated them.
- Test invocation precision, procedural compliance, output usefulness, and safe refusal separately.

## Failure modes

Kitchen-sink skills, vague triggers, hidden dependencies, prose copied into every prompt, instructions that conflict with authority, and skills judged only on a successful happy path.

## Output

Skill card/package, trigger examples, dependency list, evaluation fixtures, and version rationale.
