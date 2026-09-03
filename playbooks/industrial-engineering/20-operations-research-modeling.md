# Operations-research modeling

## Question answered

What allocation, sequence, routing, inventory, or capacity decision best serves a declared objective while respecting the real constraints?

## Model contract

Name the decision owner, decision deadline, controllable variables, objective and units, hard constraints, policy constraints, time horizon, uncertainty, source evidence, and feasible fallback. Separate a physical constraint from a current policy and from a guessed limit.

Build the smallest model that can change the decision. Use dimensional checks and a manually solvable fixture before real data. Verify that every returned solution satisfies the encoded constraints, compare it with a current-practice baseline, vary uncertain inputs, and have process owners challenge missing constraints.

An optimum is conditional on the model. It does not prove that the objective represents customer value, that omitted constraints are harmless, or that the solution can be executed. A solver status of feasible is not an operational approval.

## Method routing

| Problem shape | Candidate method | Required challenge |
|---|---|---|
| finite resources assigned to competing work | linear/integer programming | integrality, setup, qualification, and precedence |
| work assigned one-to-one | assignment model | compatibility and transition cost |
| material moved through a network | transportation/network flow | lane, lot, time, and handling feasibility |
| congestion under stochastic arrivals/service | queueing or discrete-event simulation | stationarity, distribution, priority, blocking, rework |
| competing sequences | dispatch-rule comparison | due dates, setups, material, and downstream effects |
| facility alternative | weighted-factor or flow-distance analysis | weights, hazards, expansion, and qualitative constraints |

## Stop conditions

Stop when the objective hides a safety, quality, workforce, customer, or regulatory trade; a constraint lacks an owner or source; the model recommends violating configuration or qualification; or validation fails on a known case.

## Output

Decision statement, typed model, evidence-linked parameters, dimensional check, solver/method version, feasibility result, baseline comparison, sensitivity and scenario results, omitted effects, recommendation, dissent, and human decision.

Public orientation: [NCEES PE Industrial and Systems specification](https://ncees.org/wp-content/uploads/PE-Ind-Oct-2020_with-codes-and-standards.pdf) and [Purdue MS Industrial Engineering](https://engineering.purdue.edu/IE/academics/graduate/degree_programs/online).
