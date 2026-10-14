# Handback — F308 round 3 — R-1314 and R-1315 repaired, the design document gains its section

## Session

SESSION 1 of feature F308 · round 3 · rounds so far 3

Context self-assessment: C1 to C3 landed clean on the first attempt for their own content; gate 1
then caught a real defect in C2 (the F7 refusal's repaired message split its own required phrase
across two f-string lines, so it no longer appeared contiguous on disk) that was repaired by a
non-destructive reset back to C2 and a re-commit of C2 and C3, with nothing pushed at any point;
context held comfortably throughout.

Fortschritt: ~75 % (T001 to T003 landed, R-1314 and R-1315 repaired · the closure open) — Schätzung

## Range

Review of `59ce28989`..`cf14bfbae`

## Commits

### da23b72bf F308 R3 C1: book round 2, register R-1314 and R-1315, the plan, save the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f308-r3.md` | +104/-0 | NEW FILE, byte copy of `block.md` (104 lines, sha256 `bcc13980c1f99eadfcf821fa13cf2e74625e4dc99b85670df71e9143e4d80b66`) |
| `.agent/live_review.md` | +6/-0 | round 2's PASS booked and R-1314/R-1315 registered, byte-identical to `dry-live_review.md` |
| `.agent/plan.md` | +5/-6 | rewritten for round 3 (Current Step and Next Steps updated), byte-identical to `dry-plan.md` |

### eff0b05c6 F308 R3 C2: a part split again in the same episode, and the F7 refusal names the definition (R-1314, R-1315)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/run_task_list.py` | +14/-8 | R-1314: `task_ids_after_splits` now counts a split's parent in `out` (the list as it stands after the splits before it) rather than in the original `ids`, so a part split again in the same episode is accepted; its docstring updated to match. R-1315: `checked_episode_task_list`'s F7 refusal names the DEFINITION's list unchanged (byte-for-byte the pre-F308 wording with no split recorded) and, when the episode recorded at least one split, appends `, with this episode's recorded splits applied: <list>` before the `(F7: ...)` clause |
| `tests/orchestration/test_run_task_list.py` | +19/-0 | two tests added to `TestTaskIdsAfterSplits`: a split of `T001` into `T001a`/`T001b` followed by a split of `T001a` into `T001c`/`T001d` gives `["T001", "T001a", "T001c", "T001d", "T001b"]` with no problem; the same two splits in the opposite order leave the second unapplied and report one problem |
| `tests/orchestration/test_run_manifest_call_task_binding.py` | +21/-0 | one test added to `TestASplitTheRunRecorded`: an edit from outside after a recorded split (one more task appended) is refused with a message containing both the definition's list and the words `with this episode's recorded splits applied` |

### cf14bfbae F308 R3 C3: the run manifest's design document describes the split

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T0_F012.md` | +29/-0 | new section "A task the run splits (F308, 2026-10-14)" copied byte-identical from `dry-T0_F012.md`, describing the split record, the F7 check, the manifest field, the declared-list binding, the split-parent expectation and the cross-episode chain rule |

### (this commit) F308 R3 C4: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite per `docs/agents/handback_template.md` |

## External actions

- No worktree added or removed (beyond the pre-existing `.remedy-wt/f308-r3-worker/` scratch
  directory the block told the worker to create for throwaway scripts; nothing under it is
  tracked or committed).
- No `gh pr merge`, `gh pr edit`, `gh pr create` (the block orders no PR this round).
- No branch created beyond the one already checked out. The Open PR Gate was checked at session
  start: `gh pr list --state open ...` returned an empty list, so no merge was required.
- Push (`git push origin feature/f308-run-manifest-task-split`) runs after this commit; its
  outcome is reported in the session's final reply only, per the write-once rule — it did not
  exist when this file was written.

## Verification

Preconditions confirmed before C1: `git branch --show-current` read
`feature/f308-run-manifest-task-split`; `git rev-parse HEAD` read
`59ce28989283bdf32b7088090f8539663215dbd5`; the tree was clean. `block.md` was verified first: 104
lines, sha256 `bcc13980c1f99eadfcf821fa13cf2e74625e4dc99b85670df71e9143e4d80b66` — matches the
digest given in the prompt that delivered it. `dry-live_review.md`, `dry-plan.md`,
`dry-T0_F012.md`, `verify.py`, `run_selection.py` and `selection.txt` were each checked by
`sha256sum` against the digests given in the prompt before any use; all six matched.

C1: `block.md`, `dry-live_review.md` and `dry-plan.md` were copied to their paths; `cmp` printed
nothing for each pair.

C2: `task_ids_after_splits` and `checked_episode_task_list` were read in full against R-1314's and
R-1315's text in `dry-live_review.md` before editing; the repair was traced by hand against the
new test cases before running them. `ruff check` on the three changed files — `All checks
passed!`. `pytest tests/orchestration/test_run_task_list.py
tests/orchestration/test_run_manifest_call_task_binding.py -q` — `34 passed` (19 + 15), no
existing test edited (confirmed by reading the diff: every change to the two test files is an
addition only).

C3: `dry-T0_F012.md` was copied over `docs/roadmap/features/T0_F012.md`; `cmp` printed nothing;
the staged diff was read and checked against the production code's actual behavior before
committing (29 insertions, no deletions).

