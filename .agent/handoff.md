# Handoff — F029, round 3

## Session

SESSION 1 of feature F029 · round 3 · rounds so far 3. Context remaining at
handback: comfortable — reading the block's named files (`subtree_rerun.py`,
`cost_preview.py`, `budget_resolution.py`, `job_veto_cmd.py`, `job_inject_cmd.py`,
the catalog, `commands/__init__.py`, exit-codes docs/tests, the orphan/reachability
allowlists, `test_job_veto.py`, `test_subtree_rerun_prepare.py`) and drafting S1–S4
plus their tests and the mutation tool took the bulk of it; every gate ran clean
on the first pass, with ample context left had a repair round been needed.

## Range

Review of `aa054d8b`..`HEAD` (`HEAD` is this handback's own commit, `F029 R3
C6b`, on `feature/f029-subtree-rerun`).

## Commits

### ba2cc9e14 F029 R3 C1: copy round 3 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r3-block.md | 260/0 | copy of this round's block |
| .agent/authored/f029-r3-booking.diff | 63/0 | copy of the booking diff payload |
| .agent/authored/f029-r3-plan.md | 33/0 | copy of the plan payload |

Measured insertions: 356 (block's own line count 260 + 96), matching the
block's expectation exactly, under the 500-line cap.

### e00da9cb8 F029 R3 C2: book round 2's PASS, resolve R-1080, register R-1081, record D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 41/0 | DECISION F029 D3 appended |
| .agent/live_review.md | 6/0 | round 2's Gate entry, R-1080's `Done:` line and R-1081's registration appended |
| .agent/plan.md | 10/11 | rewrite from the plan payload |

Matches the block's expected numstat (41/0, 6/0, 10/11) exactly. Applied via
`git apply --check` (exit 0) then the real apply (exit 0) of `booking.diff`,
followed by the `plan.md` rewrite via `shutil.copyfile`.

### 427ee8322 F029 R3 C3: R-1081 — never leave a rerun's worktree lock held
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/subtree_rerun.py | 67/36 | S1 (a): every subtree task's rerun-archive destination checked BEFORE `worktrees.create`, refusing `stream_archive_occupied` with nothing touched; S1 (b): a `completed`/`refused` flag pair checked in a `finally` calls `worktrees.retain_for_recovery` on any exit that is neither success nor a `SubtreeRerunRefused`, using `sys.exc_info()` rather than a blind `except Exception`/`except BaseException` |
| tests/orchestration/test_subtree_rerun_prepare.py | 45/0 | new `TestR1081Repair`: an occupied archive destination refuses with no worktree re-added and `job.json` byte-identical; a `save_job_plan` raising `OSError` leaves the lock free and the error propagating |

### d86c54002 F029 R3 C4: estimate a subtree rerun's cost from its plan bands
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/subtree_rerun.py | 66/0 | S2: `subtree_rerun_cost_estimate` sums each subtree task's plan-band estimate via `estimate_cost_band`/`PLAN_BAND_TO_TOKEN_BAND`, unavailable as a whole when any task has no band, an unrecognised band or an unpriced config |
| tests/orchestration/test_subtree_rerun_prepare.py | 59/0 | new `TestSubtreeRerunCostEstimate`: S/M bands sum to 0.4 at both bounds at the block's stated price basis and class defaults; one XL task, and one task without a band, each make the whole estimate unavailable with `unpriced` naming it |

### 6a195b143 F029 R3 C5: add remedy job rerun-subtree behind the cost preview
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job_rerun_cmd.py | 131/0 | new module: S3, `_cmd_rerun_subtree` — job/task resolution, the cost preview, `prepare_subtree_rerun`, the refusal-code mapping and both the JSON and human answers |
| apps/cli/command_catalog.py | 27/0 | S4: the `job.rerun-subtree` `CommandEntry` after `job.veto-task`'s, `is_expensive=True`, `--yes` worded as `job.resume`'s |
| apps/cli/commands/__init__.py | 2/1 | S4: `job_rerun_cmd` joins the import list and the `for mod in (...)` tuple |
| docs/guides/exit-codes.md | 1/0 | S4: `remedy job rerun-subtree \| 3` row |
| tests/cli/test_job_rerun_subtree.py | 175/0 | new CLI test file: the yes/json path, the human answer's last line, the model override, the confirmation-required/declined-prompt paths, and every refusal's exit code (`unknown_task`, `model_invalid`, `job_running`, `interleaved` with `facts`, `job_not_found`) |
| tests/orchestration/import_reachability_allowlist.txt | 2/0 | S4: `apps.cli.commands.job_rerun_cmd` and `packages.orchestration.subtree_rerun`, the two modules `test_import_reachability.py`'s own failure named once the command wired the module in |
| tests/test_command_catalog.py | 4/3 | S4: `test_exactly_one_command_is_marked_expensive_so_far` renamed to `test_exactly_two_commands_are_marked_expensive_so_far`, now pinning `["job.rerun-subtree", "job.resume"]` |
| tests/test_no_orphan_modules.py | 0/2 | S4: `subtree_rerun.py`'s `ALLOWED_UNWIRED` entry removed — it is wired now |

342 total insertions, under the 500-line cap; no split needed.

### b7b1092b5 F029 R3 C6a: add the mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r3-mutations.py | 185/0 | the G5 mutation (red-proof) tool, covering m1–m10 across `subtree_rerun.py` and `job_rerun_cmd.py` |

### (this commit) F029 R3 C6b: rewrite handoff for round 3
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file |

## External actions

`git worktree add --detach .remedy-wt/f029-r3-mut 6a195b143` — created the disposable
mutation worktree at the last commit before C6b. `git worktree remove --force
.remedy-wt/f029-r3-mut` then `git worktree prune` — removed it after G5; `git worktree
list | wc -l` read 61 both before and after, matching the step-4 reading. `git push
origin feature/f029-subtree-rerun` — reported below under Verification/G6; its real
outcome is in the reply to the delegator, since C6b cannot contain it. No PR opened,
no merge, no branch deleted, no force-push, no stash.

## Verification

**BEFORE ANYTHING ELSE**
- `ls .agent/STOP` → `No such file or directory` (absent).
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty; `git branch
  --show-current` → `feature/f029-subtree-rerun`; `git log --oneline -1` → `aa054d8bb`.
- Block bytes (R-0954): measured 260 lines, sha256
  `daeb11450309f440ce6a46aa07d88f29db743b21451470735077a826c5fdf5ef` — both match the
  delegation message's readings exactly.
- `git worktree list | wc -l` → 61.

**PAYLOADS** — both matched the table exactly:
`booking.diff` 63 lines / 13798 bytes / `ec05f1ab...837ab`; `plan.md` 33 lines / 1197
bytes / `d9564ff2...89acf3ef`.

**G1 TRANSPORT** — each `.agent/authored/f029-r3-*` copy read via `git show
ba2cc9e14:<path>` equals its source byte for byte: block copy 21315 bytes == source
21315 bytes (True); booking.diff copy 13798 == 13798 (True); plan.md copy 1197 == 1197
(True).

**G2 THE BOOKING** — sha256 of each file read via `git show e00da9cb8:<path>` equals
the reviewer's reading exactly:
`.agent/decisions.md` 2290828 bytes, `41fe5d8c...4dd680444` — match.
`.agent/live_review.md` 317154 bytes, `4e36aac1...2a965eaf703` — match.
`.agent/plan.md` 1197 bytes, `d9564ff2...89acf3ef` — match.
`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`'s
text: at `aa054d8b` → `['R-1080']`; at `e00da9cb8` → `['R-1081']` — both match the
reviewer's stated readings.

**G3 THE CODE** —
```
python3 -m ruff check packages/orchestration/subtree_rerun.py apps/cli/commands/job_rerun_cmd.py apps/cli/commands/__init__.py apps/cli/command_catalog.py tests/cli/test_job_rerun_subtree.py tests/orchestration/test_subtree_rerun_prepare.py tests/test_command_catalog.py tests/test_no_orphan_modules.py
```
→ `All checks passed!`, exit 0. `_cmd_rerun_subtree`'s whole body (from `6a195b143`)
and `prepare_subtree_rerun`'s body from `worktrees.create` to its return (from
`427ee8322`) were read and quoted in full during the round; both match what is
committed.

**G4 THE TESTS** — the exact selection, serially, real exit code:
```
python3 -m pytest -q -p no:cacheprovider -rs <the block's 38-file selection> 2>&1 | tail -12
```
→ `1700 passed, 7 skipped` at real exit code 0. The 7 skips are the same F252
quarantine lines round 2 read: 6 in `test_named_bugs.py`'s D3 quarantine block (lines
295, 312, 321, 383, 392, 399) and 1 in `test_agent_tooling.py`'s D12 quarantine (line
43), all carrying the same F252 backlog reason.
Accounting for the difference from 1683: `--collect-only -q` over the two files this
round touched (`tests/cli/test_job_rerun_subtree.py`, new, and
`tests/orchestration/test_subtree_rerun_prepare.py`, grown from 16 to 21 tests) reads
31 nodes total; the round added 31 − 16 = 15 nodes there. 1683 + 15 = 1698, two short
of the actual 1700 — the remaining two are `tests/cli/test_exit_codes.py`'s two
`@pytest.mark.parametrize("entry", CATALOG, ...)` guards, each gaining one node for
the new `job.rerun-subtree` catalog entry (confirmed: no other file in the selection
parametrizes a test over `CATALOG`, the rest only iterate it inside one test body).
Then `python3 -m apps.cli.main integrity check --json` → all 6 checks `pass`,
`fail_count: 0`, `ok: true`.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f029-r3-mut 6a195b143`,
then `python3 -B .agent/authored/f029-r3-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f029-r3-mut`:
```
control (unmutated, first): exit=0 failed=0 nodes=[(none)]
m1 S1 (a) is skipped: exit=1 failed=1 nodes=[...TestR1081Repair::test_occupied_archive_destination_refuses_before_worktree_touched]
m2 S1 (b) never calls retain_for_recovery: exit=1 failed=1 nodes=[...TestR1081Repair::test_a_failing_save_leaves_the_lock_free_and_the_error_propagating]
m3 S2 skips a task without a band...: exit=1 failed=4 nodes=[...TestRerunSubtreeConfirmation::test_a_declined_prompt_changes_nothing, ...test_without_yes_non_tty_is_confirmation_required, ...TestSubtreeRerunCostEstimate::test_a_task_without_a_band_makes_the_whole_estimate_unavailable, ...test_one_xl_task_makes_the_whole_estimate_unavailable]
m4 S2 counts the root task alone: exit=1 failed=3 nodes=[...TestSubtreeRerunCostEstimate::test_a_task_without_a_band_makes_the_whole_estimate_unavailable, ...test_one_xl_task_makes_the_whole_estimate_unavailable, ...test_s_and_m_bands_sum_to_point_four_at_both_bounds]
m5 S3 prepares the rerun after a declined preview: exit=1 failed=1 nodes=[...TestRerunSubtreeConfirmation::test_a_declined_prompt_changes_nothing]
m6 S3 exits 3 for unknown_task: exit=1 failed=1 nodes=[...TestRerunSubtreeRefusalExitCodes::test_unknown_task_exits_2_with_no_preview_printed]
m7 S3 exits 1 for job_running: exit=1 failed=1 nodes=[...TestRerunSubtreeRefusalExitCodes::test_job_running_exits_3]
m8 S3 passes no model to prepare_subtree_rerun: exit=1 failed=2 nodes=[...TestRerunSubtreeJSON::test_model_override_reaches_the_record, ...TestRerunSubtreeRefusalExitCodes::test_model_invalid_exits_2]
m9 S3 passes yes=False to the preview: exit=1 failed=6 nodes=[...TestRerunSubtreeHuman::test_last_line_is_the_run_command, ...TestRerunSubtreeJSON::test_model_override_reaches_the_record, ...test_yes_json_prepares_the_rerun_with_estimate_and_run_command, ...TestRerunSubtreeRefusalExitCodes::test_interleaved_exits_3_with_facts, ...test_job_running_exits_3, ...test_model_invalid_exits_2]
m10 S3 leaves the refusal's facts out of the envelope: exit=1 failed=1 nodes=[...TestRerunSubtreeRefusalExitCodes::test_interleaved_exits_3_with_facts]
restored byte-identical: True
control (unmutated, last): exit=0 failed=0 nodes=[(none)]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every mutation was red on the first run; no repair round was needed. Then
`git worktree remove --force .remedy-wt/f029-r3-mut`, `git worktree prune`;
`git worktree list | wc -l` → 61, matching the step-4 reading.

**Constraint 3** — `git diff --name-only aa054d8b` at the tip before C6b lists exactly
the 16 paths the block's tracked path set names (the 17th, `.agent/handoff.md`, is
this commit); no path outside the set changed.

## Authored-text proofs

`.agent/authored/f029-r3-block.md`, `f029-r3-booking.diff` and `f029-r3-plan.md`
(C1, `ba2cc9e14`): each read back via `git show` equals its source
(`.remedy-wt/f029-r3/block.md`, `.remedy-wt/f029-r3-payloads/booking.diff`,
`.remedy-wt/f029-r3-payloads/plan.md`) byte for byte — see G1 above.
`.agent/authored/f029-r3-mutations.py` (C6a, `b7b1092b5`) is this session's OWN tool,
not reviewer-authored text, so it carries no fidelity comparison; its behavior is
proved instead by G5's live run above.

## Deviations & assumptions

None. Every commit landed as the block ordered it (C1–C6a as named, C6b this one);
no commit was split, reordered or dropped; no existing test was edited; no gate went
red.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 3.

Landed: R-1081 — every exit past `worktrees.create` other than success and a
`SubtreeRerunRefused` now passes through `worktrees.retain_for_recovery` via a
completion flag checked in a `finally`, and the archive destination is checked
before the worktree is ever claimed.

Open findings: 1 (R-1081, landed and awaiting review). Operator questions: 0. After
review, T003 is next: the rerun's run-log event with every reader of its name, the
attempt fan and its popover, the browser's command, and the end-to-end proof.
