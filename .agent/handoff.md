# Handoff — F283 Machine contracts, part two: refusal sweep, JSON gap, exit-code taxonomy · Round 10 · `do --json` one envelope, grouped's parser refusals, `test` group, R-1026

## Session

SESSION 3 of feature F283 · round 10 · rounds so far 10

This round booked round 9's PASS (five commits `d6eda8ea`..`859f883c`, all six gates
PASS, one finding registered), registered R-1026 and recorded DECISIONs F283 D5 and D6.
Then, one commit each: `_cmd_do_order`'s `--json` branch now builds its result document
and answers it in ONE envelope — `emit_ok(**document)` on success, `fail("step_failed",
..., json_output=True, failed_step=last.name, **document)` on a failed walk — resolving
the double-envelope hazard round 9 correctly declined (D5); every parse-level usage
refusal in `apps/cli/grouped.py::main` now asks `_wants_json(raw)` and answers in the
envelope when it holds, at the SAME exit code, through a small shared helper
(`_usage_refusal`) plus two `fail()` calls for the post-parse pairs (D6); the `test`
group's three refusals in `apps/cli/commands/test_cmds.py` moved onto `fail()`; and the
three sites R-1026 named — `job_context_cmd.py::_cmd_job_context`,
`project.py::_cmd_attach_project_job` and `::_cmd_project_adopt` — now pass
`job_not_found` instead of `invalid_job_id`.
Context self-assessment: roughly 96% of the working budget remained at the point this
handoff was written (about 14.4M of 15M tokens).

## Range

Review of `859f883c`..`HEAD`.

## Block self-verification (R-0954)

| reading | measured | given | equal |
|---|---|---|---|
| line count | 240 | 240 | True |
| sha256 | `ac2ab5f6b85401844eb490b82f660dad84dffaa463ad778d6727084d9a5c0a79` | `ac2ab5f6b85401844eb490b82f660dad84dffaa463ad778d6727084d9a5c0a79` | True |

Neither reading differed, so the round went ahead.

## Pre-flight

- `ls .agent/STOP`: `No such file or directory`. No STOP on disk.
- `git status --porcelain`: empty.
- `git branch --show-current`: `feature/f283-machine-contracts-part-two`.
- `git log --oneline -1`: `859f883c`, matching the delegation message.

## Commits

### 1b9f3367 F283 R10 C1: copy round 10 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f283-r10-block.md | +240/-0 | byte-for-byte copy of this round's step block |
| .agent/authored/f283-r10-decisions.md | +62/-0 | byte-for-byte copy of decisions.md |
| .agent/authored/f283-r10-ledger.md | +4/-0 | byte-for-byte copy of ledger.md |
| .agent/authored/f283-r10-plan.md | +39/-0 | byte-for-byte copy of plan.md |

Measured insertions (`git show --numstat`): **345** (240+62+4+39).

### d8b31461 F283 R10 C2: book round 9's PASS, register R-1026, record D5 and D6
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +62/-0 | append decisions.md: DECISIONs F283 D5 and D6 |
| .agent/live_review.md | +4/-0 | append ledger.md by strict byte concatenation: round-9 `Gate:` entry, registration of R-1026 |
| .agent/plan.md | +19/-15 | rewrite to plan.md payload, byte-identical; git's line diff shows only the lines that changed, not the whole file |

Measured insertions (`git show --numstat`): **85** (62+4+19); 15 deletions from the plan.md rewrite.

