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
R11, this round: close the session. Record the R10 verdict and write the
reviewer's own session verdict to disk, so that no verdict this session issued
exists only in a transcript (finding R-0571). No code, no test, no PR.

## Next Steps
1. R12 — the REVISION embedding T002 still owes. `resolve_build_revision()` in
   `apps/cli/version_report.py` reads a `REVISION` file out of the installed
   distribution's metadata and NOTHING WRITES THAT FILE, so an installed wheel
   reports `dev` exactly as a checkout does. `hatch_build.py` is where it gets
   written, beside the asset guard that already lives there.
2. Then T003 — the release CI stage, the changelog and tag gate, the wheel-size
   budget and the seeded-failure tests.
3. Then the install smoke, the integration gate, and closure. The packaging
   ist-doc is written at closure, when the built state stops moving.

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
