# Handoff — F268 remedy do: the one-command start · Round 6 (R-0892 + T005)

## Session

SESSION 1 of feature F268 · round 6 · rounds so far 6

## Range

Review of 68cf6a13..HEAD — branch `feature/f268-remedy-do`.

## Summary

The round landed C1 and R-0892's code-and-test half (C2, C2b, C2c). It STOPPED before C3 (T005) under constraint 4, because DECISION F268 D14's test premise does not hold at this base. It also could not make the SKILL.md edit that R-0892's fix clause asks for, because the permission system refuses writes under `.claude/`.

- **C2 (D13, R-0892).** `export_job_evidence` ends by writing four files: `agent_run_trace.jsonl`, `agent_run_trace_summary.json`, `command_transcript.json` and `job_flow.json`, in that order. They are written after the final `manifest.json`, so every other file already exists.
  - The trace heirs `do job-flow`'s reconstruction (`70c78773^:apps/cli/commands/do_cmd.py` `_build_agent_run_trace`). It is built with `agent_run_trace.create_trace_event` from the job's run records, the exported `task_runs/<id>/prompt_trace.jsonl` and any exported F004 streams. The summary comes from `build_trace_summary`.
  - Providers come from the job's `execution_config`. The deleted promote dry-run event has no heir, because no export runs one.
  - `job_flow.json` carries:
    - `job_id`;
    - `final_audit.status` = `final_verifier_report.json`'s `verdict`, or null when there is none;
    - `final_audit.missing_observability_artifacts`, computed against the manifest script's required root and task lists over the written package;
    - `target_guard.mutated_target` = `target_guard.json`'s `target_mutated`, with the key absent when that value is not a boolean.
  - `command_transcript.json` lists only commands the records show ran: a round whose `test_passed` is not None (the job's `test_command`, with the exit code parsed from `exit=<n>`), and each `verification_tests.json` run. Otherwise it is an empty list with a `reason`. It keeps `do job-flow`'s per-command field names; start and finish times are null because nothing records them.
  - A manual-only completion, as the script defines it, gets none of the four. The script marks them `not_applicable_manual_completion` for exactly that package, and `test_manual_completion_bundle.py` pins this.
- **Measured before writing (block C2), at `56779fae`:** a fake-provider `do` job exported with `export_job_evidence` and checked with `validate_evidence_candidate` gave `is_valid_current_run: false`. The only errors were `missing root artifact:` for `job_flow.json`, `agent_run_trace.jsonl`, `agent_run_trace_summary.json` and `command_transcript.json`. `required_task_artifacts` was `{}`, so no per-task artifact was missing, and `final_verifier_report.json` read `BLOCKED`.
- **C3 not built. The blocker, measured at this base:** the block orders "a test that runs the five lines in order, as printed, … with the fake builder and reviewer selected through that repository's own `remedy.toml` role configuration". No such configuration exists.
  - `pingpong_job.default_role_provider_name` (`pingpong_job.py:1876-1894`) calls `role_config.resolve_role_config(role)` with no `config_file`.
  - `_resolve_cfg` (`:1897-1903`) knows only the sources `cli`, `persisted` and `default`.
  - The only production `config_file=` caller in `packages/` and `apps/` is `teacher_model.py:182`.
  - `config.py` registers no builder or reviewer provider key, and no `BUILDER_PROVIDER` environment variable is read.
  - So an unflagged `remedy do "Write a CONTRIBUTING.md" --no-ui` records builder `ollama` from source `default`.
  - Also, without `--no-llm`, the plan and shape steps call `intake.make_structured_call_fn`, which is Ollama-only and probes a live Ollama client (`intake.py:280-326`). The study step does the same through `study.study_call_fn`.
  - So the lines D14 prescribes (no provider flag, no `--no-llm`) cannot be run as printed in a test without a real-provider probe (constraint 3), or without first adding a config-file route for role providers. That change is in `role_config.py` and `pingpong_job.py`, outside the change set, and it changes D14's premise.
  - Per constraint 4 (a red that touches a DECISION → stop and report), `_QUICK_START`, the README Quickstart and their pinning tests are untouched.

## Commits

### 56779fae F268 R6 C1: book round 5's PASS, resolve R-0968 and R-0969; DECISIONs F268 D13 and D14; plan
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f268-r6-block.md` | +99 / -0 | Byte copy of the step block |
| `.agent/authored/f268-r6-decisions.md` | +31 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r6-ledger.md` | +6 / -0 | Byte copy of the payload |
| `.agent/authored/f268-r6-plan.md` | +26 / -0 | Byte copy of the payload |
| `.agent/decisions.md` | +31 / -0 | `git show 68cf6a13:` bytes + decisions.md (append) |
| `.agent/live_review.md` | +6 / -0 | `git show 68cf6a13:` bytes + ledger.md (append) |
| `.agent/plan.md` | +9 / -11 | := plan.md payload |

### 21391dc3 F268 R6 C2: job evidence writes job_flow.json, the agent run trace and its summary, and command_transcript.json from the job's own records (DECISION F268 D13, R-0892)
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/job_evidence.py` | +328 / -0 | The call after the final `manifest.json` write. The mirrored lists `REVIEW_REQUIRED_ROOT_ARTIFACTS`, `REVIEW_REQUIRED_TASK_ARTIFACTS` and `REVIEW_MANUAL_REPAIR_EXEMPT_ARTIFACTS`. The functions `_read_export_json`, `_exported_prompt_trace_index`, `_build_job_agent_run_trace`, `_executed_job_commands`, `_missing_review_artifacts`, `_is_manual_only_completion` and `_write_job_flow_artifacts` |

### d1dbce3b F268 R6 C2b: a fake-provider do job's exported evidence passes the review-package check; its final audit status is the verifier's verdict
| Path | +/- | Reason |
|------|-----|--------|
| `tests/cli/test_do_evidence_package.py` | +180 / -0 | New: validity (`is_valid_current_run` True, no `missing root artifact` and no `task_runs/…: missing`); status equals the verifier's verdict, forced to `PASS` and `NEEDS_TESTS` (parametrized) and unforced; trace rounds against the run record; empty transcript with its reason; one verification command in the transcript; the mirrored lists equal to the script's own |

### ab848190 F268 R6 C2c: the trace builder's docstring drops the retired promote word the docs guard refuses
| Path | +/- | Reason |
|------|-----|--------|
| `packages/orchestration/job_evidence.py` | +1 / -1 | G3 repair: `tests/docs/test_retired_promote_word.py::test_no_file_outside_the_map_carries_the_word` failed on C2's docstring ("promote dry-run" → "dry-run apply") |

### (this commit) F268 R6 C4: handoff — round 6
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This document (self-reference exception) |

### Pre-existing tests edited, one line each

None. C3's pinning-test updates (`TestQuickStart`, the quick-start assertions in `tests/test_cli_execution_loop_closure.py`, `tests/cli/test_advertised_commands.py`) were not made, because C3 stopped.

## External actions

- Measurement probe: the new test file's first draft was a `test_probe` that printed the validation result. It was replaced by the real tests before C2b and never committed.
- G5: `git worktree add --detach .remedy-wt/f268-r6/g5-wt HEAD` (at `ab848190`), removed with `git worktree remove --force` (exit 0). `git worktree list` showed only the main checkout before and after.
- `git push` after this commit (no force). The outcome and G6 are in the round report.
- No PR create, edit or merge.

## Verification

All runs at `ab848190`, except where a line says otherwise. C4 changes only this file.

- G1 (`.remedy-wt/f268-r6/g1.py`) → `REAL_EXIT=0`:
  - `digest ledger.md True authored-copy-identical True`, and the same for `decisions.md`, `plan.md` and `block.md`.
  - `live_review append True`, `decisions append True`.
  - `cmp .agent/plan.md .remedy-wt/f268-r6/plan.md` → `CMP_EXIT=0`.
- G2 `python3 -m pytest -q -p no:cacheprovider` over the block's nine files plus `tests/cli/test_do_evidence_package.py` (all ten exist) → `439 passed in 97.68s (0:01:37)`, `REAL_EXIT=0`. The first run, at `d1dbce3b`, also read `439 passed`.
- G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py`:
  - at `d1dbce3b`: `1 failed, 456 passed in 6.81s`, `REAL_EXIT=1`, failing `tests/docs/test_retired_promote_word.py::test_no_file_outside_the_map_carries_the_word` on `packages/orchestration/job_evidence.py`;
  - repaired in C2c, then `457 passed in 6.75s`, `REAL_EXIT=0`.
- G4 `python3 -m ruff check packages/orchestration/job_evidence.py tests/cli/test_do_evidence_package.py` → `All checks passed!`, `RUFF_EXIT=0`.
- G5 (`.remedy-wt/f268-r6/g5.py`), one worktree at `ab848190`:
  - Each run went from the worktree root with `python3 -B -m pytest -q -p no:cacheprovider tests/cli/test_do_evidence_package.py`. `__pycache__` was purged before each run (0 found each time), and each run printed `/home/decodeux/Repos/remedy/.remedy-wt/f268-r6/g5-wt/packages/orchestration/job_evidence.py`.
  - Each mutation was a single-occurrence replacement, reverted with `git checkout --` and confirmed by an empty `git status --porcelain`.
  - control → `8 passed in 7.50s`, `EXIT=0`.
  - (a) `write_json("job_flow.json", {` → `(lambda *a, **k: None)("job_flow.json", {` → `4 failed, 4 passed`, `EXIT=1`. Failing: `test_a_do_jobs_exported_evidence_passes_the_review_package_check`, `test_job_flow_final_audit_status_is_the_exports_own_verifier_verdict[PASS]`, `[NEEDS_TESTS]` and `test_the_unforced_verdict_reaches_job_flow_and_the_manifest_check`.
  - (b) `"status": final_status,` → `"status": "BLOCKED",` → `2 failed, 6 passed`, `EXIT=1`. Failing: `test_job_flow_final_audit_status_is_the_exports_own_verifier_verdict[PASS]` and `[NEEDS_TESTS]`. The unforced test stays green under (b), because the fake run's own verdict is `BLOCKED`; this is why the forced two-verdict test exists.
  - (c) not run, because C3 did not land.
  - The `remedy/job-*` branch count was 31 before and 31 after.
- Wider regression check (not a block gate), at `d1dbce3b`, over every test file that references the export, the flow artifacts or `job evidence`: 37 files, among them `test_manual_completion_bundle.py`, `test_repair_attest.py`, `test_review_*`, `test_run_manifest*`, `test_token_ledger.py` and `test_observability_index.py` → `1160 passed in 139.05s`.
  - Its first run, before the manual-completion rule and the absent-key rule, read `3 failed` in `test_manual_completion_bundle.py`. Those were fixed in C2 before it was committed.
- G6 (clean tree, HEAD == origin) runs after the push. It is in the round report.

## Authored-text proofs

The four payloads were verified by sha256 before use (`block.md` `0a7471aa…43f3`, `ledger.md` `12b5edbe…8c`, `decisions.md` `ffcd3f6e…ea`, `plan.md` `dfdfa702…c4`). They were copied byte-exact to `.agent/authored/f268-r6-*`, and G1 prints each copy identical. Both appends were built from `git show 68cf6a13:` bytes plus the payload, and G1 proves the committed bytes.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `56779fae` |
| R-0892 (C2) | deviated | Code and test landed (C2, C2b, C2c), red under G5 (a) and (b). The SKILL.md half is not done: writes under `.claude/` are refused by the permission system |
| T005 (C3) | skipped | Stopped under constraint 4: D14's test premise (role providers from the fixture's `remedy.toml`) does not exist at this base; see Summary |
| C4 handoff | done | This commit |

