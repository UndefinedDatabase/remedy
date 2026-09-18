# Handoff — F268 remedy do: the one-command start · Round 8 (DECISION F268 D16, R-0933) — STOPPED before C3

## Session

SESSION 2 of feature F268 · round 8 · rounds so far 8

## Range

Review of 3c18ade2..HEAD — branch `feature/f268-remedy-do`.

## Summary

The round landed C1 (bookkeeping), C2 (D16 clauses (4) to (7): `--project`, the budget flags, `--builder-model`, `--reviewer-model`, `--planner-model`) and two repair commits for reds that C2 caused. It STOPPED BEFORE C3 under constraint 3. With C3's production change applied as a dry run in the working tree, `tests/orchestration/test_autorun.py::TestCalcFixtureBuilderWithProof::test_no_ui_suppresses_ui` goes red. That test is not on C3's list, and only the deleted routing can satisfy it. Its body calls `COMMAND_HANDLERS["do.run"]` with `ui = "true"`, `no_ui = True` and `_cmd_do` patched, then asserts `kwargs["enable_ui"] is False`. D16 (2) deletes `--ui` from the handler and the dispatch lambda, so the kwarg no longer exists and the test fails with `KeyError: 'enable_ui'`. The dry-run edits were reverted by exact path (`git checkout -- apps/cli/grouped.py apps/cli/commands/do_cmd.py apps/cli/command_catalog.py`). No C3 commit exists, and R-0933 stays OPEN.

- **C2, the SPEC as built.** `DoContext` gains `project_selector`, `budgets` (a dict, set only when a budget flag was given), `builder_model`, `reviewer_model` and `planner_model`. `_cmd_do_order` validates the two role models with `_validate_role_override` and resolves the budget flags with `resolve_job_budgets(cli_…, project_root=repo)` before `walk_do_sequence`. An error prints `Error: <reason> Nothing was run.` and exits 2. `_step_init` with a selector calls `select_project(selector, root)`. On `ProjectNotFoundError` or `InvalidProjectSelectorError` it returns DO_STEP_FAILED with `no project matches --project '<selector>'; list them with: remedy project list`. On success its detail is `project <slug> (<id>) selected by --project`. The repository root is still resolved from `--repo`, and the ignore entries are still written. `_step_run` passes `builder_model=`, `reviewer_model=` and `budgets=` to `run_job`. `_provider_flags` is renamed `_job_run_role_flags` and appends `--builder-model`/`--reviewer-model` (each `shlex.quote`d) after the provider flags on every `remedy job run` Next line. `--planner-model` reaches `model=` of `_step_plan`'s `make_structured_call_fn(MissionPlanDraft, …)` and of `plan_order_job`'s task-plan call `make_structured_call_fn(TaskPlan, …)`. It also reaches the intake call: with a planner model, `plan_order_job` builds `make_structured_call_fn(JobIntake, model=planner_model)` directly instead of `make_provider_call_fn()`, which takes no model and which four tests outside the change set patch. `plan_order_job` gains a `planner_model` keyword. The catalog `do.run` entry and the parser get the three model flags. `--planner-model` parses through the generic `else` branch of `_add_command_args`; the other two have branches of their own.
- **C2, a routing bridge (see Deviations).** C2 alone would leave its own tests on the autorun path, because every new flag makes the invocation non-bare. So C2 adds `--project`, the three model flags and the five budget flags to `_BARE_ALLOWED`/`_BARE_VALUED`, and passes them through `_cmd_do`'s truly-bare branch. C3 deletes the whole detection.
- **Measured with C3's production change applied (dry run, reverted).** The change deleted the truly-bare block and `_did_inject` in `grouped.py`, plus the three `_add_command_args` branches for `--max-cycles`, `--autonomy-level` and `--ui`, which no other command declares; `--dry-run` stays, because `job.apply` and one other entry declare it. It deleted the four ArgDefs, changed `--no-ui`'s help to `Do not open the cockpit for the job that ran`, and reduced `_cmd_do` to the not-yet-available refusal plus `_cmd_do_order(...)`. The dispatch lambda lost `autonomy_level`, `max_cycles`, `injected_default`, `truly_bare`, `enable_ui` and `dry_run`. The patch is kept as scratch at `.remedy-wt/f268-r8/c3_production_dryrun.patch`, sha256 `813ff65ac6ca806022d214e3ed18daa1cb5ab2716b1cb85cf7339b258f8539a8`. The G2 list, plus every test file that names `_cmd_do`, `do.run`, `truly_bare` or a `["do", …]` argv (19 files, plus `tests/cli/test_quick_start.py`, `tests/orchestration/test_import_reachability.py` and `tests/docs/`), read `14 failed, 896 passed, 1 skipped`:
  - on C3's list: `test_golden_path.py::TestDoMission::test_explicit_do_run_skips_golden_path`, `::test_budget_flag_skips_golden_path`, `test_job_commands.py::TestDoDirectGoalCommandRewrite::test_do_direct_dry_run`, `::test_do_run_alias_still_works`, `::test_do_with_all_flags`, `test_cli_execution_loop_closure.py::TestDoProviderCliParsing::test_default_command_rewrite` (the `truly_bare` line), and the three `TestUiBooleanFlagParsing` tests;
  - fixed by C3's docs rewrite: `test_advertised_commands.py::test_every_operator_facing_advertised_flag_is_declared_by_its_command` (`docs/guides/autocoder-usage.md:22`, `:97`, `docs/guides/do-run-v1.md:19`) and `test_do_cmd_summary.py::TestDocsCommandContract::test_docs_do_commands_valid`;
  - red because of C2, repaired in C2b: `tests/docs/test_vocabulary.py::test_every_binding_word_in_a_description_carries_the_pages_meaning`;
  - red at base `3c18ade2` already (see below): `test_job_commands.py::TestRemedyDo::test_do_command_in_catalog`;
  - **THE STOP:** `tests/orchestration/test_autorun.py::TestCalcFixtureBuilderWithProof::test_no_ui_suppresses_ui`.
