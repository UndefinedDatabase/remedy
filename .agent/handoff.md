# Handoff — F268 remedy do: the one-command start · Round 9 (DECISION F268 D16 (1) to (3), D17, R-0933)

## Session

SESSION 2 of feature F268 · round 9 · rounds so far 9

## Range

Review of 5243e0a6..HEAD — branch `feature/f268-remedy-do`.

## Summary

Round 9 landed round 8's C3. Every `remedy do`, with or without the word `run`, now walks the F268 sequence. The bare-flag detection in `grouped.py`, the autorun branch of `_cmd_do` and the four flags only that branch read (`--autonomy-level`, `--max-cycles`, `--ui`, `--dry-run`) are gone from `do`. Smoke section `12ao` now runs the `do` sequence end to end, as DECISION F268 D17 (2) orders. The G2 list reads `1039 passed, 1 skipped`, and both G3 readings are 0 at the last code commit.

- **C2 production, built from round 8's patch** (`.remedy-wt/f268-r8/c3_production_dryrun.patch`, digest matched, applied cleanly with `git apply -3` at `0bac38f0`). The block ordered two changes to it:
  - `--no-ui`'s help is now `Do not open the cockpit`. The word `job` is gone, and `tests/docs/test_vocabulary.py` passes.
  - `--project`'s help is now `Select a registered project by slug or id instead of the repository's own` (D16 (4)).
  - `_cmd_do` now does two things: it refuses the not-yet-available flags, then calls `_cmd_do_order(...)`. Its docstring records the deliberate absence of a second route. The dispatch lambda no longer passes `autonomy_level`, `max_cycles`, `injected_default`, `truly_bare`, `enable_ui` or `dry_run`.
  - The `--dry-run` parser branch in `grouped.py` stays, because other commands still declare it. The `--max-cycles`, `--autonomy-level` and `--ui` branches are deleted.
- **C3 tests and smoke:**
  - (a) and (b): the deletions and rewrites below;
  - (c): smoke `12ao` rewritten, and `REPAIR_JOB_ID` renamed `DO_JOB_ID` at all three uses;
  - (d): the four docs lines;
  - (e): two new tests in `tests/cli/test_do_flags.py`, one of them parametrized four ways.
- **C3b repair:** `tests/docs/test_named_source_paths.py::test_every_source_path_an_operator_facing_page_names_exists` went red after C3. `docs/guides/do-run-v1.md:133` still named the deleted `tests/cli/test_do_runtime.py`. C3b deletes that line; the path is in the change set.

### Tests deleted BY DESIGN (C3 (a)), each checked against its body first

| Test | Reason |
|------|--------|
| `tests/cli/test_do_runtime.py` (whole file: `TestDoRuntime`, `TestDoRuntimeText`, `TestDoRuntimeTruth`, 14 tests) | Every test runs `do … --autonomy-level N` or `--max-cycles 0` and asserts the autorun's JSON (`stop_reason`, `autonomy_capped`, `run_contract`, …). D16 (1) and (2) delete both the flags and that route |
| `tests/cli/test_job_commands.py::TestDoDirectGoalCommandRewrite::test_do_direct_dry_run` | Parses `do "<goal>" --dry-run`; `--dry-run` left `do` (D16 (2)) |
| `…::test_do_run_alias_still_works` | Parses `do run "<goal>" --dry-run`; same reason. The explicit `do run` routing is now pinned by the new `test_do_flags` test and the rewritten golden-path test |
| `…::test_do_with_all_flags` | Passes `--autonomy-level 4 --max-cycles 2`, both of which left `do` |
| `tests/test_cli_execution_loop_closure.py::TestUiBooleanFlagParsing::test_ui_bare_flag_parses` | Asserts `args.ui is True`; `--ui` left `do` |
| `…::test_no_ui_suppresses` | Asserts `args.ui` beside `args.no_ui`; same reason |
| `…::test_enable_ui_logic` | Asserts the `enable_ui` handler kwarg, which is deleted with `--ui` |
| `tests/orchestration/test_autorun.py::TestCalcFixtureBuilderWithProof::test_no_ui_suppresses_ui` | D17 (1): asserts `kwargs["enable_ui"] is False`, and that kwarg left with `--ui`. Its now-unused `patch` import left with it (ruff F401) |

### Tests rewritten BY DESIGN (C3 (b)) — none asserts less

| Test | Before → after |
|------|----------------|
| `tests/cli/test_golden_path.py::TestDoMission::test_explicit_do_run_skips_golden_path` → `test_explicit_do_run_walks_the_do_sequence` | Before: `] shape:` absent from stdout. After: `do run "<order>"` with `--no-llm`, the fake roles and `--no-ui`; asserts exit 0 and `[done] shape:` in stdout |
| `…::test_explicit_default_flag_skips_golden_path` → `test_explicit_default_flag_walks_the_do_sequence` | Before: `--autonomy-level 1` (the flag's default) kept `] shape:` out of stdout. After: `--repo .` (that flag's default, given explicitly); asserts exit 0 and `[done] shape:`. `--autonomy-level` itself left `do` and is pinned to exit 2 by `test_do_flags` |
| `tests/test_cli_execution_loop_closure.py::TestDoProviderCliParsing::test_default_command_rewrite` | Only the `truly_bare` assertion is dropped; the docstring says "the one route" instead of "the bare sequence route" |
| `tests/cli/test_job_commands.py::TestRemedyDo::test_do_command_in_catalog` | `may_mutate_repo is False` → `is True` (R-0969's value, D17 (3)); this was the red at base |
| `tests/test_cli_execution_loop_closure.py::TestSmokeScriptNewCliSections::test_smoke_has_repair_loop_section` → `test_smoke_has_do_sequence_section` | Before: `repair-loop` and `12ao` somewhere in the script. After: `_SMOKE_SECTION="12ao"` exists; the section's single `remedy do "` line carries `--no-llm`, `--builder-provider fake` and `--reviewer-provider fake`; `--autonomy-level` appears nowhere in the script; the section sets `DO_JOB_ID=` |

