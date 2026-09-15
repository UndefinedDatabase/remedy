# Handback — F261 round 12

## Session

`SESSION 3 of feature F261 · round 12 · rounds so far 12`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `a75814c6`..`HEAD`: C0a, C0b, C1, C2, C3, C4 and C5, plus this handback commit C6. `.agent/STOP` was
ABSENT at all three readings constraint 2 orders: before C0a, before C2 and before C6, each read by
`.remedy-wt/f261r12w/stopcheck.py`, which runs `test -e .agent/STOP` and printed `exit 1 -> absent` each time.

## Commits

### 0e1808d9 F261 R12 C0a: save the round 12 step block

Commit total per constraint 5: **285** insertions, 0 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r12.md` | +285 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### 247fd612 F261 R12 C0b: mirror the round 12 step block into last_block

Commit total per constraint 5: **138** insertions, 166 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +138 / -166 | the same bytes, the mirror |

### 52b7b07a F261 R12 C1: re-point the plan at round 12, book round 11's PASS and the resolutions of R-0901 and R-0902, record DECISION F261 D11

This is the FIRST SUBSTANTIVE COMMIT. Commit total per constraint 5: **32** insertions, 12 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +16 / -0 | slice DEC11 appended: DECISION F261 D11 |
| `.agent/live_review.md` | +6 / -0 | slice RECORD12 appended: `Gate: F261 R11 —` PASS and `Done:` for R-0901 and R-0902 |
| `.agent/plan.md` | +10 / -12 | slice PLAN12, a full replacement: 32 lines |

### 01eda6bf F261 R12 C2: give the staging pipeline's job-result promote words apply words, by the staging table

Commit total per constraint 5: **239** insertions, 160 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r12-staging.jsonl` | +79 / -0 | the table, 79 `edit` rows, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/commands/job.py` | +7 / -7 | the status and report sections and `_extract_job_truth` read `applied_to_target` |
| `apps/ui/src/api/humanizeCatalog.ts` | +1 / -1 | the stream event `staging_applied_to_target` replaces `staging_promoted` |
| `docs/system/first-fulfilled-job-demo-v0.md` | +7 / -7 | the demo's field tables and guarantees name the target apply |
| `packages/orchestration/job_fulfillment.py` | +30 / -30 | record fields, contract flag, blocker codes, export keys and run event renamed per D11 CHOSEN FIRST |
| `packages/orchestration/staging_workspace.py` | +39 / -39 | `apply_staged_changes_to_target` and `TargetApplyResult` replace the promote names |
| `tests/cli/test_job_report.py` | +2 / -2 | the former report key list reads `applied_to_target` |
| `tests/orchestration/test_fence_production_e2e.py` | +3 / -3 | asserts read `applied_to_target` |
| `tests/orchestration/test_job_fulfillment.py` | +71 / -71 | tests and class names read the target apply words |

### b7b2d179 F261 R12 C3: give the run level's job-result promote words apply words, by the run table

Commit total per constraint 5: **78** insertions, 52 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r12-run.jsonl` | +26 / -0 | the table, 26 `edit` rows, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/commands/do_cmd.py` | +2 / -2 | `do evidence` reads `apply_readiness` and prints `Ready to apply:` |
| `apps/ui/src/api/humanizeCatalog.ts` | +1 / -1 | the trace event `apply_dry_run_completed` |
| `packages/orchestration/agent_run_trace.py` | +1 / -1 | the trace event kind `apply_dry_run_completed` |
| `packages/orchestration/pingpong_evidence.py` | +8 / -8 | `apply_readiness`, `_assess_apply_readiness`, `## Apply Readiness` |
| `packages/orchestration/pingpong_loop.py` | +11 / -11 | `apply_allowed`, printed `Apply: allowed` / `Apply: blocked` |
| `tests/orchestration/test_evidence_bundle.py` | +4 / -4 | asserts read `apply_readiness` |
| `tests/orchestration/test_repair_loop.py` | +25 / -25 | asserts and names read `apply_allowed` and apply words |

### f4d5f4dd F261 R12 C4: word the builder's repair prompt with a target apply, by the prompt table