- **Two more facts for C3, measured and not acted on.**
  - (1) `scripts/remedy_smoke.sh:1928`, section `12ao. Repair-loop fixture E2E`, runs `remedy do "Make tests pass" --repo "${TMP_REPAIR}" --autonomy-level 6 --max-cycles 3 --no-ui --json` and checks the autorun JSON (`version == 1`, the repair loop). Rewriting that line to the sequence's flags leaves a section that tests the deleted autorun, so C3's docs rule cannot be met by a rewrite alone. `tests/test_cli_execution_loop_closure.py::TestSmokeScriptNewCliSections::test_smoke_has_repair_loop_section` pins `repair-loop` and `12ao` in the script.
  - (2) Two of the three `test_job_commands.py` tests the block lists, `TestRemedyDo::test_dry_run_no_side_effects` and `::test_dry_run_phases_by_autonomy`, call `autorun.dry_run_autorun` directly. They pin no routing and no flag, and they stayed green under the dry run, so they need nothing in this round; they leave with `dry_run_autorun` in the next round.
- **A red at base.** `tests/cli/test_job_commands.py::TestRemedyDo::test_do_command_in_catalog` asserts `cmd.may_mutate_repo is False`, but the `do.run` entry declares `may_mutate_repo=True` at `3c18ade2` (R-0969, round 5). Run from a clean worktree at `3c18ade2`, the file read `1 failed, 19 passed`. This red is why G2 reads `1 failed`. It was not repaired: it sits in the autorun `TestRemedyDo` class, whose fate is the next deletion round's, and the fix is a reviewer call (flip the pin to `True`, or delete it with the class).

## Commits