### Tests added (C3 (e)), in `tests/cli/test_do_flags.py`

- `test_an_explicit_do_run_walks_the_sequence_and_its_job_has_the_cli_builder` (R-0933):
  - the argv is `main(["do", "run", ORDER, --builder-provider fake, --reviewer-provider fake, --no-llm, --no-ui, --json])`;
  - it asserts `mission_id`, `steps` is a list whose first five names are `init study plan shape run`, and the run step is `done`;
  - the job's `execution_config` records `(builder, builder_source) == ("fake", "cli")`, and the same for the reviewer. The default source is `default`, so the `cli` source is what tells the two apart.
- `test_a_flag_removed_from_do_exits_2_and_runs_nothing[autonomy-level|max-cycles|ui|dry-run]`:
  - each flag, given to `remedy do "<order>"`, exits 2;
  - stdout is empty, no job plan exists, and the repository stays unregistered.

## Commits

### 0bac38f0 F268 R9 C1: bookkeeping — book round 8's verdict, record DECISION F268 D17, round 9 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r9-block.md` | +115 / -0 | Byte copy of the step block |
| `.agent/authored/f268-r9-decisions.md` | +21 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r9-ledger.md` | +2 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r9-plan.md` | +26 / -0 | Byte copy of the payload |
| `.agent/decisions.md` | +21 / -0 | `git show 5243e0a6:` bytes + decisions.md (DECISION F268 D17) |
| `.agent/live_review.md` | +2 / -0 | `git show 5243e0a6:` bytes + ledger.md (Gate: F268 R8, PASS) |
| `.agent/plan.md` | +6 / -6 | := plan.md payload |

