# Handoff — F047 Checkpoint & resume, Integration Gate

Branch: feature/f047-checkpoint-resume · PR #153 (draft)
Base: main @ 89c4ef0e723f89c58956de3964d1653461d273b9
Gate range: `72fc653..4692cca` · Feature range: `89c4ef0..4692cca`
Open findings: 0 · **Zero unexplained branch-only failures.**
Next expected action: reviewer gate verdict, then closure.
Only the reviewer may claim the gate verdict; this is the worker's evidence.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| [A] persist round-2 verdict | done | own commit 9cbfbf9, first action |
| [B] full suite on branch | done | 3 runs, raw below |
| [C] full suite on base 89c4ef0 | done | worktree, raw below; worktree removed |
| [D] compare + serial re-runs | done | 2 genuine failures found and fixed |
| [E] canary | done | 42 passed |

## External actions taken

| Action | Detail |
|--------|--------|
| Pushed branch | `git push` → `72fc653..4692cca` |
| Worktree add/remove | `git worktree add <scratch>/base89 89c4ef0`, then `git worktree remove --force` — `git worktree list` is clean (one entry) |

No PR update this round (description already covers T001–T003 + R-0146).
No closure artifacts: no evidence bundle, no zip, no STATUS edit.

## Commits this round

**9cbfbf9** chore(f047): persist the round-2 reviewer verdict; open the integration gate

| File | +/- |
|------|-----|
| .agent/live_review.md | +19 / −2 |
| .agent/plan.md | +7 / −8 |

**4692cca** chore(f047): live_review.md gains its Steps section (gate parity)

| File | +/- |
|------|-----|
| .agent/decisions.md | +17 / −0 |
| .agent/live_review.md | +9 / −0 |

## [B] Full suite on the BRANCH (raw)

    $ python3 -m pytest -n auto -q
    run 1 (pre-fix):  196 failed, 14028 passed,  9 skipped             in 189.64s
    run 2 (pre-fix):  177 failed, 14046 passed,  8 skipped, 3 errors   in 162.22s
    run 3 (post-fix): 158 failed, 14065 passed,  8 skipped, 2 errors   in 158.32s

