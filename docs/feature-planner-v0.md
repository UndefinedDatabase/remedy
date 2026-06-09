# Feature Planner v0

Deterministic next-work suggestions. No LLM. Rules-based only.

## Generate suggestions

```bash
remedy feature plan --agent [--json]
remedy feature plan <job_id> [--json]
```

## Accept a suggestion

```bash
remedy feature accept <job_id> <suggestion_id> [--json]
```

Accept creates ProposedTask metadata. It does NOT execute anything.

## How suggestions work

The planner reads the progress ledger and applies deterministic rules:

| Rule | Priority | Source |
|---|---|---|
| Open blocker/high findings | High | Review findings |
| Known pre-existing failing tests | High | Known risks |
| Proof gaps | Medium | Proof chain |
| Stale handoff (inconsistencies) | High | Ledger state |
| No issues → roadmap items | Medium/Low | Hardcoded roadmap |

## Roadmap suggestions (when everything is clean)

1. File Provenance v1 expansion
2. Run Contract Enforcement v1
3. Real Test Execution v1
4. Operator Cockpit read-only v0.2

## What accept does

- Creates metadata dict linking suggestion to job
- Sets `creates_proposed_task: true`
- Sets `executed: false`, `applied: false`
- Records planner version and source refs
- Does NOT create real tasks, execute code, or apply changes

## User-controlled workflow

1. Run `remedy feature plan --agent --json` to see suggestions
2. Select a suggestion ID
3. Run `remedy feature accept <job_id> <suggestion_id>` to accept
4. The accepted suggestion becomes a ProposedTask for future work

## Safety

- Suggestions are read-only until explicitly accepted
- Accept creates metadata, not execution
- No raw content in suggestions
- No LLM hallucination — all rules are deterministic
- Suggestion IDs are stable hashes