### 3bfddd48 F268 R9 C2: DECISION F268 D16 clauses 1 and 2 — every remedy do walks the sequence; the autorun branch and the autonomy, cycles, ui and dry-run flags leave do
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +2 / -6 | Four ArgDefs deleted; `--no-ui` and `--project` help rewritten |
| `apps/cli/commands/do_cmd.py` | +17 / -120 | `_cmd_do`'s autorun branch and parameters deleted; it always calls `_cmd_do_order`; the dispatch lambda loses six kwargs |
| `apps/cli/grouped.py` | +0 / -43 | Truly-bare detection, `_did_inject`, and the `--max-cycles`, `--autonomy-level` and `--ui` parser branches deleted |

### 3f745d30 F268 R9 C3: tests and smoke — the autorun routing's tests leave, the golden-path and catalog pins follow D16 and D17, smoke 12ao runs the do sequence, R-0933's explicit do run test
| Path | +/- | Reason |
|------|-----|--------|
| `docs/guides/autocoder-usage.md` | +5 / -6 | Lines 22, 47–50 and 97 at `5243e0a6`: only flags `do` still has; the R-0933 paragraph now says every `do` walks one sequence |
| `docs/guides/do-run-v1.md` | +1 / -1 | Line 19: `--autonomy-level 3` dropped |
| `scripts/remedy_smoke.sh` | +25 / -34 | `12ao` is now a `do` sequence run on a one-commit fixture (D17 (2)); `REPAIR_JOB_ID` becomes `DO_JOB_ID` (three uses) |
| `tests/cli/test_do_flags.py` | +37 / -1 | Two new tests (five cases); module docstring |
| `tests/cli/test_do_runtime.py` | +0 / -348 | Deleted (C3 (a)) |
| `tests/cli/test_golden_path.py` | +16 / -9 | Two rewrites (C3 (b)) |
| `tests/cli/test_job_commands.py` | +2 / -36 | Three deletions; catalog pin True |
| `tests/orchestration/test_autorun.py` | +1 / -22 | `test_no_ui_suppresses_ui` deleted; unused `patch` import dropped |
| `tests/test_cli_execution_loop_closure.py` | +13 / -35 | Three deletions, one assertion dropped, smoke pin rewritten |

### 6e909f13 F268 R9 C3b: repair — the do run v1 guide no longer names the deleted runtime test file
| Path | +/- | Reason |
|------|-----|--------|
| `docs/guides/do-run-v1.md` | +0 / -1 | `tests/docs/test_named_source_paths.py` was red on line 133, `tests/cli/test_do_runtime.py` |

### (this commit) F268 R9 C4: handoff — round 9
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This document (self-reference exception) |

## External actions

- `git worktree add -q --detach .remedy-wt/f268-r9-g5 6e909f13`, run from `.remedy-wt/f268-r9/g5b.py` (G5 (b)). The same script removed it with `git worktree remove --force` on that exact path, in a `finally`.
- `git push` after this commit (no force); the outcome and G6 are in the round report.
- No PR was created, edited or merged.

## Verification

All gates ran at `6e909f13`, the last code commit; C4 changes only `.agent/handoff.md`.

- **G1** `python3 .remedy-wt/f268-r9/g1.py` (reads HEAD through `git show`):
  - `ledger.md digest True authored True`; `decisions.md digest True authored True`; `plan.md digest True authored True`; `block.md digest True authored True`;
  - `.agent/live_review.md True`; `.agent/decisions.md True`;
  - `.agent/plan.md True`.
- **G2** the block's list, exactly (output in `.remedy-wt/f268-r9/g2.log`):
  - `EXIT-0`, `1039 passed, 1 skipped in 146.60s (0:02:26)`.
  - Before C3b, the same list read `1 failed, 1038 passed, 1 skipped`. The one failure was `tests/docs/test_named_source_paths.py::test_every_source_path_an_operator_facing_page_names_exists` (`docs/guides/do-run-v1.md:133: tests/cli/test_do_runtime.py`).
  - At C2's tip, the list plus `tests/cli/test_do_runtime.py` read `23 failed, 1032 passed, 1 skipped`. Every failure was on C3's lists or was one of the two docs reds C3 (d) fixes.
