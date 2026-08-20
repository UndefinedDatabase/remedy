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
R5, this round: record the R4 verdict and close the session. The claim, the
repair of the R1 carry, the measured packaging inventory and the two packaging
DECISIONs are all landed and gated. No code has been written yet — T001 has not
started.

## Next Steps
1. R6 — T001 begins, ruled by DECISION F086 D1 in `.agent/decisions.md`: the
   explicit wheel carry for `apps/ui/dist`, chosen by MEASUREMENT of what the
   installed hatchling honours; the packaging-time guard that refuses a wheel
   whose `apps/ui/dist/index.html` is absent; the dual-mode resolver in
   `_get_frontend_dist()` with a test per mode; and the installed-mode path that
   never spawns npm. The measured baseline it must move is a wheel of 414
   members and 2038283 bytes carrying 0 members under `apps/ui/dist/`.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the
  wheel's console script. This session's permission layer refuses to execute any
  interpreter under `.remedy-wt/`, so that smoke cannot be proved green from a
  session with this posture; the round that writes it must name its execution
  host or it will be unverifiable where it matters.
- Building a releasable wheel will require the UI to be built first, by DECISION
  F086 D1's own consequence. CI and any human cutting a release inherit that
  constraint, and a round that adds the npm build step routes it through the
  F085 `exec_guard` seam rather than a bare subprocess.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, measured against
  the same files at the base.
