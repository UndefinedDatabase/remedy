# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #233 merged (F110);
F112 claimed in STATUS.md round 1; T001-T003b2b2b2 complete and green,
all six closure preconditions satisfied. R-0790 and R-0791 both fixed
and verified. The review zip's `BLOCKED_EVIDENCE` status is an OPEN,
UNRESOLVED question (R-0792 registered on its own terms, not yet proven
the cause). Round 26 is a handoff: no code changes, no further guessing.

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion cascade
with full omission disclosure, and a context that cannot fit raises a
task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md).

## Current Step

Round 26 books RECORD25 (registers R-0792) and writes the session's
handoff per G8 (self_drive_protocol.md): the BLOCKED_EVIDENCE cause is
not yet confirmed, so the session ends here rather than guessing at a
fix. No `.agent`-outside file is touched.

## Next Steps

- Read `scripts/build_review_manifest.py` lines ~3200-3340
  (`evidence_valid`, `alignment_ok`, `containment_ok`, `gate_matrix`,
  `fv_ok_for_ready`, `git_status_ok`, `tt_ok_for_ready`,
  `_check_bundle_integrity`) against their ORDERING relative to the
  script's own "Evidence refresh completed for staged copy" step, since
  every individual gate file reads clean POST-refresh.
- Once the true cause is confirmed: fix it, re-run the evidence job and
  zip, then the reviewer authors the STATUS line.
- Closure commit: STATUS `[x]`, README capability sync, `self_use_queue`
  SU-007 `consumed_by=F112`, final `.agent/` state. PR after.

## Risks

- R-0784, R-0767 (both OPEN, unrelated to F112) and R-0792 (may or may
  not bear on the BLOCKED_EVIDENCE puzzle) all carry forward undecided.
- Do not mint a fix for BLOCKED_EVIDENCE without first confirming which
  of the seven package_status gates actually read false at build time.