# Plan — F251 Full-suite stabilization (R3)

> NOT the authored f251-r3-2 text. That text failed its sha256 check
> (received c30e6828…, stated 8ac81a9a…) and unverified authored bytes are
> not committed, so this is the worker's own rewrite covering the same
> ground. R-0153 stays open until the authored plan is re-sent and applied.

## Goal
Three consecutive `pytest -n auto -q` runs with identical failure sets;
churn zero; standing red stays catalogued (operator ruling pending on the
13 D-classes). Zero quarantines — keep it that way unless a flake survives
an honest root-cause attempt.

## State
- S1/S2 done. S3 done except the 2 stopped F-A ids (product change).
- Fixed hermetically: F-C (1), F-B/F-E (5, one root cause), F-A/F-D (11 of
  13), 7 repo-scan ids (cwd fixture), F-F (3, this round). Churn 14 → 1–2
  ids/run before F-F.
- Churn gate attempt 2: run2 == run3 == expected 154; run1 +1 id (F-F).

## F-F — root-caused and fixed this round
A run manifest records Remedy's OWN worktree identity (HEAD, content hash,
dirty), and any untracked entry sets dirty. The reference manifest is
written when the job runs; the candidate is built moments later. Under
`-n auto` all 24 workers share one repo tree, so a neighbouring test
creating or removing a repo file between those moments produces a blocking
drift and `same_inputs` becomes False where the test requires None.
Deterministic reproducer: churn an untracked file in the repo root → 5/5
red; quiet tree → 3/3 green. Fix: freeze the identity per test to the value
observed at test start — the real value, not a forced "complete" — the same
seam the module already uses in `_patch_remedy_identity`. Product code
untouched: detecting a changed Remedy checkout is the intended F012
behaviour, so this is test hermeticity, not a product bug.

## Checklist
- [x] R3 verdict persisted (2a93e31)
- [x] F-F root cause + hermetic fix, proofs recorded
- [ ] Churn gate ×3 retry
- [ ] Operator ruling pending: 13 D-classes (154 standing red), the 2
      stopped F-A ids, and a re-send of f251-r3-2 for R-0153

## Current Step
Churn gate retry.

## Risks
- D4 ids stay coupled to live `.agent` state; gate comparisons name them.
- No D-class edits until the operator rules.