### 14aabb59 F283 R10 C3: do --json answers in one envelope
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/do_cmd.py | +25/-26 | `emit_ok` imported alongside `fail`; `_cmd_do_order`'s `json_output` branch builds `document` (the same dict, same keys) and, when `ctx.failed`, calls `fail("step_failed", f"{last.name} failed: {last.detail}", json_output=True, failed_step=last.name, **document)` (new token), else `emit_ok(**document)` and returns; the text branch is unchanged and its trailing line becomes `fail("step_failed", ..., json_output=False)`; the NOT-migrated comment is deleted |
| tests/cli/test_do_flags.py | +21/-1 | `test_an_unknown_project_exits_1_with_the_init_step_failed_and_no_mission` repaired to assert an empty stderr and the envelope (`ok` false, `error` `step_failed`, `failed_step` `init`, `message`); added `test_a_successful_do_json_object_carries_schema_version_1_and_ok_true` and `test_a_failed_walk_in_text_mode_still_writes_error_init_failed_on_stderr` |
| tests/cli/test_do_commit_flags.py | +5/-1 | `test_a_push_the_remote_refuses_leaves_the_commit_and_fails_the_walk` repaired the same way (`failed_step` `apply`) |
| tests/cli/test_do_sequence_cli.py | +5/-1 | `test_an_apply_the_baseline_check_refuses_fails_the_walk_naming_the_job` repaired the same way (`failed_step` `apply`) |
| tests/cli/test_job_refusal_envelope.py | +12/-11 | `TestDoRefusalsAreAllMigrated` docstring and assertion updated: NO flagged site remains (`test_no_flagged_print_then_exit_pair_survives`), not one |

Measured insertions: **68** (25+5+21+5+12); 40 deletions.

### 5f8ffc69 F283 R10 C4: parser usage refusals answer in the envelope under --json
| Path | +/- | Reason |
|---|---|---|
| apps/cli/grouped.py | +28/-20 | `emit_error`/`fail` imported at module level (the `_dispatch` local import of `emit_error` removed as redundant); new helper `_usage_refusal(where, token, message, raw, exit_code=2)` — the envelope under `--json`, today's prose otherwise, same exit code; the conflicting-options site, the unknown-group site and the unknown-subcommand site call it; the usage-error-on-a-known-subcommand site answers `missing_argument`/`invalid_argument` inline under `--json` (keeping today's command-help text otherwise); the unrecognized-arguments site calls the helper; the two post-parse pairs become `fail("unknown_command", ...)` and `fail("no_handler", ...)` with `json_output=_wants_json(raw)` |
| tests/cli/test_do_flags.py | +6/-2 | `test_a_flag_removed_from_do_exits_2_and_runs_nothing`'s four parameters repaired to assert exit 2, empty stderr and the envelope (`error` `unrecognized_arguments`), keeping the nothing-was-written assertions |
| tests/cli/test_job_refusal_envelope.py | +21/-0 | `TestGroupedRefusalsAreAllMigrated`: no print-then-exit pair survives in `../grouped.py` |
| tests/test_grouped_cli.py | +49/-0 | `TestParserRefusalsAnswerInTheEnvelopeUnderJson`: unknown subcommand, unrecognized argument, missing positional and the conflicting pair each exit 2 with an empty stderr and one envelope under `--json`; without `--json` the unrecognized-argument stderr is byte-identical to `render_error`'s |

Measured insertions: **104** (28+6+21+49); 22 deletions.

### a50d9715 F283 R10 C5: test group refusals answer through fail()
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/test_cmds.py | +6/-12 | `fail` imported; `_cmd_discover_commands`'s `except Exception` catch-all → `fail("job_store_error", str(exc), json_output=as_json)` (reused, `job.py`'s own token for the identical `require_job_plan` condition); its branched `no_target_repo` site → `fail("no_target_repo", "no target_repo attached.", json_output=as_json, job_id=str(job_id), candidates=[])` (reused, BRANCHED rule); `_cmd_test_status`'s branched `job_not_found` site → `fail("job_not_found", f"No job matches {job_id_str!r}. Try: remedy job list.", json_output=as_json, job_id=job_id_str)` (reused, BRANCHED rule); `_cmd_run_tests` unchanged |
| tests/cli/test_job_refusal_envelope.py | +18/-0 | `TestTestCmdsRefusalsAreAllMigrated`: no print-then-exit pair survives in `test_cmds.py` |
| tests/test_command_discovery.py | +46/-0 | `TestDiscoverNoTargetRepoAnswersInTheEnvelope`: `test discover --json` on a job with no target repo answers one envelope (`no_target_repo`, `job_id`, `candidates` `[]`, empty stderr); text mode stderr reads `Error: no target_repo attached.\n` exactly — the ONE test file judged nearest, chosen because it already exercises `_cmd_discover_commands` directly with a saved `JobPlan` fixture |

