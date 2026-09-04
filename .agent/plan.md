# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
integration gate PASSED round 19, self-use consumed round 21, Built
State landed round 22, evidence job succeeded round 23 but the review
zip BLOCKED on a real pre-existing bug (R-0790: `ABS_PATH_RE` false-
positives on `/-` inside `+/-`). Round 24 fixes R-0790, then re-runs the
evidence job and zip against the new head.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 24 books RECORD23 (registers R-0790), fixes
`packages/common/path_redaction.py`'s `ABS_PATH_RE` POSIX branch with a
positive lookahead (dry-run confirmed against the full existing test
surface), adds a pinning test case, mutation red-proofs it in a
disposable worktree, re-runs the full relevant test surface, then
re-runs the evidence job and the review zip to confirm it now succeeds.

## Next Steps

- Once the zip succeeds: reviewer authors the STATUS line from the new
  job_id/package/hash/path/accepted-HEAD.
- Closure commit: STATUS `[x]`, README capability sync (same commit,
  R-0154 pin), `scripts/self_use_queue.json` SU-007 `consumed_by=F112`,
  final `.agent/` state.
- AGENTS.md PR workflow; merge deferred to the next feature's start.

## Risks

- R-0784 (self-use/R-0418 curation gap, OPEN) and R-0767 (model-routing
  seam, OPEN) are both documented pre-existing risks, unrelated to F112.
- R-0790's fix touches a security-sensitive, four-consumer shared
  utility — full relevant test surface must stay green, not just the
  narrow case that motivated the fix.
- If the fix reveals a SECOND, different blocking commit subject once
  this one clears, that is its own registered finding, not folded here.