### 93f42233 F268 R8 C1: bookkeeping — book round 7's verdict, record DECISION F268 D16 and operator question Q3, round 8 plan and payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r8-block.md` | +127 / -0 | Byte copy of the step block |
| `.agent/authored/f268-r8-decisions.md` | +33 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r8-ledger.md` | +2 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r8-opq.md` | +10 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r8-plan.md` | +26 / -0 | Byte copy of the payload |
| `.agent/decisions.md` | +33 / -0 | `git show 3c18ade2:` bytes + decisions.md (DECISION F268 D16) |
| `.agent/live_review.md` | +2 / -0 | `git show 3c18ade2:` bytes + ledger.md (Gate: F268 R7, PASS) |
| `.agent/operator_questions.md` | +10 / -0 | `git show 3c18ade2:` bytes + opq.md (Q3) |
| `.agent/plan.md` | +8 / -8 | := plan.md payload |

### 38668454 F268 R8 C2: DECISION F268 D16 clauses 4 to 7 — remedy do honours --project, the budget flags and the builder, reviewer and planner model flags; tests in test_do_flags
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +3 / -0 | `--builder-model`, `--reviewer-model`, `--planner-model` on `do.run` |
| `apps/cli/commands/do_cmd.py` | +56 / -2 | `_cmd_do_order`: model validation, budget resolution before the walk, the new `DoContext` fields; `_cmd_do` and the dispatch lambda pass the flags through |
| `apps/cli/grouped.py` | +8 / -2 | Routing bridge: the new flags keep `do "<order>"` on the sequence (deleted with the detection in C3) |
| `packages/orchestration/do_sequence.py` | +55 / -15 | `DoContext` fields; `_step_init` selector; `_step_run` budgets/models; `_job_run_role_flags`; `planner_model` through `_step_plan`, `_step_shape`, `plan_order_job` |
| `tests/cli/test_do_flags.py` | +200 / -0 | New: six tests of D16 (4) to (7) |

### 146635ce F268 R8 C2b: repair — the builder and reviewer model flag descriptions carry the vocabulary page's meaning of their binding word
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/command_catalog.py` | +2 / -2 | "of every job" → "on every task": `job` in a description must carry `mission`/`budget`/`fence`/`task` (`tests/docs/test_vocabulary.py`) |

### deac5e74 F268 R8 C2c: repair — the golden-path budget flag test, named for rewrite by round 8, asserts the sequence runs, as C2's routing makes it
| Path | +/- | Reason |
|------|-----|--------|
| `tests/cli/test_golden_path.py` | +4 / -4 | `test_budget_flag_skips_golden_path` → `test_budget_flag_walks_the_do_sequence`: asserts `"[done] shape:" in result.stdout`; the old test asserted it absent |

### C3 — not made
Stopped under constraint 3 (see Summary). No commit.

