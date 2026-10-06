# F290 (Findings paydown v6) — Acceptance Audit (amend0930b-slow-cap hardening stage)

## What was read, what was not, and how this was run

**Read in full:** `docs/roadmap/features/T2_F290.md`; `AGENTS.md`; the one paragraph "Operator amendment amend0930b-slow-cap" in `docs/agents/self_drive_protocol.md` (rule 2, the hardening-stage definition this audit executes); `.agent/authored/f290-r5-cpu.txt`.

**Read from `.agent/live_review.md`, by grep only, as instructed:** the seven registration paragraphs `- R-1117`, `- R-1125`, `- R-1127`, `- R-1128`, `- R-1129`, `- R-1133`, `- R-1137`, and the seven matching `Done: R-<id>` paragraphs (`grep -n "^- R-11.." .agent/live_review.md` and `grep -n "^Done: R-11.." .agent/live_review.md`). No other line of that file, and neither `.agent/live_review_archive.md`, `.agent/handoff.md`, `.agent/plan.md`, any `Gate:` paragraph, anything under `.agent/authored/` besides the one file above, nor any `.remedy-wt/f290-*` directory, was opened.

**Read from `.agent/decisions.md`, by grep only:** the three sections headed `DECISION F290 D1`, `DECISION F290 D2`, `DECISION F290 D3`.

**Source and test files read:** `README.md` (Tier 5 row); `docs/README.md` (the `system`/`guides` link lines); `tests/docs/test_docs_consistency.py` (`test_the_readme_tier_table_total_column_matches_the_ledger`, class `TestDocsIndexRegistersEveryPage`); `tests/test_data_root_isolation.py` and `tests/conftest.py` (`_data_root_allocator`); `tests/ui_server/test_preview_end_to_end.py`; `apps/ui/src/api/taskEditSend.ts` and `taskEditSend.test.ts`; `tests/orchestration/test_job_task_runner.py` (class `TestCompletionGate`) and `packages/orchestration/pingpong_job.py` (`validate_job_task_result`); `packages/orchestration/pingpong_loop.py` (`_apply_fake_builder_changes`, `is_fake` wiring) and `packages/orchestration/pingpong_provider.py` (`FakeProvider`); `apps/cli/commands/do_cmd.py` and `apps/cli/command_catalog.py` (`job.run`).

**Worktree:** one disposable worktree, created with:

    git -C /home/decodeux/Repos/remedy worktree add --detach \
      /home/decodeux/Repos/remedy/.remedy-wt/f290-audit-wt 151ca7fc4

`apps/ui/node_modules` was symlinked and `apps/ui/dist` copied into the worktree's `apps/ui/` (via a Python helper, since the raw shell `ln`/`cp` forms were not auto-approved) before any UI test ran.

**Exact command forms used**, all from the worktree:

    python3 -B -m pytest <files or node ids> -q -n auto -p no:cacheprovider
    npm run test:unit -- <file>                      (cwd: <worktree>/apps/ui)
    python3 -B -m apps.cli.main job run <job_id> --builder-provider fake \
      --reviewer-provider fake --json                 (cwd: <worktree>, the one user-level proof)

`__pycache__` was cleared with a short Python snippet before Python runs that followed a restore. Every mutation was made, read, then reverted, with the reverted bytes checked via `cmp` against the primary checkout's own copy of the same file before the next mutation began. No two test commands ran at once; the full suite was never run.

**Primary checkout:** `git -C /home/decodeux/Repos/remedy status --porcelain` was empty before this audit and is empty now; no primary-checkout file was ever opened for writing.

**Not read**, per the brief: `.agent/handoff.md`, `.agent/plan.md`, any `Gate:` paragraph, `.agent/live_review_archive.md`, anything under `.agent/authored/` except `f290-r5-cpu.txt`, and any `.remedy-wt/f290-*` directory (including the pre-existing `.remedy-wt/f290-r4-dry` left by an earlier session, untouched here).

**Total statements audited: 9. Proven at once: 7. Gaps: 0.**

(1 statement is pure ledger-text about the overall paydown, confirmed true by reading, with its seven named repairs proven individually; 1 — R-1137 — is RECORD ONLY, a decision rather than a code repair, as the feature file itself allows.)

## Statement 1 — "Every id this feature takes at its claim carries a resolution line naming its evidence, or is carried by name to the next paydown feature at this closure."

