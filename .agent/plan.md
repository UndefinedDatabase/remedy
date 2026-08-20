# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1. Pull request
#207 is open and NOT merged by this session; it merges at the next feature's Open
PR Gate, and only once its CI check is green.
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
R32: repair R-0598 — the build hook refused the editable target, so
`pip install -e ".[dev]"`, which is CI's first step, failed on every fresh clone
and no test in this branch's only CI run executed. Register the finding, record
R31's verdict, exempt the editable target behind a named predicate, and cover it.

## Next Steps
1. THE REVIEWER GATES R32 and, if it passes, authors `Done: R-0598` for the next
   round. The branch stays open until the CI check on #207 is green.
2. THE PR IS NOT MERGED BY THIS SESSION. It merges at the next feature's start
   through the AGENTS.md Open PR Gate, which is the operator's manual-review
   window; the operator may merge it manually at any time instead.
3. F086 STAYS `[x]` IN THE LEDGER. R-0598 does not falsify the closure's own
   claim — a shipped wheel is still refused without UI assets, and the accepted
   evidence names the commit it was taken at — so the correction is a dated
   ledger entry, never a rewrite of a landed STATUS line.

## Risks
- THE FEATURE'S OWN DONE CONDITION IS NOT FULLY PROVEN and closure says so rather
  than counting a skipped test as coverage: no wheel has been installed into a
  fresh virtualenv, and `.github/workflows/release.yml` has never been dispatched.
  Both are human actions and both are named in the STATUS line's PASS_WITH_RISKS.
- CI HAS NEVER RUN GREEN ON THIS BRANCH. R-0598 is the first failure it found;
  a second may sit behind it, because the run died before any test executed.
- The review package is 71% `.remedy-wt/` scratch by member count (R-0403, open
  and routed to a paydown branch); it inflates the package and is not a failure.
