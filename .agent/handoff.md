# Handoff — F290 Findings paydown v6, paused at the weekly usage cap after round 2

## Session

SESSION 1 of feature F290 · round 2 · rounds so far 2

Context self-assessment: the reviewer's context is comfortable; the session ends because the loop
runner wrote `.agent/STOP` at the weekly usage cap, not because of the context.

Fortschritt: ~30 % (T001 to T004 landed · T005 to T007 open) — Schätzung

For the operator, in plain words: the automatic build loop paused itself because this week's usage
allowance reached the limit you set (60 percent). It starts again by itself after the allowance
resets on Wednesday, 7 October, at 01:00. Nothing is waiting for you. In this session the previous
feature, the background service called "remedy serve", was merged into the main line, and the
next feature, a clean-up of seven known defects, was started; four of the seven are repaired so
far, and all four repairs are tests or wording checks, not changes to how Remedy behaves.

## Range

Review of `491529fc8`..`491529fc8` — no round ran after round 2's handback; this commit only
rewrites this file.

## Commits

### this commit — F290 S1: handoff at the weekly usage cap

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | full rewrite | this file; copied byte for byte from the reviewer's prepared file `.remedy-wt/f290-stop/handoff.md` |

## External actions

- Session start: the Open PR Gate merged pull request 308 (F200) with
  `gh pr merge 308 --merge --delete-branch` after hosted CI run 36870609054 on `9bbe297df` passed
  both its Python 3.10 and its Python 3.12 job at its first attempt; `main` is `31542dbfd`.
- Round 1 pushed `feature/f290-findings-paydown-v6` (new branch) to `977f46f50`; round 2 pushed it
  to `491529fc8`. No pull request exists for it yet.
- This commit is pushed with `git push origin feature/f290-findings-paydown-v6`.
- The reviewer's disposable dry worktree `.remedy-wt/f290-r3-dry` (detached at `491529fc8`) is
  left in place for the next session's round 3, together with its prepared files under
  `.remedy-wt/f290-r3/`; the round 1 and round 2 dry worktrees were removed.

## Verification

None ordered: this commit changes `.agent/handoff.md` alone. Round 2's gates are in round 2's
handback at `491529fc8`.

## Authored-text proofs

`.agent/handoff.md` (this commit): byte comparison against `.remedy-wt/f290-stop/handoff.md`.

## Deviations & assumptions

None in this commit. `.agent/STOP` (author `remedy-weekly-cap`, 2026-10-01 16:43) is untracked and
is left in place: the loop runner removes it itself.

## Round 2's verdict, to book in round 3's first commit (amend0827-process-diet rule 1)

VERDICT PASS for F290 round 2, over `977f46f50`..`491529fc8` (commits `00c20e742` 137,
`fc29ef4a3` 42 and `491529fc8` 79 insertions, each single-parent), verified by dry run with
identical bytes, compared at `fc29ef4a3`. Round 2's handback says `git worktree list` read 11 lines;
it read 12, a miscount that changes nothing on disk. The gate entry, already written with the
resolutions of R-1125 and R-1133, is the prepared file `.remedy-wt/f290-r3/append-live_review.txt`
(sha256 `116dc9a729d44f375b5a7110c00593e583fda72bd9a81c3b3fc2bd19af700084`). If that scratch file
is gone, the next session writes the entry again from this paragraph.

## Round 3, prepared and not delegated

T005 (R-1129): `describeTaskEditConflict` in `apps/ui/src/api/taskEditSend.ts` reads a non-empty
`detail` before `current_version`, with two tests in `apps/ui/src/api/taskEditSend.test.ts`. In
the dry tree on `491529fc8`: two vitest mutations, each turning exactly its own new test red, with
an unmutated control of 1572 passed in `src/api`; the type check clean, with a red control; the
round's Python selection read `7273 passed, 15 skipped`. Prepared files under
`.remedy-wt/f290-r3/`; the block is not yet written. Before writing it, the next session
regenerates `selection.txt` (the last `compose.py` run rewrote it without
`tests/ui_contracts/test_task_edit_controls_contract.py`, which belongs in it) and re-checks every
prepared digest. The first full run in a fresh worktree installs `apps/ui/node_modules` and reads
four failures before it does; only the second run is a reading.

## Next

1. Phase 1 rule 1: `.agent/STOP` — while it exists, hand off again and end.
2. Phase 1 rule 2: the Open PR Gate (no pull request is expected to be open).
3. Confirm `origin`'s tip equals `feature/f290-findings-paydown-v6`'s tip named by this commit
   before delegating.
4. Round 3: book round 2's verdict and the resolutions of R-1125 and R-1133, and land T005
   (R-1129).

Operator questions open: 0.
Open findings: 5 (R-1117 Medium; R-1125, R-1129, R-1133, R-1137 Low; all owned by F290).

## Item status

| Item | Status | Reason |
|---|---|---|
| Open PR Gate: merge pull request 308 | done | merged as `31542dbfd` |
| Round 1: claim, F200 R14 booked, D1, T001, T002 | done, PASS | booked by round 2 |
| Round 2: R1 booked, T003, T004 | done, PASS | to book in round 3 |
| Round 3: T005 | prepared, not delegated | the session stopped at the weekly usage cap |
| T006, T007, hardening stage, closure | open | later rounds |