Measured insertions: **70** (6+18+46); 12 deletions.

### b492c193 F283 R10 C6: a job the store cannot find answers job_not_found (R-1026)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job_context_cmd.py | +1/-1 | `_cmd_job_context`'s `JobNotFoundError` site: `invalid_job_id` → `job_not_found` (reused, R-1026) |
| apps/cli/commands/project.py | +2/-2 | `_cmd_attach_project_job`'s and `_cmd_project_adopt`'s `JobNotFoundError` sites: `invalid_job_id` → `job_not_found` (reused, R-1026); nothing else changes |
| tests/cli/test_job_context_cmd.py | +25/-0 | `TestJobContextRefusesInTheCallersShape::test_a_job_the_store_cannot_find_answers_job_not_found`: the resolver accepts the id (monkeypatched to identity), `require_job_plan` raises `JobNotFoundError`, answers one envelope with `job_not_found` and an empty stderr |

Measured insertions: **28** (1+2+25); 3 deletions. No `Done:` line written — the reviewer writes it.

### C7 — THE HANDBACK (this commit)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback, written once; a single `.agent/**` state file, exempt from the 500-line cap under DECISION F104 D1 |

Self-reference exception (handback template, R-0149 pattern): a handback cannot
table the commit that writes it.

## External actions

- `git worktree add .remedy-wt/f283-r10-redproof b492c193` for G5 — used for the
  unmutated control and all four mutation red-proofs, then
  `git worktree remove .remedy-wt/f283-r10-redproof --force` — a plain remove
  sufficed because every mutation was reverted by hand back to the original text
  (verified clean with `git status --porcelain` after each revert) before removal.
- `git push origin feature/f283-machine-contracts-part-two` after C7 — real
  outcome reported in the session reply, since it ships this very file.
- `gh pr list --state open ...` after the push — real outcome reported in the
  session reply.
- **NOTHING IS MERGED.** No `gh pr merge`, no `gh pr create`, no checkout of
  `main`, no branch deletion.
- No worktree other than the one disposable G5 worktree was added or removed.
  The three `remedy/job-*` worktrees were left alone throughout.

## Verification

### G1 — PAYLOADS transport, then four authored copies

| file | lines measured/given | bytes measured/given | sha256 equal |
|---|---|---|---|
| decisions.md | 62/62 | 4523/4523 | True |
| ledger.md | 4/4 | 4492/4492 | True |
| plan.md | 39/39 | 1760/1760 | True |

**All readings equal: True.**

Four `.agent/authored/f283-r10-*` copies (the block copy plus three payloads), each
read back from the committed tree with `git show 1b9f3367:<path>` and compared
byte-for-byte with its source:

| copy | bytes | identical to source |
|---|---|---|
| f283-r10-block.md | 16210 | True |
| f283-r10-decisions.md | 4523 | True |
| f283-r10-ledger.md | 4492 | True |
| f283-r10-plan.md | 1760 | True |

**Copies compared: 4. All True.**

### G2 — THE BOOKING

**(a) Append arithmetic**, by strict byte concatenation:

| file | pre (`859f883c`) | payload | post | pre+payload==post |
|---|---|---|---|---|
| .agent/live_review.md | 492157 | 4492 | 496649 | True |
| .agent/decisions.md | 1799308 | 4523 | 1803831 | True |

Matches the reviewer's stated `492157 + ledger.md = 496649` and
`1799308 + decisions.md = 1803831` exactly.

**(b) Line-anchored on the committed ledger**: `^Gate: F283 R9 — ` = **1**;
`^- R-1026 — ` = **1**. Open set by distinct id, via `open_finding_ids` from
`scripts/rotate_live_review.py` (imported and called directly):

| rev | OPEN by distinct id |
|---|---|
| `859f883c` | **22** |
| C2 (`d8b31461`) | **23** |

Added: `['R-1026']`. Removed: `[]`. Matches the reviewer's stated 22 → 23, ADDED
`R-1026`, REMOVED empty, exactly.

