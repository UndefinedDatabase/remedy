# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
integration gate PASSED round 19, self-use consumed round 21, Built
State landed round 22 (RECORD22: VERDICT PASS, booked this round). All
six closure preconditions are now satisfied. Round 23 runs the evidence
job and the mandatory review zip.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 23 builds the evidence bundle via
`job_evidence.create_manual_completion_bundle` (review_feature_id="f112",
scoped verification runs via `_run_verifications`, never a full-suite
node-id list), then the mandatory review zip
(`scripts/make_review_zip.sh --evidence-dir <path>`). Produces NO
repository diff — the evidence dir is never committed
(docs/roadmap/STATUS_closure_protocol.md). Results (job_id, package
filename, SHA-256, archived path or NOT ARCHIVED) are reported in the
handback for the reviewer to author the STATUS line from.

## Next Steps

- Reviewer authors the STATUS line from round 23's reported job_id/
  package/hash/path/accepted-HEAD.
- Closure commit: STATUS `[x]`, README capability sync (same commit,
  R-0154 pin), `scripts/self_use_queue.json` SU-007 `consumed_by=F112`,
  final `.agent/` state — nothing else.
- AGENTS.md PR workflow; merge deferred to the next feature's start.

## Risks

- R-0784 (self-use/R-0418 curation gap, OPEN) and R-0767 (model-routing
  seam, OPEN) are both documented pre-existing risks, unrelated to F112,
  carried forward per precondition 1's "Resolved or documented risk".
- Evidence-bundle construction has a documented history of BLOCKED_EVIDENCE
  pitfalls (F051/F052/F080) — round 23 uses the existing
  `_run_verifications` helper rather than hand-building verification_run
  dicts, specifically to avoid them.