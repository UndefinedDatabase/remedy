# Plan — F086 Release capability

Branch: feature/f086-release-capability, pushed and unmerged, cut from `main` at
76661dc1. No pull request exists: this feature is mid-flight and its PR belongs
to its closure round. `.agent/live_review.md` is the source of truth for the open
set, for the next free finding id and for the round map; this file repeats none
of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R7, this round: register the four defects R6 exposed in the reviewer's own gates,
record the R6 verdict, rule DECISION F086 D3, and land T001 part (a) — the
`artifacts` carry for `apps/ui/dist` in `pyproject.toml`. The carry mechanism was
selected by a measurement the reviewer executed itself, with a control that can
fail; R6's own control could not, which is finding R-0574.

## Next Steps
1. R8 — T001 part (b), the packaging-time guard that refuses to produce a wheel
   whose `apps/ui/dist/index.html` is absent, plus the two-mode resolver TEST that
   DECISION F086 D3 keeps after withdrawing the two-mode resolver CODE. The guard
   is owed because the carry alone is silent: measured at 72e07381, a build with
   the carry applied and no `dist/` present exits 0 and produces a 414-member
   wheel carrying 0 UI files.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the wheel's
  console script. This session's permission layer refuses to execute any
  interpreter under `.remedy-wt/`, so that smoke cannot be proved green from a
  session with this posture; the round that writes it must name its execution
  host or it will be unverifiable where it matters.
- A wheel that carries `apps/ui/dist` is only as honest as the directory it was
  built from, so a release now requires the UI to be built first — DECISION F086
  D1's own stated consequence, inherited by CI and by any human cutting a release.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, measured against the
  same files at the base.