**(c) `.agent/plan.md` at C2 equals plan.md byte-for-byte**: sha256-equal to the
payload; committed blob and payload compared directly (both hash equal).

Line count: **39**, under the AGENTS.md 50-line rule.

### G3 — THE CHANGE, COUNTED FROM THE TREE

`git diff --name-only <parent> <commit>` and `git show --numstat` insertions:

| commit | paths changed | insertions |
|---|---|---|
| C3 `d8b31461`→`14aabb59` | apps/cli/commands/do_cmd.py, tests/cli/test_do_commit_flags.py, tests/cli/test_do_flags.py, tests/cli/test_do_sequence_cli.py, tests/cli/test_job_refusal_envelope.py | 68 |
| C4 `14aabb59`→`5f8ffc69` | apps/cli/grouped.py, tests/cli/test_do_flags.py, tests/cli/test_job_refusal_envelope.py, tests/test_grouped_cli.py | 104 |
| C5 `5f8ffc69`→`a50d9715` | apps/cli/commands/test_cmds.py, tests/cli/test_job_refusal_envelope.py, tests/test_command_discovery.py | 70 |
| C6 `a50d9715`→`b492c193` | apps/cli/commands/job_context_cmd.py, apps/cli/commands/project.py, tests/cli/test_job_context_cmd.py | 28 |

At C6, `python3 .remedy-wt/f283-r6-scratch/pairs.py do_cmd.py ../grouped.py test_cmds.py
project.py job_context_cmd.py`:

```
do_cmd.py exits 1 mechanical 0 flagged 0 unflagged 0
   142 _refuse_before_any_step False None
../grouped.py exits 4 mechanical 0 flagged 0 unflagged 0
   456 _usage_refusal False None
   595 _dispatch False None
   519 main False None
   516 main False None
test_cmds.py exits 2 mechanical 0 flagged 0 unflagged 0
   53 _cmd_run_tests False as_json
   46 _cmd_run_tests False as_json
project.py exits 2 mechanical 2 flagged 1 unflagged 1
   345 _cmd_project_current True json_output
   387 _cmd_project_attach_repo True None
job_context_cmd.py exits 0 mechanical 0 flagged 0 unflagged 0
```

Matches the reviewer's stated readings exactly: `do_cmd` `mechanical 0`, `grouped`
`mechanical 0`, `test_cmds` `mechanical 0`, `project` unchanged
(`mechanical 2 flagged 1 unflagged 1` — the two no-prefix
`ProjectNotFoundError`/`InvalidProjectSelectorError` sites the migration rule never
reaches), `job_context` `exits 0`.

`git diff --name-only 859f883c b492c193 -- packages/` prints **nothing** (real
exit code implicit 0, empty stdout) — confirmed `packages/` untouched across the
whole round.

### Token list — every `fail()`/`emit_error()` token C3 to C6 use, its line, new or reused

