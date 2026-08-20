# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1. R31 is the
closure round and the branch terminator; its pull request is created by this round
and merged by the NEXT feature's Open PR Gate, never here.
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
R31: register R-0597, record R30's verdict, then the closure commit — the `[x]`
STATUS line with the values R30 measured, the README capability sync in that SAME
commit (R-0154), and the handback — followed by the pull request, unmerged.

## Next Steps
1. THE PR IS NOT MERGED BY THIS SESSION. It merges at the next feature's start
   through the AGENTS.md Open PR Gate, which is the operator's manual-review
   window; the operator may merge it manually at any time instead.
2. THE NEXT FEATURE is selected by Rule A5 from `docs/roadmap/STATUS.md` — the
   first `[ ]` in ledger order — in a FRESH session. Its first reviewed round
   reads `.agent/candidates.md`, which this closure leaves empty and correct.
3. R-0597 IS OPEN AND ROUTED, not fixed here: the closure commit's path set is
   fixed by R-0154 at STATUS.md, README.md and `.agent/`, and the finding's
   counter-measure already exists as checklist item 8 — it was not run, rather
   than missing — so nothing is owed to `docs/agents/`.

## Risks
- THE FEATURE'S OWN DONE CONDITION IS NOT FULLY PROVEN and closure says so rather
  than counting a skipped test as coverage: no wheel has been installed into a
  fresh virtualenv, and `.github/workflows/release.yml` has never been dispatched.
  Both are human actions and both are named in the STATUS line's PASS_WITH_RISKS.
- The review package is 71% `.remedy-wt/` scratch by member count (R-0403, open
  and routed to a paydown branch); it inflates the package and is not a failure.
- The open set closes PASS_WITH_RISKS, as F083 and F085 both did.
