# Handoff — agent-state data hygiene

Feature round 1, session 1. Branch `feature/agent-data-hygiene`, based on `a6f9ba80a`.
No commit or PR yet. `.agent/STOP`, runtime data, provider settings, other worktrees and Git history
were not changed.

## State
Review packages now exclude development-only `.agent` bytes at both discovery and ArchivePlan
policy layers. A staged-diff guard refuses new credentials, machine-local paths, provider-session
links, private-network addresses and binary attachments under `.agent`; historical records are not
rewritten.

## Changed files
| Area | Files | Change |
|---|---|---|
| Package boundary | ZIP shell, manifest and ArchivePlan policy | exclude all `.agent` members, including changed ReviewSubject files |
| Prevention | `scripts/check_agent_hygiene.py`, `.githooks/pre-commit` | fail closed on sensitive staged additions |
| Tests | `tests/test_agent_state_hygiene.py`, two ArchivePlan policy tests | red/green package and guard coverage |
| Docs/state | two system pages and current plan/context/handoff | document boundary and task state |

## Verification
- Focused package/policy suite: 48 passed, 1 skipped.
- ZIP hygiene/full integration suite: 48 passed; manifest privacy suite: 10 passed.
- Ruff: passed for changed Python files.
- Mypy: passed for both changed source modules.
- Shell syntax and `git diff --check`: passed.
- Fast lane first run: 1,518 passed, 1 skipped, 5 state/source-discovery failures; all five causes
  corrected. Final fast lane: 1,523 passed, 1 skipped.
- Full pytest: not run.

Open findings: 84 by `open_finding_ids`; none is newly claimed or resolved by this task.

## Deviations
- No history rewrite: already committed sensitive metadata remains in Git history.
- Required append-only workflow records were not destructively sanitized. Package exclusion prevents
  their distribution; the staged guard is forward-looking.
- No review ZIP artifact was retained; integration tests built packages only in temporary repositories.

## Next
Review the staged diff, commit, push, create the PR, and record final commit evidence. The operator
may separately authorize a coordinated history rewrite if removal from old Git objects is required.