Landed: R-0892 (except its SKILL.md half) — `export_job_evidence` writes `job_flow.json`, `agent_run_trace.jsonl`, `agent_run_trace_summary.json` and `command_transcript.json` from the job's own records (DECISION F268 D13). A fake-provider `remedy do` job's export passes `scripts/build_review_manifest.py`'s `validate_evidence_candidate` with `is_valid_current_run` True, and `job_flow.json`'s `final_audit.status` equals the export's own verifier verdict: `test_a_do_jobs_exported_evidence_passes_the_review_package_check` and `test_job_flow_final_audit_status_is_the_exports_own_verifier_verdict` in `tests/cli/test_do_evidence_package.py` (C2, C2b, C2c). Not landed: `.claude/skills/remedy-evidence-review/SKILL.md` still names `apps/cli/commands/do_cmd.py` `_build_final_audit()` (line 21) and a `promote_ready` field (lines 26, 52, 71) that the heir does not write.

## Open findings

126 open by distinct id, derived with `.remedy-wt/f268-r4/count.py`: HEAD has 140 registrations and 14 `Done:` ids. Against round 5's 128, C1 booked R-0968 and R-0969 as `Done:`. This round opens no finding.

## Deviations & assumptions

- **Commit sequence.** The block ordered C1, C2, C3, C4. The round ran C1, C2, C2b, C2c, C4:
  - C2 was split into C2 (production, +328) and C2b (tests, +180), because together they were over 500 insertions (constraint 1).
  - C2c is the G3 repair in its own commit (constraint 4).
  - C3 was not made (stop, above).
