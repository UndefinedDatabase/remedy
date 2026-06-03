# Project Brain

Project Brain gives you a summary across all jobs in a project. Instead of looking at one job at a time, you can see the big picture.

## What It Shows

- **Job counts**: total, active, completed, blocked
- **Current focus**: what needs attention now
- **Blockers**: which jobs are stuck and why
- **Repeated patterns**: problems that keep coming back
- **Frequently touched files**: files that get modified across many jobs
- **Model quality confidence**: whether model checks used real data or only examples
- **Next step**: what Remedy suggests doing next

## What It Does Not Do

- It does not read raw source code into summaries.
- It does not auto-write project memory. Memory suggestions require your approval.
- Model confidence stays "low" unless you run real model checks.
- Patterns are only flagged when they occur two or more times. A single failure is not a pattern.
- The dashboard is read-only. No buttons write to your repo.

## Commands

```sh
# Text summary
remedy project summary <project_id>

# JSON output
remedy project summary <project_id> --json

# Related commands
remedy project show <project_id>
remedy project brain <project_id>
remedy project context <project_id>
remedy project list
```

## Repeated Patterns

Remedy detects these recurring patterns:

| Pattern | Triggers when |
|---------|---------------|
| Repeated stop reason | Same reason stops two or more jobs |
| Frequently touched file | Same file modified in two or more jobs |
| Repeated parse failure | Model produces unparseable output repeatedly |
| Repeated test failure | Tests fail after patch apply in two or more jobs |
| Repeated permission block | Permission denied across multiple jobs |
| Repeated provider unavailable | Local model unreachable across jobs |
| Repeated repair exhaustion | Repair loop budget runs out repeatedly |

## Memory Suggestions

When patterns are strong enough (count >= 2-3), Remedy suggests project memory updates. These are suggestions only:

- Each suggestion has a title, summary, and evidence count.
- Every suggestion requires approval before writing.
- Remedy does not silently change project memory.

## Model Quality Confidence

- **low**: only example-based data exists, or no model checks have run.
- **medium**: real local model data exists with 5+ samples.
- **high**: real data with 15+ samples.

If confidence is low, the summary says "needs real model check." Run a real model check with:

```sh
REMEDY_REAL_OLLAMA_EVAL=1 scripts/remedy_builder_eval.sh --ollama
```

## Dashboard

The dashboard shows a compact project summary card in the right panel:

- Job counts, active/blocked
- Top blocker
- Pattern count
- Model confidence
- Suggested next step with copyable command

If no project is linked to the current job, the card is hidden.