Commit total per constraint 5: **5** insertions, 3 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r12-prompt.jsonl` | +2 / -0 | the table, 2 `edit` rows, copied with `shutil.copyfile`; sha256 equal |
| `packages/orchestration/pingpong_loop.py` | +1 / -1 | `Do not apply changes to the target repository, commit, or push.` |
| `tests/orchestration/test_builder_prompt_golden.py` | +2 / -2 | the `full` and `resumed` frozen renders |

### 514941fc F261 R12 C5: hold the kept promote senses by file and token, by the guard table

Commit total per constraint 5: **367** insertions, 29 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r12-guard.jsonl` | +30 / -0 | the table, 29 `edit` rows and 1 `create`, copied with `shutil.copyfile`; sha256 equal |
| `apps/cli/command_catalog.py` | +1 / -1 | the `do` group reads `Run, report, and apply Remedy tasks.` |
| `docs/roadmap/features/T2_F261.md` | +5 / -1 | the Acceptance bullet names the guard test for its promote half |
| `docs/system/self-use-track-v1.md` | +2 / -2 | `never applies` |
| `packages/orchestration/final_verifier.py` | +1 / -1 | a docstring takes an apply word |
| `packages/orchestration/job_evidence.py` | +1 / -1 | a docstring takes an apply word |
| `packages/orchestration/pingpong_job.py` | +3 / -3 | a docstring and two comments take apply words; the `promoted` comment about records on disk stays |
| `packages/orchestration/self_use_job.py` | +2 / -2 | docstring takes apply words |
| `packages/orchestration/self_use_runner.py` | +3 / -3 | docstring takes apply words |
| `packages/orchestration/token_measurement.py` | +1 / -1 | a comment takes an apply word |
| `scripts/build_review_manifest.py` | +2 / -2 | two comments take apply words; the `promote_ready` key check stays |
| `tests/cli/test_task_input.py` | +1 / -1 | the fixture body reads `auto-apply` |
| `tests/docs/test_retired_promote_word.py` | +304 / -0 | NEW: the guard, `KEPT_BY_SENSE` by file and token |
| `tests/orchestration/test_final_verifier.py` | +2 / -2 | docstrings take apply words |
| `tests/orchestration/test_job_task_runner.py` | +2 / -2 | a section comment and `TestApplySafetyReuse` take apply words |
| `tests/orchestration/test_review_final_verifier_reproducible.py` | +1 / -1 | a `commit_execution_gate` fixture value reads `APPLY_READY` |
| `tests/orchestration/test_review_gate_embedded_verdicts.py` | +5 / -5 | a docstring, a test name, a comment and a loop variable take apply words |
| `tests/orchestration/test_self_use_runner.py` | +1 / -1 | a docstring takes an apply word |

