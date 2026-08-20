# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1. Pull request
#207 is open and its CI check is GREEN at 665c45df, run 32405232165 — the first
green run this branch has had. It merges at the next feature's Open PR Gate.
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
R33: record R32's verdict, resolve R-0598 — the editable-target exemption, which
the branch's own CI run now proves in the environment that found the defect — and
register R-0599 against the pair-shape reading the R32 block declared. State
files only; no source file, test or document changes.

## Next Steps
1. THE REVIEWER GATES R33. If R33 ends the branch its verdict has no on-disk gate
   entry by construction, and that absence is the terminator rather than a missing
   gate (docs/agents/planner_reviewer_prompt.md section 4 item 13).
2. THE OPEN PR GATE MERGES #207 at the start of the next feature, per AGENTS.md —
   not in this round. The operator may merge it manually at any time instead.
3. F086 STAYS `[x]` IN THE LEDGER. Neither R-0598 nor R-0599 falsifies the
   closure's own claim — a shipped wheel is still refused without UI assets, and
   the accepted evidence names the commit it was taken at — so each correction is
   a dated ledger entry, never a rewrite of a landed STATUS line.

## Risks
- THE FEATURE'S OWN DONE CONDITION IS NOT FULLY PROVEN and closure says so rather
  than counting a skipped test as coverage: no wheel has been installed into a
  fresh virtualenv, and `.github/workflows/release.yml` has never been dispatched.
  Both are human actions and both are named in the STATUS line's PASS_WITH_RISKS.
- THE GREEN RUN IS A CI RUN, not a wheel install. It proves the dev install and
  the suite, which is what R-0598 broke, and it proves neither risk above.
- The review package is 71% `.remedy-wt/` scratch by member count (R-0403, open
  and routed to a paydown branch); it inflates the package and is not a failure.
