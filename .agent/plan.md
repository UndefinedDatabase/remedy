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
R9, this round: land T001 part (b) — the packaging-time guard that refuses to
build a wheel whose `apps/ui/dist/index.html` is absent — together with the
two-mode resolver TEST that DECISION F086 D3 keeps after withdrawing the
two-mode resolver CODE. Register R-0580 and record the R8 verdict.

## Next Steps
1. R10 — T002: the version single-source and the build info behind
   `remedy --version`, with a checkout mode that reports "dev" honestly
   (DECISION F086 D2).
2. Then T003 — the release CI stage, the changelog and tag gate, the wheel-size
   budget and the seeded-failure tests; then the integration gate; then closure.
   The packaging ist-doc is written at closure, when the built state stops moving.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the wheel's
  console script. This session's permission layer refuses to execute any
  interpreter under `.remedy-wt/`, so that smoke cannot be proved green from a
  session with this posture; the round that writes it must name its execution
  host or it will be unverifiable where it matters.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is itself gitignore-matched, so any
  packaging probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches.
