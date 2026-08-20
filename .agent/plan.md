# Plan — F086 Release capability

Branch: feature/f086-release-capability, cut from `main` at 76661dc1, the merge
commit of PR #206. `.agent/live_review.md` is the source of truth for the open
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
R4, this round: record the R3 verdict, and rule as DECISIONs how the wheel comes
to carry the UI it serves and where the single version string lives — both from
what R3 measured rather than from the feature file's assumptions. No code and no
test this round.

## Next Steps
1. R5 — T001 begins: the packaging change DECISION F086 D1 rules, in its own
   commits — the wheel-side asset carry, the packaging-time guard that refuses
   to build a wheel with no UI, and the dual-mode resolver in
   `_get_frontend_dist()` with a test for each mode. The measured baseline it
   must move is a wheel of 414 members and 2038283 bytes carrying 0 members
   under `apps/ui/dist/`.

## Risks
- The install smoke F086 requires creates a fresh virtualenv and runs the
  wheel's console script. R3 measured that THIS session's permission layer
  refuses to execute any interpreter under `.remedy-wt/`, so the smoke cannot
  be proved green from a session with that posture; the round that writes it
  must name its execution host or it will be unverifiable where it matters.
- `_load_frontend()` reacts to a missing `dist/` by spawning npm, and
  `apps/ui/package.json` ships in the wheel, so an installed environment can
  reach the npm path with no `node_modules` present. DECISION F086 D1 rules
  that path off in installed mode; a T001 that carries assets but leaves the
  spawn reachable has fixed only half of it.
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, measured against
  the same files at the base.
