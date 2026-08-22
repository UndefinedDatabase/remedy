# Plan — F009 The single write channel

Branch: feature/f009-single-write-channel, cut from `main` at `ce49348b`, the
merge commit of pull request #209. `.agent/live_review.md` is the source of truth
for the open set, the round map and the finding-id ceiling.

## Goal
Exactly ONE door for UI-initiated change: POST /api/jobs/{jid}/commands validates
against the UI-exposed catalog subset, authenticates with a bearer token plus an
X-Remedy-CSRF double-submit, rate-limits per token and job, deduplicates by
client nonce, and ENQUEUES into the existing decision, approval and control
machinery without touching files, jobs or shells directly. Every other POST, PUT
and DELETE answers 405. DONE when the exposed commands round-trip through their
effects on fixtures, replayed nonces are idempotent, unauthenticated and
cross-site attempts fail closed and are audited as rejected, and a route-walking
test plus an import guard prove no other mutating route exists.

## Current Step
R34 is closure round two and the last round of this branch. It records the R33
verdict, then one commit carries the STATUS `[x]` line, the README capability
sync and the closure candidate, and the pull request is created from it.

## Next Steps
1. Nothing remains on this branch. The pull request is NOT merged in this
   session.
2. The next session's Open PR Gate merges it before any new feature is claimed,
   which is the operator's manual-review window.

## Risks
- The STATUS edit must be the LAST commit on the branch (Rule A4), so the
  handback is written inside that same commit rather than after it.
- README and STATUS may never disagree in any committed state (R-0154), which
  is why both land in one commit and the docs gate runs at it.
- Two open High findings, R-0495 from F085 and R-0574 from F086, are inherited
  from closed features and are documented risks, not F009 defects; the verdict
  is PASS_WITH_RISKS, exactly as F008 closed one feature ago.