Three runs of the SAME tree differ by ~38 failures. That is the known
F135/F052 xdist nondeterminism (F046's gate saw the same churn); it is why
every branch-only id below was re-run serially rather than argued about.
Run 1 was used as the comparison set; run 3 is post-fix.

## [C] Full suite on the BASE 89c4ef0 (raw)

    $ git worktree add <scratch>/base89 89c4ef0
    $ (cd <scratch>/base89 && python3 -m pytest -n auto -q)
    190 failed, 13947 passed, 14 skipped, 3 errors in 143.21s

## [D] Comparison

Unique failing node ids: branch run 1 = 197, base = 195.
Set difference: **40 branch-only**, 38 base-only — churn in BOTH directions,
which is itself the flake signature.

### Serial re-run of all 39 branch-only node ids (raw)

    $ python3 -m pytest -q <39 node ids>
    2 failed, 37 passed in 5.67s

(The 40th line was stray stderr — `ERROR: '/tmp/pytest-of-decodeux/…/myrepo'
is not a git repository.` — not a test id. Its base counterpart appears in
the base-only list with a different pytest tmp path, so it is the same
worker-scoped noise on both sides.)

**37 of 39 passed serially → xdist flakes, not regressions.** They cluster in
`tests/regression/test_named_bugs.py` (smoke-script structure checks),
`tests/runtimes/test_supervisor_portability.py`,
`tests/runtimes/test_runtime_cli_process_boundary.py`,
`tests/orchestration/test_test_runner.py` and `tests/cli/test_runtime_cmd.py`
— all process/port/tmpdir-contending suites, none touching F047 code.

### The 2 genuine, reproducible branch-only failures

    tests/orchestration/test_test_runner.py::TestNoBroadExceptAndDegradedSignals::test_live_review_has_steps_section
    tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs::test_live_review_has_steps_section

Both assert `"Steps" in .agent/live_review.md`. F047-attributable, and the
cause is in a file this feature authored — so fixed in-round per the gate
rules. The base passed them **by accident**: F046's live_review.md happened
to contain the substring inside prose, in the sentence about plan.md missing
its "## Next Steps" section. The F047 rewrite legitimately dropped that
sentence and with it the token.

Fix (commit 4692cca): live_review.md now carries a real `## Steps` section
listing the feature's rounds and ranges. The reviewer-authored finding and
verdict text is untouched — the section is purely additive. **Neither test
was modified**; the contract is met, not weakened. Same class as F046's
plan.md "## Next Steps" repair at its own gate. Recorded in decisions.md.

    $ python3 -m pytest <the 2 node ids> -q
    2 passed in 0.11s                                              exit 0

### After the fix

    branch-only failures (run 3 vs base): 6
      tests/runtimes/test_supervisor_portability.py::TestDeniedCwdPortability::test_a_wrong_readable_cwd_is_still_a_mismatch
      tests/runtimes/test_supervisor_portability.py::TestLiveApplicationOwnership::test_the_real_supervised_app_is_a_child_of_its_supervisor
      tests/test_data_paths.py::TestResolveDataRoot::test_default_ends_with_data
      tests/test_grouped_cli.py::TestGroupedExecution::test_brain_graph_json
      tests/test_grouped_cli.py::TestGroupedExecution::test_policy_contract_json
      tests/test_grouped_cli.py::TestGroupedExecution::test_policy_token_json

    $ python3 -m pytest -q <those 6 node ids>
    6 passed in 2.10s                                              exit 0

All six pass serially — a different six from run 1's flake set, which is the
point. **Zero unexplained branch-only failures.**

### Known classes — parity confirmed on BOTH sides, nothing touched

14 catalog/discovery failures, all present on branch AND base:

    tests/cli/test_do_cmd_summary.py::TestDocsCommandContract::test_docs_remedy_commands_catalog_valid
    tests/orchestration/test_event_replay.py::TestDocsExist::test_resume_docs_commands_catalog_valid
    tests/orchestration/test_project_summary.py::TestProjectBrainDocs::test_docs_commands_catalog_valid
    tests/test_command_catalog.py::TestCatalogClassification::test_every_command_has_action_class
    tests/test_command_catalog.py::TestCatalogClassification::test_mutating_commands_flagged
    tests/test_command_catalog.py::TestCatalogSensitivity::test_no_sensitive_terms_in_arg_help
    tests/test_command_discovery.py::TestCLIDiscoverCommandsSchemaV1::test_json_has_counts
    tests/test_command_discovery.py::TestCLIDiscoverCommandsSchemaV1::test_json_has_selected_test_candidate
    tests/test_command_discovery.py::TestCLIDiscoverCommandsSchemaV1::test_json_has_version_1
    tests/test_command_discovery.py::TestCLIDiscoverCommandsSchemaV1::test_json_output_is_pure_json
    tests/test_command_discovery.py::TestCLIDiscoverCommands::test_json_candidates_argv_is_list
    tests/test_command_discovery.py::TestCLIDiscoverCommands::test_json_candidates_have_required_keys
    tests/test_command_discovery.py::TestCLIDiscoverCommands::test_json_output_is_pure_json
    tests/test_command_discovery.py::TestCLIDiscoverCommands::test_text_output_does_not_crash

4 `.agent` contract failures, all present on branch AND base:

    tests/orchestration/test_test_runner.py::TestNoBroadExceptAndDegradedSignals::test_context_md_updated
    tests/orchestration/test_test_runner.py::TestNoBroadExceptAndDegradedSignals::test_plan_md_current
    tests/ui_server/test_dashboard_contract.py::TestAgentStateFilesCurrentBranch::test_context_md_references_current_branch
    tests/ui_server/test_dashboard_contract.py::TestLiveReviewAndAgentStateRefs::test_context_md_no_stale_steps

Deliberately not swept up — pre-existing on both sides and out of scope.

## [E] Canary (raw)

    $ python3 -m pytest tests/cli/test_golden_path.py -q
    42 passed in 19.02s                                            exit 0

## F047's own suites in the branch full run

None of `test_checkpoints.py`, `test_resume_cli.py`, `test_resume_kill.py` or
`test_long_run_executor.py` appears in the branch failure set — 128 tests,
green under `-n auto` as well as serially.

## Notes for the reviewer

- Zero F047-attributable regressions remain. The one real finding this gate
  produced was in an F047 state file, was fixed by meeting the contract (not
  by editing the test), and is documented in decisions.md.
- `git worktree list` shows exactly one entry (the main checkout).
- No closure artifacts built, per the round constraints.
- Docs still deferred to closure: `remedy job resume` gained two behaviors
  (F047 mode, `--dry-run` preview); `docs/resume.md` does not exist and its
  two tests are pre-existing red on both sides.
