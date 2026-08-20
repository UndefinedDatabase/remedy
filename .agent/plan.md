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
R19, this round and this session's last: record R18's verdict, register R-0585 —
a done-when gate of the R18 block counted a path list that lives in another
section of that block — and promote the rule it exposes into the §3 pre-emission
checklist, item 16, where a rule has to live to bind the next block.

## Next Steps
1. R20 writes the install smoke per DECISION F086 D4: one `smoke`-marked,
   `slow`-marked module that SELF-SKIPS unless `REMEDY_INSTALL_SMOKE` is set. What
   it can gate is the skip path and the module's own logic; what it cannot gate is
   the install itself, and it says so rather than implying coverage.
2. Then the smoke's wall-clock is MEASURED on a host that can run it, and only
   then is a CI stage chosen to opt in — the `smoke` stage carries a 300 s budget
   that AGENTS.md forbids raising by hand.
3. Then the integration gate (docs/agents/integration_gate.md) and closure. The
   packaging ist-doc is written at closure, when the built state stops moving.
4. THE RELEASE WORKFLOW HAS NEVER BEEN RUN, and no round can dispatch it; its
   first real run is a human action.

## Risks
- The install smoke needs network, a venv interpreter and minutes. MEASURED at
  R17: this session's permission layer refuses to execute an interpreter under
  `.remedy-wt/`, so a self-drive round can write that smoke but cannot run it.
- A build tool's file selection depends on WHERE the tree is: hatchling drops
  every VCS exclusion when the build root is gitignore-matched, so any packaging
  probe uses a worktree OUTSIDE this repository (finding R-0574).
- Ruff is RED repo-wide at 26 pre-existing errors and is NOT a gate; a round
  touching Python gates ruff scoped to the files it touches, by multiset.
