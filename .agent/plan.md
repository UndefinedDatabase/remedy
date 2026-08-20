# Plan — no feature claimed; the Open PR Gate is CLEAR

Branch: `main`. F085 is CLOSED, ACCEPTED and MERGED — PR #204 merged at 68155931
with `--merge --delete-branch`. The operator amendment amend0820-gate-autonomy is
merged too (PR #205 at 86555049). `.agent/live_review.md` stays the source of truth
for the open set, for the next free finding id and for the round map; this file
repeats none of them.

## Goal
Claim the next feature by Rule A5. Nothing is in flight: no open PR, no feature
branch, no half-landed round. This file exists to say so plainly, because the next
session's Phase 0 reads it before it reads anything else.

## Current Step
IDLE at the gate, with the gate open. `gh pr list --state open` returns zero rows,
`git status --porcelain` is empty on `main`, and `.agent/STOP` is absent. The two
blockers the previous three sessions ended on are both gone:

- The red `ci` check on #204 was ONE cause, not a stage budget. The guard's
  deny-network posture emptied `NO_PROXY`, so a guarded child could not reach a
  loopback server it had started itself; 62 tests failed with `[Errno 111]
  Connection refused`. A 63rd, the deny test's own CONTROL, failed because CI runs
  pytest itself as a guarded child, so a control spawned with plain
  `subprocess.run` inherited the very posture it was meant to contrast with. See
  DECISION amend0820-gate-autonomy A1 in `.agent/decisions.md`.
- The reason no session could NAME that cause was a missing permission, not a
  protocol judgement. `Bash(gh run:*)`, `Bash(gh api:*)` and `Bash(gh pr checks:*)`
  are now in the tracked `.claude/settings.json`, and AGENTS.md's Open PR Gate now
  treats a running or red check as WORK. See DECISION amend0820-gate-autonomy A2.

## Next Steps
1. Re-read `.agent/STOP` from disk before anything else — Phase 1 rule 1.
2. Claim the next feature by Rule A5. Its FIRST reviewed round must register or
   resolve BOTH `.agent/candidates.md` entries and empty that file.

## Risks
- CI runs its stages serially: `pytest_argv_for_stage` adds no `-n auto` and
  `pyproject.toml` sets no `addopts`, where local runs use `-n auto`. MEASURED
  across three hosted runs on 2026-08-19/20: no stage has yet tripped its budget —
  the widest `standard` sample was 1617.5 s against a 2100 s cap. The risk stays
  listed because a slower hosted runner could still trip it; the budget is then
  re-derived by the rule `tests/orchestration/test_ci_stages.py` states, from a
  re-measured maximum, never raised by hand.
- The R75 record round (e950e8af..4c2d707b, `.agent/` only) carries no gate entry,
  by the terminator rule its own carrier candidate describes.
- `.claude/settings.local.json` is gitignored and read-denied, so what it grants or
  denies cannot be inspected from inside a session. The three grants above were
  therefore added to the TRACKED settings file; whether they take effect is
  observable only from a session that is not in bypass-permissions mode.