Gate 1, first run (after C3) — RED: `git status --porcelain` empty, but
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f308-r3/prep/verify.py /home/decodeux/Repos/remedy`
printed `False the F7 refusal keeps its words` and `ALL False`. Cause: C2's repaired message put
the phrase the gate checks for (`no longer matches the episode-start snapshot's job-input
definition`) across two adjacent f-string literals split at a line break between "episode-start "
and "snapshot's ...", which joins correctly at runtime but does not appear as one contiguous
substring in the raw file bytes the gate reads. Repair: nothing had been pushed, so the branch was
moved back to C2 with `git reset --soft`, the docs change was unstaged (not discarded) and left
untouched in the working tree, the f-string was rewritten so the required phrase sits inside a
single literal, the three affected files were re-tested and re-linted, C2 was amended in place
(still unpushed, so no history was shared yet), and C3 was then re-committed from the same
preserved working-tree diff with its original message. Final SHAs are the ones in the Commits
section above.

Gate 1, re-run after the repair — GREEN: `git status --porcelain` empty;
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f308-r3/prep/verify.py /home/decodeux/Repos/remedy`
— all 15 lines `True`, last line `ALL True`.

Gate 2: `python3 -m ruff check packages/orchestration/run_task_list.py
tests/orchestration/test_run_task_list.py
tests/orchestration/test_run_manifest_call_task_binding.py` — exit 0, `All checks passed!`.

Gate 3: `python3 /home/decodeux/Repos/remedy/.remedy-wt/f308-r3/prep/run_selection.py
/home/decodeux/Repos/remedy /home/decodeux/Repos/remedy/.remedy-wt/f308-r3-worker/selection-output.txt`
— exit 0. Paths: `192 paths`. Summary: `7284 passed, 5 skipped in 86.08s (0:01:26)`. No FAILED,
ERROR or `process(es) behind` line. Every SKIPPED line:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/regression/test_f293_acceptance.py:191: main holds F293, so its own changes are history
SKIPPED [1] tests/regression/test_f294_acceptance.py:73: main holds F294, so its own changes are history
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
```

Gate 4: `python3 -m apps.cli.main integrity check --json` — exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Six checks, all `pass`; `"fail_count": 0`.

Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
— exit 0, list `['R-1246', 'R-1252', 'R-1276', 'R-1277', ..., 'R-1315']` (R-1246, R-1252, then
R-1276 to R-1315 in order), length 42.

## Authored-text proofs

- `.agent/authored/f308-r3.md` against `block.md`: byte-equal, 104 lines, sha256
  `bcc13980c1f99eadfcf821fa13cf2e74625e4dc99b85670df71e9143e4d80b66`.
- `.agent/live_review.md` (C1) against `dry-live_review.md`: byte-equal.
- `.agent/plan.md` (C1) against `dry-plan.md`: byte-equal.
- `docs/roadmap/features/T0_F012.md` (C3) against `dry-T0_F012.md`: byte-equal.
- C2's production and test edits wrote no prepared reviewer-authored text (the repair and the
  tests were the worker's own, written from R-1314's and R-1315's text in `dry-live_review.md`);
  nothing further to compare there.

## Deviations & assumptions

1. C2, as first committed, left the F7 refusal's repaired message with its required phrase split
   across two f-string lines at "episode-start " / "snapshot's ...", so gate 1's contiguous-text
   check on the raw file failed (`False the F7 refusal keeps its words`). Nothing had been pushed,
   so rather than add a new commit (which the block's fixed C1–C4 sequence and `verify.py`'s exact
   three-commit chain check do not allow), the branch was moved back to C2 with `git reset --soft`
   — never `--hard`, never a stash — the pending C3 docs change was unstaged but left intact in the
   working tree, the wording was fixed, C2 was amended in place, and C3 was re-committed unchanged
   from the preserved working-tree diff. The resulting SHAs (`eff0b05c6`, `cf14bfbae`) are the ones
   in the Commits section above; the first (buggy) C2 commit (`b2be1aba9`) never left this
   checkout and was never pushed.

No other departure from the block's ordered commit sequence occurred.

## For the operator, in plain sentences

This round first wrote down two small repairs that last round's review had asked for. One fixed
how the run counts a task's appearances when that same task gets split a second time within one
episode, so a part that is split again is now accepted instead of wrongly refused. The other fixed
the wording of the message shown when a run's task list no longer matches what it is supposed to
be: it now always names the original plan the same way it always did, and only adds a short extra
clause describing any splits this run recorded when there actually were any. Both repairs carry a
test that fails without the fix. The round also added a short new section to the existing design
document for the run manifest, describing how a split is recorded and checked, so that document
now matches what the code actually does. While wiring in the wording fix, one early attempt put
two pieces of the message's text on separate lines in a way a later check could not read as one
phrase; nothing had been published at that point, so the two commits involved were quietly
corrected and nothing was lost. Everything that already worked before this round still works
exactly as before.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. The Open PR Gate, which runs at the start of the next session.
3. Book round 3's verdict in the next round's first commit.
4. The closure sequence.

Operator questions open: 0.
Open findings: 42 (R-1252, R-1314 and R-1315 owned by F308, the rest by F307).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | amended once after a wording-contiguity fix (deviation 1); final SHA `eff0b05c6` |
| C3 | done | re-committed unchanged alongside C2's amend (deviation 1); final SHA `cf14bfbae` |
| C4 | done | this handback |
| Gate 1 | done | red once (contiguity check), green after the amend: all `True`, `ALL True` |
| Gate 2 | done | `All checks passed!` |
| Gate 3 | done | exit 0, 192 paths, 7284 passed, 5 skipped |
| Gate 4 | done | exit 0, six checks `pass`, `fail_count` 0 |
| Gate 5 | done | open set is R-1246, R-1252, R-1276 to R-1315, length 42 |
| R-1314 | done | repaired in `task_ids_after_splits`, held by two new tests |
| R-1315 | done | repaired in `checked_episode_task_list`, held by one new test |
| Push | pending | runs after this commit; outcome reported in the session's final reply only |