| commit | line | token | new/reused | search behind a `new` one |
|---|---|---|---|---|
| C3 | 369 | step_failed | new | `grep -rn 'fail("step_failed"\|"step_failed"' apps/cli/ tests/` before this commit: 0 hits anywhere |
| C3 | 388 | step_failed | reused (same commit, L369) | — |
| C4 | 497 | conflicting_options | reused (the hand-written dict this site replaced already used this exact string at `grouped.py:487`, just not through `fail()`/`emit_error()` — DECISION F283 D6 names it "replacing the hand-written object, which lacks `schema_version`") | — |
| C4 | 502 | unknown_command | new | `grep -n '"unknown_command"' apps/cli/**/*.py` before this commit: 0 hits anywhere under `apps/cli/` |
| C4 | 506 | unknown_command | reused (same commit, L502) | — |
| C4 | 512 | missing_argument | reused (`job.py:63` and `worker.py:158` already use this token for "a required argument/flag combination was not given" — the same condition argparse's own "the following arguments are required" message names) | — |
| C4 | 514 | invalid_argument | reused (widely used already — `do_cmd.py`, `job.py`, `mission_cmd.py` — for "the value given for an argument is not one of the allowed ones", the same condition a non-missing usage error names) | — |
| C4 | 540 | unrecognized_arguments | new | `grep -n '"unrecognized_arguments"' apps/cli/**/*.py` before this commit: 0 hits anywhere under `apps/cli/` |
| C4 | 545 | unknown_command | reused (same commit, L502) | — |
| C4 | 550 | no_handler | new | `grep -n '"no_handler"' apps/cli/**/*.py` before this commit: 0 hits anywhere under `apps/cli/` |
| C5 | 105 | job_store_error | reused (`job.py:213` uses it for the identical `require_job_plan`-raises condition) | — |
| C5 | 109 | no_target_repo | reused (`job_context_cmd.py:281`, pre-existing, uses it for the identical "job has no target_repo attached" condition) | — |
| C5 | 206 | job_not_found | reused (`brain.py` and many other modules already use it for the identical `JobNotFoundError`/`require_job_plan` condition) | — |
| C6 | 276 (job_context_cmd.py) | job_not_found | reused (this round's own R-1026 repair; the spelling every other `JobNotFoundError` site in `apps/cli/` already uses) | — |
| C6 | 152 (project.py) | job_not_found | reused (same as above) | — |
| C6 | 433 (project.py) | job_not_found | reused (same as above) | — |

New tokens this round: `step_failed`, `unknown_command`, `unrecognized_arguments`,
`no_handler` — four, each confirmed absent from any `fail("<token>"`/`emit_error("<token>"`/
bare-string search over `apps/cli/` before its introducing commit.

### G4 — TARGETED SELECTION, ruff, integrity

`.remedy-wt/f283-r10-scratch/selection.txt`: **100** space-separated paths (round 9's
selection plus every test file a search for this round's targets found).
`tests/test_command_discovery.py` (C5's named test file) is already in the list —
no separate run needed.

Each reading below was taken with the NOT-YET-COMMITTED-for-this-commit files
stashed away, so it reflects the real state at that exact commit, not the round's
final working tree:

| when | exit code | summary |
|---|---|---|
| after C3 | 0 | 4207 passed, 1 skipped |
| after C4 | 0 | 4213 passed, 1 skipped |
| after C5 | 0 | 4216 passed, 1 skipped |
| after C6 | 0 | 4217 passed, 1 skipped |

Zero failed, zero errors at each; the reviewer read `4205 passed, 1 skipped` at
`859f883c` — the passed count only rose, at every step. `python3 -m ruff check` over
every `.py` path the round touched (`apps/cli/commands/do_cmd.py`,
`apps/cli/commands/job_context_cmd.py`, `apps/cli/commands/project.py`,
`apps/cli/commands/test_cmds.py`, `apps/cli/grouped.py`,
`tests/cli/test_do_commit_flags.py`, `tests/cli/test_do_flags.py`,
`tests/cli/test_do_sequence_cli.py`, `tests/cli/test_job_context_cmd.py`,
`tests/cli/test_job_refusal_envelope.py`, `tests/test_command_discovery.py`,
`tests/test_grouped_cli.py`): **All checks passed!**
`python3 -m apps.cli.main integrity check --json`: `"passed": true, "fail_count": 0`,
all five checks (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `high_blockers_open`) read `"status": "pass"`.

### G5 — RED-PROOFS

Disposable worktree `.remedy-wt/f283-r10-redproof` at `b492c193`, never committed.
Ran the seven test files C3 to C6 touched (`test_do_flags.py`, `test_do_commit_flags.py`,
`test_do_sequence_cli.py`, `test_job_refusal_envelope.py`, `test_grouped_cli.py`,
`test_command_discovery.py`, `test_job_context_cmd.py`).

| step | exit code | result |
|---|---|---|
| unmutated control | 0 | 555 passed |
| (a) `_cmd_do_order`'s `--json` failed-walk branch deleted (the `if ctx.failed: ... emit_ok(**document)` block replaced by a bare `emit_ok(**document); return`) | 1 | `7 failed, 548 passed` — C3's repaired `test_an_unknown_project_exits_1_with_the_init_step_failed_and_no_mission` among them (the target), plus six collateral failures in `test_do_commit_flags.py`/`test_do_sequence_cli.py` whose walks also fail and now reach `emit_ok` instead of the envelope |
| (b) `grouped.py:452`, `_usage_refusal`'s `if _wants_json(raw):` forced to `if False:` | 1 | `7 failed, 548 passed` — the four repaired `test_a_flag_removed_from_do_exits_2_and_runs_nothing` parameters and three of C4's `TestParserRefusalsAnswerInTheEnvelopeUnderJson` tests (`test_conflicting_pair`, `test_unknown_subcommand`, `test_unrecognized_argument`) |
| (c) `test_cmds.py`'s `no_target_repo` site forced to `json_output=False` | 1 | `2 failed, 553 passed` — C5's envelope test (the target, `TestDiscoverNoTargetRepoAnswersInTheEnvelope::test_json_mode_is_one_envelope_with_job_id_and_empty_candidates`) plus one collateral failure in `tests/test_grouped_cli.py::TestGroupedExecution::test_test_discover_json`, which also reads that same refusal's `--json` shape |
| (d) `job_context_cmd.py`'s refusal passes `invalid_job_id` again | 1 | `1 failed, 554 passed` — C6's `test_a_job_the_store_cannot_find_answers_job_not_found` (the target, alone) |

Each mutation was reverted by hand and confirmed clean with `git status --porcelain`
before the next. `git worktree remove .remedy-wt/f283-r10-redproof --force` afterward.
`git worktree list` (post-removal): the primary checkout at `b492c193` plus the three
`remedy/job-*` worktrees — `.remedy-wt/job-468c8e62a2cc4fac`, `.remedy-wt/job-86f628f5e4fb4e0c`,
`.remedy-wt/job-c1dba9c3d7874968` — untouched throughout.

## Deviations & assumptions

1. **The bundle ran C1 through C6 — six commits, exactly as ordered — before
   this handback commit C7.** Nothing was added, dropped or reordered.
2. **No expected insertion figure is given for C2's rewrite or for C3/C4/C5/C6,
   per the block's own convention**: only measured figures are reported above,
   and none of them was forced to match a prediction.
3. **`tests/test_command_discovery.py` was chosen as "the ONE test file C5
   judges nearest"**, over `tests/orchestration/test_test_execution_service.py`
   and others, because it already houses a class
   (`TestDiscoveryRecordsItselfInTheRunLedger`) that exercises
   `_cmd_discover_commands` directly against a saved `JobPlan` fixture, so the
   `no_target_repo` refusal fits the same fixture shape (a job with no
   `target_repo` in its metadata) rather than needing a new harness.
4. **G5 mutations (a) and (b) each reddened more tests than the one the block
   names.** (a) names only C3's repaired unknown-project test as the one that
   "must fail"; deleting the whole failed-walk branch also breaks every OTHER
   test in the selected files whose walk fails under `--json` and now reaches
   `emit_ok` instead of the envelope (six collateral failures in
   `test_do_commit_flags.py` and `test_do_sequence_cli.py`, listed above by
   name). (b) names "C4's `--json` tests and the four repaired parameters";
   forcing `_usage_refusal`'s json branch off also breaks
   `test_conflicting_pair` (uses the same helper for the same reason).
   Reported exactly as measured, not trimmed to the named test alone — R-0485's
   lesson from round 9's own handback.
5. **`apps/cli/grouped.py`'s C4 diff removes one line beyond the block's own
   text**: the local `from apps.cli.json_envelope import emit_error` inside
   `_dispatch` became redundant once `emit_error`/`fail` were imported at
   module level for the new refusal sites, so it was deleted rather than left
   as an unused duplicate. No behavior changed; `_dispatch` still calls
   `emit_error` the same way.
6. **Constraints 1, 3, 4, 6 and 7 held throughout.** No payload was edited or
   retyped; the round's tracked path set is exactly the 19 paths (before this
   commit) constraint 3 enumerates plus `.agent/handoff.md` from this commit
   makes 20 (verified by set-equality below); `packages/` was never touched;
   every commit from C3 on left the targeted G4 selection at zero failed,
   measured against the REAL state at that commit (the not-yet-committed later
   changes were stashed out of the working tree before each reading, then
   restored — see the G4 note above); nothing was merged, no PR created, no
   checkout of `main`; the one G5 worktree was removed as G5's last action and
   the three `remedy/job-*` worktrees were left alone.

### The round's whole tracked path set (before this commit)

`git diff --name-only 859f883c b492c193` — **19** distinct paths
(`tests/cli/test_do_flags.py` touched by both C3 and C4;
`tests/cli/test_job_refusal_envelope.py` touched by C3, C4 and C5 — each counted
once); plus `.agent/handoff.md` from this commit makes **20** — set-equal to
constraint 3's enumeration (4 authored copies + live_review.md + decisions.md +
plan.md + handoff.md + do_cmd.py + grouped.py + test_cmds.py + job_context_cmd.py +
project.py + test_do_flags.py + test_do_commit_flags.py + test_do_sequence_cli.py +
test_job_refusal_envelope.py + test_grouped_cli.py + test_job_context_cmd.py +
test_command_discovery.py, the ONE test file C5 names):

| # | path | introduced by |
|---|---|---|
| 1 | .agent/authored/f283-r10-block.md | C1 `1b9f3367` |
| 2 | .agent/authored/f283-r10-decisions.md | C1 `1b9f3367` |
| 3 | .agent/authored/f283-r10-ledger.md | C1 `1b9f3367` |
| 4 | .agent/authored/f283-r10-plan.md | C1 `1b9f3367` |
| 5 | .agent/decisions.md | C2 `d8b31461` |
| 6 | .agent/live_review.md | C2 `d8b31461` |
| 7 | .agent/plan.md | C2 `d8b31461` |
| 8 | apps/cli/commands/do_cmd.py | C3 `14aabb59` |
| 9 | tests/cli/test_do_commit_flags.py | C3 `14aabb59` |
| 10 | tests/cli/test_do_flags.py | C3 `14aabb59`, touched again by C4 `5f8ffc69` |
| 11 | tests/cli/test_do_sequence_cli.py | C3 `14aabb59` |
| 12 | tests/cli/test_job_refusal_envelope.py | C3 `14aabb59`, touched again by C4 `5f8ffc69` and C5 `a50d9715` |
| 13 | apps/cli/grouped.py | C4 `5f8ffc69` |
| 14 | tests/test_grouped_cli.py | C4 `5f8ffc69` |
| 15 | apps/cli/commands/test_cmds.py | C5 `a50d9715` |
| 16 | tests/test_command_discovery.py | C5 `a50d9715` |
| 17 | apps/cli/commands/job_context_cmd.py | C6 `b492c193` |
| 18 | apps/cli/commands/project.py | C6 `b492c193` |
| 19 | tests/cli/test_job_context_cmd.py | C6 `b492c193` |
| 20 | .agent/handoff.md | C7 (this commit) |

(The table lists 20 rows, one per DISTINCT path — 19 before this commit, 20
after `.agent/handoff.md` lands — matching constraint 3's enumeration exactly;
`test_do_flags.py` and `tests/cli/test_job_refusal_envelope.py` are each one row
even though touched by multiple commits, noted in the "introduced by" column.)

No path outside the enumeration was touched: `.agent/candidates.md`,
`.agent/context.md`, `.agent/operator_questions.md`, `.agent/prose_slips.md`,
`README.md`, `docs/roadmap/**`, and `apps/cli/json_envelope.py` appear **0**
times. `packages/` appears **0** times (confirmed above under G3).

## Authored-text proofs

- The four copies at C1, compared with the reviewer's originals under
  `.remedy-wt/f283-r10-payloads/` and `.remedy-wt/f283-r10-block.md`: **four
  readings, all True** (G1).
- The one REWRITE payload against its committed file: `.agent/plan.md`'s
  committed sha256 equals the payload's sha256 (G2c).
- The two APPEND payloads against their committed files: strict byte
  concatenation True for `.agent/live_review.md` (ledger.md) and
  `.agent/decisions.md` (decisions.md), byte numbers equal to the reviewer's
  (G2a).
- No payload was edited or retyped. All four `.agent/authored/` copies and the
  one product-file rewrite were made with `shutil.copyfile`; the two appends by
  reading each payload's bytes and writing base+payload back to disk.
- Every change under `apps/` and `tests/` this round was WORKER-authored to the
  block's SPEC — there is no reviewer-authored diff to compare against for those
  files; the block's SPEC prose is the standard they were written to, and
  G3/G4/G5 above are the proof they meet it.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| Pre-flight (STOP, git state, block self-verify) | done | no STOP; tree clean at `859f883c`; block 240 lines / matching sha256 |
| C1 copy block + 3 payloads | done | 345 insertions |
| C2 book round 9 PASS, register R-1026, record D5/D6 | done | 85 insertions (62+4+19, 15 deletions from plan rewrite); open set 22→23, added R-1026 |
| C3 do --json answers in one envelope | done | 68 insertions; `step_failed` (new) used at both the failure and success paths of `_cmd_do_order`'s `--json` branch |
| C4 parser usage refusals answer in the envelope under --json | done | 104 insertions; `_usage_refusal` helper plus two direct `fail()` calls; four new tokens, four reused |
| C5 test group refusals answer through fail() | done | 70 insertions; three sites migrated, `_cmd_run_tests` left alone |
| C6 R-1026: job the store cannot find answers job_not_found | done | 28 insertions; three sites' token corrected, one test added |
| C7 the handback | done | this commit |
| G1 payload transport + authored copies | done | 3/3 payload readings equal; 4/4 authored copies byte-identical |
| G2(a) live_review.md + decisions.md append | done | 492157+4492=496649; 1799308+4523=1803831 |
| G2(b) R-1026 registration pairing + open set by distinct id | done | 1 Gate line, 1 R-1026 line; 22→23, added R-1026, removed none |
| G2(c) plan.md rewrite | done | sha256-equal to payload; 39 lines, under 50 |
| G3 change counted from the tree | done | per-commit diffs and insertions reported; `pairs.py` matches at C6; 0 paths under `packages/` |
| G4 targeted selection, ruff, integrity | done | 4207/4213/4216/4217 passed, 0 failed/errors at each (up from 4205); ruff exit 0; integrity all 5 pass, fail_count 0 |
| G5 red-proofs (a)(b)(c)(d) | done | all four go RED, each including the named target test, three with honestly-reported collateral failures; unmutated control 555 passed |
| G6 tree, push, PR list | pending at write time | reported in the worker's session reply with real exit codes |
| Constraint 1 no payload edited/retyped | done | `shutil.copyfile`, byte concatenation only |
| Constraint 2 every commit under 500 insertions | done | 345, 85, 68, 104, 70, 28; this handoff exempt as single `.agent/**` state file |
| Constraint 3 no unnamed file touched | done | 19 paths before this commit (20 after), set-equal to the enumeration |
| Constraint 4 G4 selection at zero failed after every commit | done | 4207/4213/4216/4217 passed, measured against the real per-commit state (later changes stashed out before each reading) |
| Constraint 5 STOP if a gate goes red outside constraint 3's path set | done (n/a) | no gate went red outside the named paths; no STOP was needed |
| Constraint 6 nothing is merged | done | no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion |
| Constraint 7 G5 worktree under .remedy-wt/, removed, listed | done | `.remedy-wt/f283-r10-redproof`, removed as G5's last action, `git worktree list` reported after; the three `remedy/job-*` worktrees untouched |

## Next

1. Phase 1 rule 1: read `.agent/STOP` from disk.
2. The review of round 10 — C1 through C7, with all six gates re-derived.
3. Then the tail of the refusal sweep as `.agent/plan.md` lists it: `patch`,
   `config`, `real_test_execution`, `ui`, `self`, `decision`, `snapshot`,
   `worker_facade`, the cost-preview confirmation, the `stats`, `bench`,
   `failure_stats` and `job stop` `SystemExit` sites, and the unprefixed
   refusals of `--json` handlers; then `runtime_cmd.py` as its own round.

Open findings count: **23**. Operator-questions count: **2**.