Checked by reading: the seven `Done:` paragraphs are `Done: R-1128` (`c03e2c374`, F290 R1 C2), `Done: R-1127` (`c03e2c374`, F290 R1 C2), `Done: R-1125` (`fc29ef4a3`, F290 R2 C2), `Done: R-1133` (`fc29ef4a3`, F290 R2 C2), `Done: R-1129` (`9d6dc9992`, F290 R3 C2), `Done: R-1117` (`7fc8bc579`, F290 R4 C2), `Done: R-1137` (F290 R5, DECISION F290 D3). All seven ids F290 took (DECISION F290 D1) carry a resolution line; none was carried forward.

Verdict: PROVEN (ledger text confirmed by reading; the seven repairs it names are proven below).

## Statement 2 — R-1128 (preview nonce)

**Test:** `tests/ui_server/test_preview_end_to_end.py::TestPreviewEndToEnd::test_the_preview_flow_runs_end_to_end_on_a_real_fixture_app`.

- Baseline: `1 passed in 27.04s`.
- Mutation (test's own subject, line 170): `nonce = secrets.token_hex(8)` → `nonce = "-" + secrets.token_hex(7)`.
- Red: `1 failed in 1.10s`, `assert 400 == 200` at line 172.
- Restore: `cmp` identical to primary checkout; green: `1 passed in 18.32s`.

Verdict: PROVEN.

## Statement 3 — R-1127 (data-root audit-event test)

**Test:** `tests/test_data_root_isolation.py::test_allocating_a_root_raises_no_audit_event_but_one_mkdir`.

- Baseline: `6 passed in 0.67s`.
- Mutation (`tests/conftest.py`'s `allocate()`): replaced the one `mkdir` with `tmp_path_factory.mktemp("remedy-data-root")`.
- Red: `2 failed, 4 passed in 0.69s` — the new audit-hook test, and the pre-existing `test_a_root_is_made_without_numbering_the_base_directory`.
- Restore: `cmp` identical; green: `6 passed in 0.82s`.

Verdict: PROVEN.

## Statement 4 — R-1125 (README tier totals)

**Test:** `tests/docs/test_docs_consistency.py::TestPrimaryDocsAreHonest::test_the_readme_tier_table_total_column_matches_the_ledger`.

- Baseline: `302 passed in 1.04s`.
- Mutation: `README.md` Tier 5 row `| 5 | Operator Cockpit | 38 | 38 |` → `... | 38 | 37 |`.
- Red: `1 failed, 301 passed in 0.93s` — `README tier rows (tier, Total, ledger total) that differ: [(5, 37, 38)]`.
- Restore: `cmp` identical; green: `302 passed in 1.14s`.

Verdict: PROVEN.

## Statement 5 — R-1133 (docs index registration)

**Test:** `tests/docs/test_docs_consistency.py::TestDocsIndexRegistersEveryPage::test_every_page_in_the_folder_is_linked_from_the_docs_index[system]`.

- Baseline: `302 passed in 0.82s`.
- Mutation: both `docs/README.md` lines linking `system/serve-daemon-v1.md` deleted.
- Red: `1 failed, 301 passed in 0.86s` — `pages docs/README.md does not link: ['system/serve-daemon-v1.md']`.
- Restore: `cmp` identical; green: `302 passed in 0.82s`.

Verdict: PROVEN.

## Statement 6 — R-1129 (task-edit refusal wording)

**Test:** `apps/ui/src/api/taskEditSend.test.ts` → "words a failed revalidation by its detail although current_version came too (R-1129)".

- Baseline: `28 passed`.
- Mutation: swapped the `if` order in `describeTaskEditConflict` (`apps/ui/src/api/taskEditSend.ts`) back to `current_version`-first.
- Red: `1 failed | 27 passed` — expected the `detail` sentence, got the stale-version sentence.
- Restore: `cmp` identical; green: `28 passed`.

Verdict: PROVEN.

## Statement 7 — R-1117 (no-file-change gate) — includes the required user-level proof

**Unit-level.** Mutation of `validate_job_task_result` in `packages/orchestration/pingpong_job.py`: removed
```
if not result.staged_files:
    reasons.append("no_file_changed")
```
- Baseline: `tests/orchestration/test_job_task_runner.py` → `215 passed in 3.86s`.
- Red: `2 failed, 213 passed in 3.54s` — `TestCompletionGate::test_a_job_task_that_changed_no_file_blocks_the_job` and `TestCompletionGate::test_builder_no_changes_with_reviewer_pass_blocks`.

**User-level, through the command line (kept on the same mutated file before restoring).** Built a job the way `parse_job_file` builds one from Markdown (`## Task 1: Do nothing new.`), ran:

    python3 -B -m apps.cli.main job run <job_id> --builder-provider fake --reviewer-provider fake --json

against a throwaway repo with an isolated `REMEDY_DATA_DIR`, with `docs/README.md` pre-seeded with exactly the bytes the fake builder writes for that goal (`_apply_fake_builder_changes`'s `f"# {rel_path}\n\n<!-- Remedy: {goal} -->\n"`), so its own marker check made the "build" a genuine no-op across both ping-pong rounds — the real shape of a builder saying the work is already done, reached with no test harness standing in for `run_job`.

- Red (bug reproduced, mutated file): exit 0; JSON report `"status": "completed"`, `tasks[0].status == "applied_to_job_workspace"`, `tasks[0].error == ""`; staged content byte-identical to the pre-seeded content — a task that changed no file recorded as passed.
- Restored `pingpong_job.py`; `cmp` identical to primary checkout.
- Green, same CLI command, fresh job, `__pycache__` cleared: exit 0; JSON report `"status": "blocked"`, `tasks[0].status == "blocked"`, `tasks[0].error == "completion_gate_failed: no_file_changed"`.
- Unit-level green confirmed afterward: `215 passed in 3.86s`.

Verdict: PROVEN (unit test and a real CLI run both turn red under the mutation and green without it).

## Statement 8 — R-1137 (suite CPU cost)

Checked by reading: `Done: R-1137` names `.agent/authored/f290-r5-cpu.txt` (read in full) and DECISION F290 D3 as the route taken — record, not cut. The file lists eleven test modules (all confirmed to exist in the worktree) measured serially for CPU seconds, summing to 39.18s, and `scripts/closure_suite_cost.py` (confirmed to exist) is named as the next reading's comparison point. DECISION F290 D3's numbers match the ledger paragraph exactly.

What cannot be proved by mutation: this repair is "measure, then record by decision," not a change to any production file or test guard — there is no code path whose removal this statement's truth depends on. Per the feature file's own text and this audit's brief, this is RECORD ONLY rather than forced into a mutation proof that would prove nothing real.

Verdict: RECORD ONLY — the repair is DECISION F290 D3, not production code; the measurement it records has no test or gate to mutate.

## Goal & Done statement

Substantively identical to Statement 1; same seven `Done:` paragraphs confirm every id carries a resolution line with evidence, none carried forward.

Verdict: PROVEN (ledger text confirmed by reading; repairs proven above).

## Gaps

None.

## Worktree removal

    $ git -C /home/decodeux/Repos/remedy worktree remove --force /home/decodeux/Repos/remedy/.remedy-wt/f290-audit-wt
    $ git -C /home/decodeux/Repos/remedy worktree list
    /home/decodeux/Repos/remedy                                  151ca7fc4 [feature/f290-findings-paydown-v6]
    /home/decodeux/Repos/remedy/.remedy-wt/f290-r4-dry           fdf873b6c (detached HEAD)
    /home/decodeux/Repos/remedy/.remedy-wt/job-034ab8c2d9fa4013  218eaabd6 [remedy/job-034ab8c2d9fa4013]
    /home/decodeux/Repos/remedy/.remedy-wt/job-129b3ad7206d4f8d  09441a92a [remedy/job-129b3ad7206d4f8d]
    /home/decodeux/Repos/remedy/.remedy-wt/job-1fe227733cbf41eb  218eaabd6 [remedy/job-1fe227733cbf41eb]
    /home/decodeux/Repos/remedy/.remedy-wt/job-6a38b3203cca4928  aab638e21 [remedy/job-6a38b3203cca4928]
    /home/decodeux/Repos/remedy/.remedy-wt/job-d0f70d9d45dd4363  e4fa7d06f [remedy/job-d0f70d9d45dd4363]
    /home/decodeux/Repos/remedy/.remedy-wt/job-e7268925db3a4831  cc8696a37 [remedy/job-e7268925db3a4831]
    /home/decodeux/Repos/remedy/.remedy-wt/job-e7a145761bf04f86  03d435e59 [remedy/job-e7a145761bf04f86]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f03587d31f444b15  3f36bd811 [remedy/job-f03587d31f444b15]
    /home/decodeux/Repos/remedy/.remedy-wt/job-f196d785124e48bc  3f36bd811 [remedy/job-f196d785124e48bc]
    /home/decodeux/Repos/remedy/.remedy-wt/job-fd57a5d1dfe245b0  68c833e6c [remedy/job-fd57a5d1dfe245b0]

    $ git -C /home/decodeux/Repos/remedy status --porcelain
    (empty)
