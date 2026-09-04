# Plan — F112 Prompt budget per task class

Branch: feature/f112-prompt-budget-per-task-class, PR #234 OPEN (not
merged), base main. All six closure preconditions satisfied; the
evidence-packager contract fix (R-0792, R-0793) landed and independently
verified end to end against the real packaged zip
(remedy-review-20260904-123332-READY_FOR_REVIEW.zip, SHA-256
b0085f28a2c0c50654ed33be647ed986addc07c1c462324b1ee3fc1c8bb05927,
PACKAGE_STATUS=READY_FOR_REVIEW, EVIDENCE_AUTHORITATIVE=true).

## Goal

No prompt can silently balloon: every task class carries an input-token
cap, the context compiler fits under it via the existing demotion
cascade with full omission disclosure, and a context that cannot fit
raises a task-split decision instead of a truncated prayer
(docs/roadmap/features/T3_F112.md). ACHIEVED and CLOSED.

## Current Step

Round 32 books round 31's PASS verdict (bookkeeping only, closure
sequence exempt per amend0827 rule 1). The reviewer then waits for
hosted CI on PR #234 and merges directly once green, per the operator's
own explicit instruction opening this session.

## Next Steps

- Merge PR #234 once hosted CI is green (check status, then merge, as
  two separate commands).
- Hand back the built zip's name and SHA-256 to the operator for
  archiving and the formal package review.
- Next feature per STATUS order (Rule A5) starts a fresh session.

## Risks

- R-0784 and R-0767 (both OPEN, unrelated to F112) are documented,
  pre-existing risks; F112's live-review verdict is PASS_WITH_RISKS.
- A red hosted CI run is a blocker; the merge waits for it honestly
  rather than being forced.