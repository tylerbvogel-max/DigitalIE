# Calculation pack standard

## Purpose

A calculation pack moves repeatable arithmetic out of nondeterministic agent reasoning while preserving the professional judgment needed to choose and interpret a method. It is a protocol-neutral domain module registered through the read-only Calculation MCP.

## Admission contract

Every operation must declare:

- stable method ID and tool name;
- manufacturing question and intended decision support;
- typed closed input schema with units, scope, time/configuration boundary, and required evidence context where material;
- named equations or algorithm and public primary orientation source;
- method version and deterministic implementation;
- intermediates needed to audit the result;
- mechanically validated conditions;
- undefined results and rejected domains;
- assumptions not established by the arithmetic;
- explicit human-authority boundary;
- golden, boundary, rejection, identity/invariant, and MCP round-trip tests.

## Numeric behavior

Reject booleans as numbers, nonfinite values, impossible counts, inconsistent array dimensions, invalid probabilities, and zero/negative denominators where the method does not define them. Return `null` only for a deliberately supported undefined metric and name it in `undefined_metrics`; otherwise reject the request. Do not silently clamp, impute, coerce units, round intermediate results, or replace missing values with zero.

Report full machine results in the receipt. Presentation layers may round a copy but must preserve the receipt. State percentage convention and sign convention. Require common units or an explicit conversion operation; never infer currency or time conversions.

## Algorithms and randomness

Prefer transparent closed-form equations. Iterative solvers must expose tolerance, iteration bound, convergence status, and residual or feasibility evidence. Optimization accepts typed variables, coefficients, constraints, and objectives—never arbitrary expressions or executable code.

Simulation requires an explicit pseudo-random algorithm, caller-supplied seed, trial count, distribution parameters, and method version. Identical inputs must reproduce the same receipt. Simulation output is conditional on the declared model and does not establish distribution fitness.

## Verification

At least one golden result must be independently cross-checked against a trusted implementation, authoritative worked example, or separately derived exact value. Tests must also exercise dimensional/shape errors, denominator boundaries, out-of-domain values, and an identity such as reconciliation, probability sum, constraint feasibility, or component-to-total equality.

The MCP round trip must be observed before release. Documentation examples should be pinned in tests where practical so prose cannot drift from the kernel.

## Security and authority

Calculation tools are read-only, idempotent, local-input-only, and deny arbitrary evaluation, filesystem access, database access, network access, credentials, and plant writes. A calculation may quantify evidence; it cannot accept product, disposition a nonconformance, alter a baseline, declare compliance, approve a process, set a safety limit, or make a controlled engineering/program decision.

## Change control

A formula, sign convention, algorithm, default, or validation change requires a method-version decision, regression fixtures for the former behavior, updated documentation, and an explicit compatibility assessment. Adding an independent operation does not require changing existing method versions.
