# Plan — F086 Release capability

Branch: feature/f086-release-capability, pushed and unmerged, cut from `main` at
76661dc1. No pull request exists: this feature is mid-flight and its PR belongs to
its closure round. `.agent/live_review.md` is the source of truth for the open set,
for the next free finding id and for the round map; this file repeats none of them.

## Goal
Remedy ships like a normal tool: `pip install` yields the `remedy` CLI with the
UI assets bundled, `remedy --version` reports version and build info, and a
release is gated by CI plus a semver and changelog discipline. DONE when a wheel
built from a clean checkout installs into a fresh virtualenv where the golden
path and the UI serve work, the version command matches the tag, and a release
with a missing changelog entry is refused by the gate.

## Current Step
R16, this round: the TRIGGER, and the session closes. A manual-trigger
`.github/workflows/release.yml` builds the wheel, reads this commit's real CI
conclusion and calls `scripts/release_gate_check.py`; text guards keep it manual,
thin and publish-free. Then the R15 verdict is recorded and the reviewer's own
session verdict is written to disk (finding R-0571).

## Next Steps
1. The install smoke T2_F086 T001 still owes: a fresh virtualenv, the wheel
   installed into it, `remedy` on PATH, and the golden path and the UI serve
   probed from it. The round that writes it must name its execution host.
2. Then the integration gate (docs/agents/integration_gate.md) and closure. The
   packaging ist-doc is written at closure, when the built state stops moving.
3. THE RELEASE WORKFLOW HAS NEVER BEEN RUN. It is gated as TEXT, the way
   `tests/orchestration/test_ci_workflow.py` gates `ci.yml`. No round can
   dispatch it; its first real run is a human action, and its guards check what
   they say and nothing more.

## Risks
- The install smoke creates a fresh virtualenv and runs the wheel's console
  script. This session's permission layer refuses to execute any interpreter
  under `.remedy-wt/`, so the round that writes it must name its execution host
  or it will be unverifiable where it matters.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches.