### (this commit) F268 R8 C4: handoff — round 8, stopped before C3
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This document (self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f268-r8-g5 deac5e74` inside `.remedy-wt/f268-r8/g5.py` (G5); removed by the same script with `git worktree remove --force` on that path.
- `git worktree add -q --detach .remedy-wt/f268-r8-base 3c18ade2` (the base reading of `test_job_commands.py`); removed with `git worktree remove --force` on that exact path. `git worktree list` then read one row.
- Working-tree dry run of C3's production change, saved as a patch under `.remedy-wt/f268-r8/` and then reverted with `git checkout --` on the three exact paths.
- `git push` after this commit (no force); outcome and G6 in the round report.
- No PR create, edit or merge.

## Verification

All runs at `deac5e74`, the last code commit. C4 changes only `.agent/handoff.md`.

- G1 `python3 .remedy-wt/f268-r8/g1.py`, reading from HEAD:
  - `ledger.md scratch True authored True`, and the same line for `decisions.md`, `plan.md`, `opq.md` and `block.md`;
  - `.agent/live_review.md True`, `.agent/decisions.md True`, `.agent/operator_questions.md True` (each equals the `3c18ade2` bytes plus the payload);
  - `.agent/plan.md True`.
- G2 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_do_flags.py tests/cli/test_do_sequence_cli.py tests/cli/test_golden_path.py tests/cli/test_job_commands.py tests/test_cli_execution_loop_closure.py tests/cli/test_cli_ux.py tests/cli/test_quick_start.py tests/cli/test_advertised_commands.py tests/cli/test_do_cmd_summary.py tests/test_command_catalog.py tests/orchestration/test_do_run.py tests/cli/test_do_evidence_package.py tests/orchestration/test_import_reachability.py tests/docs/` (output to `.remedy-wt/f268-r8/g2.log`) → `EXIT-NONZERO`, `FAILED tests/cli/test_job_commands.py::TestRemedyDo::test_do_command_in_catalog`, `1 failed, 683 passed in 79.56s (0:01:19)`. This is the red that was already there at base (see Summary). The round's other edited test file is `tests/cli/test_golden_path.py`, which is in the list.
  - A wider run at `deac5e74` (the G2 list plus `test_do_runtime.py`, `test_autorun.py`, `test_mission_cmd.py`, `test_plan_approval.py`, `test_scoped_listings.py`, `test_dead_command_check.py`, `test_provider_mode.py`, `test_install_smoke.py` and `test_role_override_flags.py`) read `3 failed, 951 passed, 1 skipped`. That run came before C2b and C2c: two of the three reds are the ones those commits repaired, and the third is the red at base.
- G3 `python3 .remedy-wt/f268-r8/g3.py 3c18ade2 deac5e74` (tracked files read through `git ls-tree`/`git show`):
  - `3c18ade2 code reading 13 docs reading 5`;
  - `deac5e74 code reading 13 docs reading 5`.
  - The code hits are `apps/cli/commands/do_cmd.py` (5), `apps/cli/grouped.py` (7) and `tests/test_cli_execution_loop_closure.py:73`. The docs hits are `docs/guides/autocoder-usage.md:22`, `:47`, `:97`, `docs/guides/do-run-v1.md:19` and `scripts/remedy_smoke.sh:1928`.
  - Both readings stay non-zero because C3 was not made; the second reading's required 0 is NOT met.
- G4 `python3 -m ruff check apps/cli/command_catalog.py apps/cli/commands/do_cmd.py apps/cli/grouped.py packages/orchestration/do_sequence.py tests/cli/test_do_flags.py tests/cli/test_golden_path.py` → `All checks passed!` (the six `.py` files `git diff --name-only 3c18ade2 deac5e74` names).
- G5 `python3 .remedy-wt/f268-r8/g5.py`. One worktree at `deac5e74` ran `python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_do_flags.py` from its root, with `__pycache__` purged before each run. Each mutation replaced one single-occurrence string (count asserted 1) in `packages/orchestration/do_sequence.py`, was reverted by writing the original bytes back, and was followed by `git status --porcelain` reading empty:
  - imported path: `/home/decodeux/Repos/remedy/.remedy-wt/f268-r8-g5/packages/orchestration/do_sequence.py`.
  - control → `exit 0`, `6 passed in 3.41s`.
  - (a) `budgets=ctx.budgets)` → `)` → `exit 1`, `FAILED …::test_max_total_tokens_is_the_jobs_recorded_budget`, `1 failed, 5 passed`.
  - (b) `if ctx.project_selector is not None:` → `if False:` → `exit 1`, `FAILED …::test_project_of_a_project_init_registered_walks_and_the_job_is_that_projects` and `FAILED …::test_an_unknown_project_exits_1_with_the_init_step_failed_and_no_mission`, `2 failed, 4 passed`.
  - (c) `builder_model=ctx.builder_model,` (whole line) → removed → `exit 1`, `FAILED …::test_builder_and_reviewer_models_are_the_jobs_cli_models_and_on_the_next_line`, `1 failed, 5 passed`.
  - (d) `call_fn = make_structured_call_fn(MissionPlanDraft, model=ctx.planner_model)` → `call_fn = make_structured_call_fn(MissionPlanDraft)` → `exit 1`, `FAILED …::test_planner_model_reaches_every_structured_planner_call`, `1 failed, 5 passed`.
  - `git worktree list`: one row before and one row after. `remedy/job-*` branch count: 31 before and 31 after.
- G6 (clean tree, local tip == origin) runs after the push; it is in the round report.

## Authored-text proofs

Four payloads and the block were verified by sha256 before use and again in G1: `ledger.md` `d33becb6…5207`, `decisions.md` `ed8c331e…4cf9`, `plan.md` `b8b046bd…0cd`, `opq.md` `04536a0f…11b1`, `block.md` `f8049655…065b`. Each was copied byte-exact to `.agent/authored/f268-r8-<name>`. G1 prints every copy identical, the three appends equal to their `git show 3c18ade2:` bytes plus the payload, and `.agent/plan.md` equal to plan.md. The block's own copy is `.agent/authored/f268-r8-block.md`, sha256 `f8049655c3971ba6a5482cf2e90e2a878a52f4ad470dbd922380d3a380ef065b`.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `93f42233` |
| C2 D16 (4) to (7) | done | `38668454`; red under G5 (a), (b), (c), (d) |
| C2b repair (vocabulary) | done | `146635ce`, a red C2 caused |
| C2c repair (golden-path budget test) | done | `deac5e74`, a C3-listed rewrite that C2's routing had already made red |
| C3 D16 (1) to (3), R-0933 | skipped | Constraint 3: `tests/orchestration/test_autorun.py::TestCalcFixtureBuilderWithProof::test_no_ui_suppresses_ui` is outside C3's list, and only the deleted `--ui` routing can satisfy it |
| C4 handoff | done | This commit |

No `Landed:` line: R-0933 did not land. Resolving it needs D16 (1) (every `do` walks the sequence) together with the explicit-`do run` test, and both belong to C3.

## Open findings

126 open by distinct id, derived with `.remedy-wt/f268-r4/count.py`: HEAD has 140 registrations and 14 `Done:` ids, unchanged from round 7. C1 booked a verdict and no `Done:`. This round opens no finding. R-0933 and R-0892 stay open.

## Deviations & assumptions

- **Commit sequence.** The block ordered C1, C2, C3, C4. The round ran C1, C2, C2b, C2c and C4, and made no C3 (the constraint 3 stop). C2b and C2c are repair commits under constraint 3's repair clause, each for a red caused by C2. C2c is also one of the three golden-path rewrites C3 names; it was made early because C2's routing bridge had already made it red.
- **C2's routing bridge.** The block puts D16 (4) to (7) in C2 and the routing deletion in C3. Without the bridge, every C2 test would have been routed to autorun at C2's tip, because each new flag made the invocation non-bare. The bridge adds the new flags to the bare-flag lists that C3 deletes. It is the reason the golden-path budget test went red at C2.
- **Test strengthening beyond the letter of C2.**
  - The `--project` test registers the project with `remedy init` in a SECOND repository, so a walk that ignored the selector would register the target instead; that is why G5 (b) turns both `--project` tests red. It also asserts the target stays unregistered.
  - The planner-model test runs with `--plan-only` and asserts that both `MissionPlanDraft` and `JobIntake` calls are recorded, beside "every call is `p1`".
  - The budget error message adds ` Nothing was run.`, which the invalid-budget test asserts.
- **`InvalidProjectSelectorError`.** `select_project` raises it for an empty selector, and it is not a `ProjectNotFoundError` subclass. `_step_init` fails the step on either.
- **Exit codes.** The shell guard refuses `$?`, so G2 ends in `&& echo EXIT-0 || echo EXIT-NONZERO`, and G5 prints each pytest `returncode` from Python. G1, G3 and G5 ran from script files under `.remedy-wt/f268-r8/`.
- **Full suite** not run (amend0917-throughput).

## Next

Reviewer: rule on the stop, then re-issue C3 with the three facts measured above:

1. Delete or rewrite `tests/orchestration/test_autorun.py::TestCalcFixtureBuilderWithProof::test_no_ui_suppresses_ui`, which only `--ui` can satisfy.
2. `scripts/remedy_smoke.sh` section `12ao` exercises the autorun. Decide whether it and `test_smoke_has_repair_loop_section` go now or with the autorun deletion round.
3. `test_do_command_in_catalog` is red at base.

The C3 production dry-run patch is in `.remedy-wt/f268-r8/` (digest above). Book round 8's verdict in the next round's first commit.