- **The SKILL.md edit (R-0892's fix clause) is not made.** The Edit tool's write to `.claude/skills/remedy-evidence-review/SKILL.md` was refused by the permission system. I did not route around the refusal with a shell write. The intended edit:
  - line 21 → `packages/orchestration/job_evidence.py` — `_write_job_flow_artifacts()` writes `job_flow.json`, whose `final_audit.status` is the export's own `final_verifier_report.json` verdict (DECISION F268 D13; heir of the deleted `do_cmd.py` `_build_final_audit()`);
  - line 26 `(job_id, final_audit, promote_ready)` → `(job_id, final_audit, target_guard)`;
  - line 52 → its verdict is `final_audit.status` in job_flow.json;
  - line 71 → a manual-only completion has none of the four; the manifest marks them not applicable.
  - This needs the operator to grant the write, or to make the edit.
- **The required lists are mirrored, not imported.** D13 says missing artifacts are "computed against the manifest script's own required lists". `scripts/` is not in the wheel (`pyproject.toml` `packages = ["packages", "apps"]`) and no `packages/` module imports from it. So the three lists are copied into `job_evidence.py`, and `test_the_mirrored_required_lists_equal_the_manifest_scripts_own` pins them equal to `REQUIRED_ROOT_ARTIFACTS`, `REQUIRED_TASK_ARTIFACTS` and `MANUAL_REPAIR_EXEMPT_ARTIFACTS`.
- **Manual-only completion writes none of the four.** D13 does not name this case. Writing them failed `test_manifest_accepts_manual_completion`, which asserts all four are `not_applicable_manual_completion`, and `test_observability_index_manual_completion`. Those files have no provider-flow source in that package. The test copies the script's `_is_manual_completion` rule.
- **`target_guard.mutated_target` is absent, not null, when there is no boolean source.** D13 allows "absent or null". `_job_flow_shape_problems` rejects a present non-boolean, so the key is left out.
- **Transcript shape.** The deleted writer described one `do job-flow` invocation. D13 asks for a list of executed commands in that shape, so each entry keeps its `command_id`, `argv_safe`, `exit_code`, `stderr_ref`, `started_at` and `finished_at`, plus `task_id`, `run_id` and `round` or `duration_seconds`, and a `source`. The top level keeps `final_audit`, `target_repo_mutated` and `target_guard`. Fields with no record (hashes before and after, `promote_ready`, the argv of the `do` call itself) are not written.
- **The trace keeps `do job-flow`'s event kinds except two.** `job_flow_started` is dropped, because no job-flow command ran. `promotion_dry_run_completed` is dropped, because no dry run is performed. `final_audit_completed` carries the verifier's verdict and is omitted when there is no verdict.
- **Plan.** `.agent/plan.md` is the payload, byte-exact (G1). AGENTS.md "If Blocked" asks for the blocker in `plan.md`. Following round 5's precedent, it is recorded here instead, because G1 checks `plan.md` byte-for-byte and C4 is scoped to the handoff.
- **Full suite** not run (amend0917-throughput).

## Next

Reviewer: review round 6 at this branch tip and book its verdict. Then rule on T005: either a DECISION that adds a `remedy.toml` role-provider route (`role_config` `config_file` wired into `default_role_provider_name` and the planner/study calls), or a D14 amendment that lets the quick-start lines carry `--builder-provider`/`--reviewer-provider`/`--no-llm`. Also grant or make the SKILL.md edit.