- **G3** `python3 .remedy-wt/f268-r8/g3.py 5243e0a6 6e909f13`:
  - `5243e0a6 code reading 13 docs reading 5`, with the 13 code hits and 5 docs hits round 8 listed;
  - `6e909f13 code reading 0 docs reading 0`.
  - `REPAIR_JOB_ID` in `scripts/remedy_smoke.sh`: `git grep -c` reads `5243e0a6:scripts/remedy_smoke.sh:3` and finds no match at `6e909f13` (0).
- **G4** `python3 -m ruff check` over the eight `.py` files that `git diff --name-only --diff-filter=d 5243e0a6 6e909f13 -- '*.py'` names (`apps/cli/command_catalog.py`, `apps/cli/commands/do_cmd.py`, `apps/cli/grouped.py`, `tests/cli/test_do_flags.py`, `tests/cli/test_golden_path.py`, `tests/cli/test_job_commands.py`, `tests/orchestration/test_autorun.py`, `tests/test_cli_execution_loop_closure.py`) → `All checks passed!`.
- **G5 (a)** `python3 .remedy-wt/f268-r9/g5a.py`:
  - The script builds a one-commit fixture under `.remedy-wt/f268-r9/g5a/` and sets `REMEDY_DATA_DIR` in its own `os.environ`. It extracts each command from `git show HEAD:scripts/remedy_smoke.sh` with its variable substituted and runs it through `[sys.executable, "-m", "apps.cli.grouped", …]`.
  - `12ao argv: ['remedy', 'do', 'Make tests pass', '--repo', '<fixture>', '--builder-provider', 'fake', '--reviewer-provider', 'fake', '--no-llm', '--no-ui', '--json']` → `12ao remedy do exit 0`.
  - 12ao's own JSON checker (extra) → `exit 0`, `do sequence: OK (jobs=1, stopped before apply)`.
  - `DO_JOB_ID 66dc4e4282c54b64`; `12aq remedy memory candidates exit 0 version 1`.
  - 12as UX gate checker via `[sys.executable, "-c", …]` → `exit 0`, `UX smoke gate: OK (story=5 journey items, checklist=2 items)`.
- **G5 (b)** `python3 .remedy-wt/f268-r9/g5b.py 6e909f13`. One worktree at `.remedy-wt/f268-r9-g5` ran `python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_do_flags.py` from its root, with `__pycache__` purged before each run:
  - imported `do_cmd.py`: `/home/decodeux/Repos/remedy/.remedy-wt/f268-r9-g5/apps/cli/commands/do_cmd.py`;
  - control → `exit 0`, `11 passed in 4.33s`;
  - mutation: `ArgDef("--dry-run", "Show the plan's tasks without executing", …)` re-added to the `do.run` entry. The parser handling is `grouped.py`'s existing `--dry-run` store_true branch, asserted present once. The worktree's `git status` read `M apps/cli/command_catalog.py`. Result: `exit 1`, `FAILED tests/cli/test_do_flags.py::test_a_flag_removed_from_do_exits_2_and_runs_nothing[dry-run]`, `1 failed, 10 passed in 5.29s`;
  - `git worktree list`: 1 row before and 1 row after. `remedy/job-*` branches: 31 before and 31 after.
- **G6** (clean tree, local tip == origin) runs after the push; it is in the round report.
- **Full suite** not run (amend0917-throughput).

## Authored-text proofs

