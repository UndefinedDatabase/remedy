# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
all closure preconditions satisfied. R-0790 fixed round 24 (positive
lookahead in ABS_PATH_RE); a trivial transport whitespace defect
(R-0791) is owed. Round 25 fixes R-0791, re-runs the evidence job and
review zip against the new head.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 25 books RECORD24 (registers R-0791), fixes R-0791 with a single
whitespace-only edit to `tests/orchestration/test_failure_postmortem.py`
(net zero byte-count change), confirms `ruff` clean, then re-runs the
evidence job (`job_evidence.create_manual_completion_bundle`, fresh
job_id, new head) and the review zip. If the zip succeeds: report the
package/hash/path for the STATUS line.

## Next Steps

- Once the zip succeeds: reviewer authors the STATUS line.
- Closure commit: STATUS `[x]`, README capability sync (same commit,
  R-0154 pin), `scripts/self_use_queue.json` SU-007 `consumed_by=F112`,
  final `.agent/` state.
- AGENTS.md PR workflow; merge deferred to the next feature's start.

## Risks

- R-0784 (self-use/R-0418 curation gap, OPEN) and R-0767 (model-routing
  seam, OPEN) are both documented pre-existing risks, unrelated to F112.
- If the zip finds a SECOND blocking commit subject, that is its own
  registered finding — do not attempt a blanket regex widening to
  pre-empt one that has not been measured.