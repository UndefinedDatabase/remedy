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
R17, this round: record R16's verdict, register finding R-0584 and repair it.
Three of the release workflow's seven text guards assert a positive existence over
text that includes the file's COMMENTS, and two of them are satisfied by a comment
alone — the `${found:-missing}` fallback can be deleted, and the only trigger the
workflow has can be commented out, with the suite green either way. All three
positive checks move onto the file's executable lines.

## Next Steps
1. The install smoke T2_F086 T001 still owes: a fresh virtualenv, the wheel
   installed into it, `remedy` on PATH, and the golden path and the UI serve
   probed from it. The round that writes it must rule, as a DECISION, WHERE that
   smoke executes — an opt-in marker, a `ci.yml` stage, or a step of
   `release.yml` — because no self-drive session can run it here.
2. Then the integration gate (docs/agents/integration_gate.md) and closure. The
   packaging ist-doc is written at closure, when the built state stops moving.
3. THE RELEASE WORKFLOW HAS NEVER BEEN RUN. It is gated as TEXT, the way
   `tests/orchestration/test_ci_workflow.py` gates `ci.yml`. No round can
   dispatch it; its first real run is a human action, and its guards check what
   they say and nothing more.

## Risks
- The install smoke creates a fresh virtualenv and runs the wheel's console
  script. MEASURED at R17 rather than assumed: this session's permission layer
  refuses to execute an interpreter under `.remedy-wt/`, so a self-drive round can
  write that smoke but cannot run it, and the round that writes it says so.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
