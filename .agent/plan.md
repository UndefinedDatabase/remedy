# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1. Pull request
#207 is open and unmerged; the CI check on 665c45df, run 32405232165, is green —
the first green run this branch has had. It merges at the next feature's Open PR
Gate.
`.agent/live_review.md` is the source of truth for the open set, for the next free
finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R35: record R34's verdict in `.agent/live_review.md` so it is not stranded
(DECISION F085 D9). This round registers no finding, resolves none, and changes
no source file, test or document.

## Next Steps
1. THE OPEN PR GATE MERGES #207, per AGENTS.md, before any new branch is cut.
   The operator may merge it manually at any time instead.
2. R35'S OWN VERDICT IS RECORDED BY THE NEXT FEATURE'S FIRST REVIEWED ROUND,
   the way F085's closure candidates reached F086 R1. R35 does NOT claim the
   terminator carve-out: R-0583 gives that to the round creating the branch's
   pull request, which was R31, so the regress ends at the merge and not here.
3. F086 STAYS `[x]` IN THE LEDGER. Neither R-0598 nor R-0599 falsifies the
   closure's own claim, so each correction is a dated ledger entry and never a
   rewrite of a landed STATUS line.

## Risks
- THE FEATURE'S OWN DONE CONDITION IS NOT FULLY PROVEN and closure says so rather
  than counting a skipped test as coverage: no wheel has been installed into a
  fresh virtualenv, and `.github/workflows/release.yml` has never been dispatched.
  Both are human actions and both are named in the STATUS line's PASS_WITH_RISKS.
- A GREEN CI RUN IS NOT A WHEEL INSTALL. It proves the dev install and the suite,
  which is what R-0598 broke, and it proves neither risk above.
- R-0571 IS THE HOLE THIS ROUND ROUTES AROUND BY HAND rather than fixes: a last
  round whose verdict was written and one whose verdict was never written are
  indistinguishable on disk, and the fix edits files F086 does not own.
