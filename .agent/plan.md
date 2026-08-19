# Plan — F085 Sandbox hardening (stage 1) — CLOSED, merge blocked

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
BLOCKED at the Open PR Gate. PR #204 is OPEN, MERGEABLE and not a draft, but its
`ci` check is FAILURE (run 32292354363, 43m26s), so `mergeStateStatus` is
UNSTABLE. AGENTS.md orders stop-and-report, not a merge. The full suite is EXIT 0
at the PR head 4c2d707b, so the red is not a local test failure; WHICH CI stage is
red is unknown, because `gh run` and `gh api` are denied in this sandbox and the
job log could not be read.

## Next Steps
1. Read the log of CI run 32292354363 and name the red stage.
2. Fix it on this branch, or record why the check is not a merge blocker.
3. Merge #204 at the Open PR Gate; then claim the next feature by Rule A5, whose
   FIRST reviewed round empties `.agent/candidates.md` — TWO entries are open.

## Risks
- CI runs its stages serially: `pytest_argv_for_stage` adds no `-n auto` and
  `pyproject.toml` sets no `addopts`, where local runs use `-n auto`. A stage may
  be dying at its budget (exit 124, note `timed out`) rather than on a real
  assertion. Unmeasured — read the log before acting on it.
- The R75 record round (e950e8af..4c2d707b, `.agent/` only) carries no gate entry,
  by the terminator rule its own carrier candidate describes.