- Three payloads and the block matched their sha256 before use: `ledger.md` `4431cb8a…25ac`, `decisions.md` `5d4ace05…9708`, `plan.md` `c858f184…0906`, `block.md` `e7ec7bec…d3f8`. The same holds for round 8's patch, `813ff65a…39a8`.
- Each was copied byte-exact to `.agent/authored/f268-r9-<name>`.
- G1 shows, reading HEAD: every copy is identical; both appends equal their `git show 5243e0a6:` bytes plus the payload; `.agent/plan.md` equals plan.md.
- `.agent/authored/f268-r9-block.md` sha256: `e7ec7bec1b0a2e2977b3de7e4f9a1c25c4c3846433e8e1c8c02179cb7fd0d3f8`.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `0bac38f0` |
| C2 D16 (1), (2) production | done | `3bfddd48` |
| C3 tests, smoke, docs | done | `3f745d30`; red under G5 (b) |
| C3b repair (named source path) | done | `6e909f13`, a red C3's file deletion caused |
| C4 handoff | done | This commit |
| R-0933 | done | Landed (see below) |

Landed: R-0933 — every `remedy do`, including an explicit `remedy do run "<order>"`, walks the sequence, and its `--builder-provider` is the job's recorded builder with source `cli` (`3bfddd48`, test `tests/cli/test_do_flags.py::test_an_explicit_do_run_walks_the_sequence_and_its_job_has_the_cli_builder` in `3f745d30`).

## Open findings

126 open by distinct id, derived with `.remedy-wt/f268-r4/count.py`: HEAD has 140 registrations and 14 `Done:` ids, the same as round 8. C1 booked a verdict and no `Done:`. This round opens no finding. R-0933 carries a `Landed:` line in this handoff only.

## Deviations & assumptions

- **Commit sequence.** The block ordered C1, C2, C3 and C4. The round ran C1, C2, C3, C3b and C4. C3b is a repair commit under constraint 3's repair clause, for a red that C3's deletion of `tests/cli/test_do_runtime.py` caused. That test's own message asks for the reference to be repaired "in the same commit as the file". Constraint 3 orders a commit of its own, and the block wins, so C3 alone leaves that one docs test red until C3b.
- **Two test renames.** Round 9's rewrites renamed three tests to say what they now assert: `…_skips_golden_path` → `…_walks_the_do_sequence` (twice) and `test_smoke_has_repair_loop_section` → `test_smoke_has_do_sequence_section`.
- **`test_explicit_default_flag_…`.** Its old flag, `--autonomy-level`, no longer exists, so "the sequence runs" is shown with `--repo .`, another flag given explicitly at its default. The removed flag's exit 2 is pinned in `test_do_flags`.
- **Smoke `12ao` checks.** Only the three that D17 (2) names: JSON with `mission_id`, non-empty `job_ids`, `stopped_before_apply` true. The autorun section's raw-leak scan and its `version`/`cycles_run`/repair fields are gone with the autorun JSON. The fixture holds one committed `README.md`. The variables were renamed `TMP_DO` and `_DO_OUTPUT`.
- **Docs held to the lines the block named.** `docs/guides/do-run-v1.md` lines 24–27 still list `--autonomy-level`, `--max-cycles` and `--dry-run` under "Flags:", and `docs/guides/autocoder-usage.md:153` and `:161` still name `--max-cycles`. Neither is on a `remedy do` line, so G3 does not see them, and the block did not name them. They describe `run_do`'s v1 flow, which leaves in the next deletion round. Two more stale texts were also left untouched: the 12aq comment "Repair loop should have created at least one candidate" and the 12as message "after repair loop".
- **`do.run`'s description** (`Start a controlled autorun for a goal.`) and `do_cmd.py`'s module docstring still say "autorun". The block did not name them; they are left for the deletion round.
- **Exit codes.** The shell guard refuses `$?`, so G2 ends in `&& echo EXIT-0 || echo EXIT-NONZERO`, and G5 prints each `returncode` from Python. G1 and G5 ran from script files under `.remedy-wt/f268-r9/`.

## Next

Reviewer: review round 9 and book its verdict in round 10's first commit. Then run the deletion round of the plan's Next Steps (2): `run_do`, `export_do_run_json`, `summarize_do_run` and `dry_run_autorun` have no caller since round 9 and leave with their tests, together with the stale texts named under Deviations.
