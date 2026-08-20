# Plan — F085 Sandbox hardening (stage 1) — CLOSED, CI repair in flight

Branch: feature/f085-sandbox-hardening. F085 is closed and accepted; the R74 PASS
verdict landed at 4c2d707b and as the single comment on PR #204.
`.agent/live_review.md` stays the source of truth for the open set, for the next
free finding id and for the round map; this file repeats none of them.

## Goal
Get PR #204 merged. F085's build goal is met and gated — builder-spawned commands
run under POSIX resource limits, a wall timeout, output caps, a pinned cwd, an
environment allowlist and a default-deny network posture, with the limitations
document written and linked. Nothing remains to BUILD in F085.

## Current Step
REPAIRING the red `ci` check on this branch, which is the Open PR Gate's blocker
for PR #204 (OPEN, MERGEABLE, not a draft). The log of run 32301614177 was read
under the operator amendment amend0820-gate-autonomy, which unblocks `gh run`.
The red was ONE cause, not a stage budget: the guard's own deny-network posture
emptied `NO_PROXY`, so a guarded child could not reach a loopback server it had
started itself, and 62 tests in the `fast` and `standard` stages failed with
`[Errno 111] Connection refused`. Fixed at f882c727 — see DECISION
amend0820-gate-autonomy A1 in `.agent/decisions.md`.

## Next Steps
1. Watch the CI run for f882c727 to the end. If red again, read the log and
   repair on THIS branch; the session does not end while the state is readable.
2. Merge #204 at the Open PR Gate; then claim the next feature by Rule A5, whose
   FIRST reviewed round empties `.agent/candidates.md` — TWO entries are open.

## Risks
- CI runs its stages serially: `pytest_argv_for_stage` adds no `-n auto` and
  `pyproject.toml` sets no `addopts`, where local runs use `-n auto`. MEASURED at
  run 32301614177: no stage tripped its budget — `fast` took 887.5 s and
  `standard` 1617.5 s, both under their caps, and both failed on assertions. The
  budget risk is not what was red; it stays listed because a slower hosted runner
  could still trip it later.
- The R75 record round (e950e8af..4c2d707b, `.agent/` only) carries no gate entry,
  by the terminator rule its own carrier candidate describes.