### C6 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r12w/wt 514941fcef235525c357545f99c5661ca1d9558a` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r12w/wt checkout -- <that file>` (exit 0, worktree status `''` after each), then removed with `git worktree remove --force .remedy-wt/f261r12w/wt` (exit 0); `git worktree list` then read one row and `git branch --list 'remedy/job-*'` 16 lines |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r12w/`, not committed. Every exit code below is the real return
code of the command as the tool reported it.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `52b7b07a`; carriers after C5 | `gate_g1g2.py` 0; `gate_g3g4.py` 0 | sha256 of `.agent/authored/f261-r12.md` at C0a `2bd2c3d75bdf08906dc31170a50034030625dcf62185f679dd3ffb17d400a870`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical** (27720 bytes). Slices FOUND **13** (PLAN12, RECORD12, DEC11, MUT-1-FROM to MUT-5-TO), each **matching** its BEGIN-marker sha256. Committed carriers: staging at C2 `135761a9…a9d43`, run at C3 `55178efb…8dab3`, prompt at C4 `755eb74f…13965`, guard at C5 `66402eaf…debef`, each **equal** to its digest |
| G2 the record | C1 | `gate_g1g2.py` 0 | `plan.md` **equals** PLAN12; **32** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `a75814c6` blob + RECORD12 (1010409 + 5072 = 1015481 bytes); `decisions.md` **equals** its `a75814c6` blob + DEC11 (1375496 + 4553 = 1380049). `^Gate: F\d+ R\d+ — ` **120** → **121**; `Gate: F261 R11 — ` **1** at C1; distinct `^- R-\d+ — ` **105** → **105**, sets equal; distinct `^Done: R-\d+ — ` **6** → **8**, C1 minus base `R-0901`, `R-0902`, base minus C1 empty; open by distinct id **99** → **97** |
| G3 the tables | C2 `01eda6bf`, C3 `b7b2d179`, C4 `f4d5f4dd`, C5 `514941fc` | `gate_g3g4.py` 0 | tables: staging **79** rows, run **26**, prompt **2**, guard **30**, every count as stated, no STOP. `--no-renames --name-only` from each parent: exactly the carrier and the paths G3 names (9, 8, 3 and 18 paths). `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` each **match** the dry run at C2 (`34149b9b…`, `ac75c123…`, `a806f9ec…`, `68e16104…`, `36e5e18b…`, `15b9e0e8…`), C3 (`db1fd362…`, `f497a373…`, `a806f9ec…`, `68e16104…`, `58ec80b5…`, `15b9e0e8…`), C4 (`db1fd362…`, `dcec9a3a…`, `a806f9ec…`, `68e16104…`, `c0c391ae…`, `15b9e0e8…`) and C5 (`fbc3f1d7…`, `0f80e084…`, `43175c76…`, `e3c01bde…`, `0e39ea4b…`, `15b9e0e8…`). Insertions: C2 **239** (160 deletions), C3 **78** (52), C4 **5** (3), C5 **367** (29); each single-parent |
| G4 the sweep | C5 `514941fc` | `gate_g3g4.py` 0 | the `git grep -n -I -i -E` of the eleven old names over `apps packages scripts tests docs README.md ':!docs/roadmap'` at C5: exit **1**, stdout `''`. `python3 -m ruff check` over the 28 `.py` paths of C2 to C5: exit **0**, `All checks passed!` |
| G5(a) control | worktree at C5 | 0 | `packages.orchestration.job_fulfillment` loaded from the worktree; `362 passed in 13.24s`; **0** failed nodes |
| G5(1) old field beside the new | same worktree | 1 | MUT-1-FROM count **1** in `job_fulfillment.py`; `1 failed, 361 passed in 13.58s`; **1** failed node, `test_no_file_outside_the_map_carries_the_word` **among them** |
| G5(2) job-result token among routing words | same worktree, after `checkout --` | 1 | MUT-2-FROM count **1** in `model_routing.py`; `1 failed, 361 passed in 13.12s`; **1** failed node, `test_no_kept_file_carries_a_token_outside_its_set` **among them** |
| G5(3) a kept token gone | same worktree, after `checkout --` | 1 | MUT-3-FROM count **1** in `dev_server.py`; `1 failed, 361 passed in 13.17s`; **1** failed node, `test_every_token_listed_for_a_file_still_occurs_in_it` **among them** |
| G5(4) the old repair prompt line | same worktree, after `checkout --` | 1 | MUT-4-FROM count **1** in `pingpong_loop.py`; `3 failed, 359 passed in 13.53s`; **3** failed nodes, `test_segments_reassemble_into_the_frozen_render[full]` **among them** (with `[resumed]` and `test_no_file_outside_the_map_carries_the_word`) |
| G5(5) apply never allowed | same worktree, after `checkout --` | 1 | MUT-5-FROM count **1** in `pingpong_loop.py`; `1 failed, 361 passed in 13.02s`; **1** failed node, `TestFinalAdjudication::test_no_findings_ready` **among them** |
| G6 the suite, SPEC S | primary checkout at C5, serially | 0 | `suite_spec.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `18183 passed, 23 skipped, 1 warning in 1372.77s (0:22:52)`; distinct bad nodes **0**, so no re-run; `git status --porcelain` `''` afterwards |
| G7 the tree | after C6 and the push | not yet run | reported in the completion message only |

Open findings: **97** by distinct id. The open High ids are **R-0803, R-0804 and R-0807**.

Operator questions open: 0

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r12.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN12 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD12, DEC11 | `.agent/live_review.md`, `.agent/decisions.md` | each **equal** to its `a75814c6` blob followed by the slice at C1 (G2) |
| the four tables | `.agent/authored/f261-r12-{staging,run,prompt,guard}.jsonl` and their paths | carrier digests **equal**; the C2 to C5 trees equal the reviewer's dry run (G3) |
| MUT-1-FROM to MUT-5-TO | the G5 worktree only | used as the mutation bytes; never written to the checkout |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically as the bytes strictly between its `BEGIN`
and `END` lines and verified against its BEGIN-marker sha256 before use; each table was verified against its digest
before it was applied and copied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN12, RECORD12, DEC11 | done | one commit, the first substantive commit |
| C2 the staging table | done | one commit |
| C3 the run table | done | one commit |
| C4 the prompt table | done | one commit |
| C5 the guard table | done | one commit |
| C6 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **G1's carrier clause was read after C5, not after C1.** Constraint 8 places G1 after C1, but the carriers are first
   committed at C2 to C5; their committed digests were read by `gate_g3g4.py` after C5, and each source carrier's
   digest was also verified before its table was applied and copied.
2. **Tables were applied directly on disk.** `.remedy-wt/f261r12w/apply_table.py` checks the carrier digest, then
   applies every row strictly in file order against the tree the previous rows left, with `encoding="utf-8",
   newline=""`, the exact-count check and the must-not-exist checks, stopping on the first mismatch; it copies the
   carrier after the last row. No count differed and no target existed, so no STOP arose.
3. **G4's ruff ran over the working tree at C5** (HEAD `514941fc`, status `''`), so the `.py` paths of C2 to C4 were
   checked in their C5 content.
4. **G5 ran through a runner**, `.remedy-wt/f261r12w/wt_runner.py`, invoked as `python3 -B`: it drops its own directory
   from `sys.path`, changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, removes
   `REMEDY_PROJECT` and `REMEDY_DATA_DIR`, sets `PYTHONDONTWRITEBYTECODE=1`, asserts that
   `packages.orchestration.job_fulfillment` loaded from inside the worktree, and calls `pytest.main` with `-q -p
   no:randomly -p no:cacheprovider -rf --tb=no` over the six test files G5 names.
5. **Commit subjects** were worded by this worker, since the block names each commit's content but not its subject.
6. **The open set** was computed as the distinct `^- R-\d+ — ` ids minus the distinct `^Done: R-\d+ — ` ids.
7. **The STOP readings went through a script**, `stopcheck.py`, which runs `test -e .agent/STOP` and prints its return
   code.
8. **The suite ran in the foreground**, inside one tool call with a 60-minute limit, from the primary checkout; it
   finished in 23 minutes and nothing else ran meanwhile.
9. **File reading before edits.** The tables and slices were applied programmatically, so instead of reading each
   target file in full I read the unstaged diff of each of C1 to C5 and the created guard test in full before
   committing; the byte-equality, tree-id gates, ruff, the red-proofs and the suite prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 12.
3. The plan of T003, the prune to D4, split by group before its first round.
