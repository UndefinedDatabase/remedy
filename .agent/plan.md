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
R6, this round: record the R5 verdict, then land T001 part (a) of DECISION F086
D1 — the explicit wheel carry for `apps/ui/dist` — with the carry mechanism
chosen by building a wheel each way and counting what each one carries. The same
round reads, without acting on it, what `_get_frontend_dist()` returns from an
extracted wheel layout.

## Next Steps
1. R7 — the reviewer rules on R6's installed-layout reading, which bears directly
   on DECISION F086 D1 part (c): the dual-mode resolver is worth building only if
   the current three-parent expression fails from an installed layout. Then T001
   parts (b) and (c) as that ruling leaves them — the packaging-time guard that
   refuses a wheel whose `apps/ui/dist/index.html` is absent, and the
   installed-mode path that never spawns npm.

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
