# Parallel agent orchestration

**Use when:** two or more bounded tasks can progress independently and concurrency is likely to reduce accepted lead time.

**Do:** define task packets, ownership, dependencies, tools/actions, acceptance evidence, stop conditions, integration owner, collision controls, and final shared verification.

**Stop when:** tasks share unresolved design decisions, files, external state, or destructive authority without isolation.

**Output:** dependency graph, work packets, ownership map, agent receipts, integrated result, and concurrency economics.
