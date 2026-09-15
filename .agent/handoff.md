# Handback — F261 round 10

## Session

`SESSION 3 of feature F261 · round 10 · rounds so far 10`

Context self-assessment: this worker's context is comfortable, and nothing in the round was cut short.

## Range

Review of `a00c1624`..`HEAD`: C0a, C0b, C1, C2, C3 and C4, plus this handback commit C5. `.agent/STOP` was ABSENT at
all three readings constraint 2 orders: before C0a (`ls -la .agent/STOP` exit 2, "No such file or directory"), before
C2 (exit 2) and before C5 (exit 2).

## Commits

### b20ed624 F261 R10 C0a: save the round 10 step block

Commit total per constraint 5: **292** insertions, 0 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r10.md` | +292 / -0 | the block, copied with `shutil.copyfile`; sha256 equal to the delegated digest |

### be0bd9f0 F261 R10 C0b: mirror the round 10 step block into last_block

Commit total per constraint 5: **141** insertions, 135 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +141 / -135 | the same bytes, the mirror |

### a3bac8e2 F261 R10 C1: re-point the plan at round 10, book round 9's PASS and register R-0901, record DECISION F261 D9

This is the FIRST SUBSTANTIVE COMMIT. Commit total per constraint 5: **27** insertions, 10 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +12 / -0 | slice DEC9 appended: DECISION F261 D9 |
| `.agent/live_review.md` | +4 / -0 | slice RECORD10 appended: `Gate: F261 R9 —` PASS and the registration of R-0901 |
| `.agent/plan.md` | +11 / -10 | slice PLAN10, a full replacement: 35 lines |

### 836518f5 F261 R10 C2: fold job digest into the digest section of job show --full, by fold table 1

Commit total per constraint 5: **93** insertions, 138 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r10-fold-1.jsonl` | +21 / -0 | the table, copied with `shutil.copyfile`; sha256 `b7cfcbed…2da6cfe68e` equal |
| `README.md` | +1 / -1 | the F040 paragraph names `remedy job show <id> --full` |
| `apps/cli/command_catalog.py` | +2 / -16 | the `--full` help names the completion digest; entry `job.digest` and its comment deleted |
| `apps/cli/commands/job.py` | +31 / -51 | `_digest_section` registered; `_cmd_job_digest` and its handler row deleted |
| `packages/orchestration/job_digest.py` | +1 / -1 | the docstring names the digest section |
| `tests/cli/test_job_digest_cli.py` | +34 / -67 | the tests read the digest section of `job show --full`; the unknown-id and catalog-registration tests deleted |
| `tests/cli/test_job_show.py` | +1 / -1 | the registry reads `permissions`, `fences`, `assumptions`, `digest`, `dod` |
| `tests/test_command_catalog.py` | +1 / -0 | `job.digest` joins `TestDeletedCommands` |
| `tests/ui_contracts/test_decision_urgency_parity.py` | +1 / -1 | the docstring names the digest section |

### 526de930 F261 R10 C3: fold job summary into the summary section of job show --full, by fold table 2

Commit total per constraint 5: **127** insertions, 86 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r10-fold-2.jsonl` | +17 / -0 | the table, copied with `shutil.copyfile`; sha256 `e1cb068a…c5b49d9fe9` equal |
| `apps/cli/command_catalog.py` | +3 / -14 | the `--full` help names the summary; entry `job.summary` deleted; `related=` tuples of `job status` and `job report` drop it |
| `apps/cli/commands/job.py` | +38 / -52 | `_summary_section` registered; `_cmd_job_summary` and its handler row deleted |
| `docs/guides/simple-operator-quickstart-v0.md` | +1 / -1 | the equivalents table drops `job summary` |
| `packages/orchestration/event_replay.py` | +2 / -2 | two checkpoint hints name `remedy job show <id> --full --json` |
| `packages/orchestration/ui_server.py` | +3 / -3 | three pipeline hints name `remedy job show <id> --full --json` |
| `tests/cli/test_job_show.py` | +60 / -1 | the registry order; `TestSummarySection` for a job without and with run events |
| `tests/test_command_catalog.py` | +1 / -0 | `job.summary` joins `TestDeletedCommands` |
| `tests/ui_server/test_dashboard_contract.py` | +2 / -13 | the source contract reads `_summary_section`; the two catalog tests deleted |

### 47d34a44 F261 R10 C4: fold job status into the status section of job show --full, by fold table 3

Commit total per constraint 5: **214** insertions, 198 deletions.

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r10-fold-3.jsonl` | +44 / -0 | the table, copied with `shutil.copyfile`; sha256 `b14b2aa8…69a10e1ca10` equal |
| `apps/cli/command_catalog.py` | +3 / -13 | the `--full` help names the status; entry `job.status` deleted; `job report` relates to `job show` alone, `job fulfill` to `job show` and `job report` |
| `apps/cli/commands/job.py` | +85 / -97 | `_status_section` registered, open-decision block first, full job id in the next safe action; `_cmd_job_status` and its handler row deleted |
| `docs/guides/simple-operator-quickstart-v0.md` | +4 / -4 | the guide names `job show <id> --full --json` |
| `docs/system/core-product-spine-v0.md` | +2 / -2 | the flow and the table name `job show <job_id> --full --json` |
| `docs/system/first-fulfilled-job-demo-v0.md` | +2 / -2 | the demo and its field table name the status section |
| `docs/system/first-perfect-job-demo-v0.md` | +3 / -3 | the demo and its field table name the status section |
| `packages/orchestration/run_report.py` | +1 / -1 | the comment names the status section |
| `scripts/remedy_smoke.sh` | +5 / -3 | reads `sections.status.data` of `job show --full --json` from stdin |
| `tests/cli/test_job_show.py` | +1 / -1 | the registry reads `permissions`, `fences`, `assumptions`, `digest`, `summary`, `status`, `dod` |
| `tests/cli/test_open_decisions_view.py` | +34 / -20 | `TestJobStatusView` reads the status section of `job show --full` |
| `tests/cli/test_plan_approval.py` | +4 / -2 | the golden path reads `sections.status.data` |
| `tests/cli/test_product_spine.py` | +17 / -40 | the truth-field tests read the status section; the catalog, handler and unknown-id tests of `job status` deleted |
| `tests/orchestration/test_job_fulfillment.py` | +8 / -10 | the status after fulfil reads the section; the guide test reads the new command; the handler test deleted |
| `tests/test_command_catalog.py` | +1 / -0 | `job.status` joins `TestDeletedCommands` |

### C5 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `git worktree add --detach .remedy-wt/f261r10w/wt 47d34a44` | created for G5; restored after each mutation with `git -C .remedy-wt/f261r10w/wt checkout -- apps/cli/commands/job.py` (rc 0, worktree status `''` after each), then removed with `git worktree remove --force .remedy-wt/f261r10w/wt` (rc 0); `git worktree list` then read one row and `git branch --list 'remedy/job-*'` 16 lines |
| `git push origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G7) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r10w/`, not committed. Every exit code below is the real return
code of the command as the tool reported it.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `a3bac8e2` | `gate_g1g2.py` 0 | sha256 of `.agent/authored/f261-r10.md` at C0a `79c6de8f519b85a4306a17cc7b78690808a625dd7f2bcefba4243abe26cd5a2e`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical**. Slices FOUND **13** (PLAN10, RECORD10, DEC9, MUT-1-FROM to MUT-5-TO), each **matching** its BEGIN-marker sha256. Committed carriers read by `gate_g3g4.py` (exit 0): fold-1 at C2 `b7cfcbed8c02a270f0864cae0d9efe17761f6f6719cbed4b587c4d2da6cfe68e`, fold-2 at C3 `e1cb068aa05e2f8879a61caa06bdd86c87b144a6a60daa3bf20c9cc5b49d9fe9`, fold-3 at C4 `b14b2aa8ad6de7866e243174063dee46de6e89d81fc725a62c85f69a10e1ca10`, each **equal** |
| G2 the record | C1 | `gate_g1g2.py` 0 | `plan.md` **equals** PLAN10; **35** lines; `^## Goal$` **1**; `^## Next Steps$` **1**. `live_review.md` **equals** its `a00c1624` blob + RECORD10; `decisions.md` **equals** its `a00c1624` blob + DEC9. `^Gate: F\d+ R\d+ — ` **118** → **119**; `Gate: F261 R9 — ` **1** at C1; distinct `^- R-\d+ — ` **103** → **104**, C1 minus base `R-0901`, base minus C1 empty; distinct `^Done: R-\d+ — ` **6** → **6**, sets equal; open by distinct id **97** → **98** |
| G3 the folds | C2 `836518f5`, C3 `526de930`, C4 `47d34a44` | `gate_g3g4.py` 0 | tables: fold-1 **21** rows, fold-2 **17**, fold-3 **44**, every count as stated. `--no-renames --name-only` from each parent: exactly the carrier and the paths G3 names, at each commit (9, 9 and 15 paths). `apps`, `tests`, `docs`, `scripts`, `packages`, `README.md` each **match** the dry run: C2 `80d1da4c…`, `b2126781…`, `d74ed73f…`, `fb0b7d81…`, `6d7aff6a…`, `15b9e0e8…`; C3 `f996a904…`, `e3248c39…`, `618a4250…`, `fb0b7d81…`, `b9d7334d…`, `15b9e0e8…`; C4 `36d6d17b…`, `56e365a3…`, `d02995d3…`, `68e16104…`, `f8b5f7a1…`, `15b9e0e8…`. Insertions: C2 **93** (138 deletions), C3 **127** (86), C4 **214** (198) |
| G4 the sweep | C4 `47d34a44` | `gate_g3g4.py` 0 | the fixed-string `git grep` exit **0**, exactly three lines: `47d34a44:tests/test_command_catalog.py:307:        "job.digest",`, `…:311:        "job.status",`, `…:312:        "job.summary",`, all inside `TestDeletedCommands.DELETED` (lines 301 to 313). The extended `git grep` of `remedy job (digest\|summary\|status)\b` exit **1**, stdout `''`. `python3 -m ruff check` over the 15 `.py` paths of C2, C3 and C4: exit **0**, `All checks passed!`. `bash -n scripts/remedy_smoke.sh`: exit **0** |
| G5(a) control | worktree at C4 | 0 | `apps.cli.commands.job` loaded from the worktree; `251 passed in 12.22s`; **0** failed nodes |
| G5(1) a `job.status` handler row | same worktree | 1 | MUT-1-FROM count **1**; `1 failed, 250 passed in 12.38s`; **1** failed node, `TestDeletedCommands::test_no_deleted_id_is_left_in_the_dispatch_table` **among them** |
| G5(2) the digest wrapped in a key | same worktree, after `checkout --` | 1 | MUT-2-FROM count **1**; `2 failed, 249 passed in 12.04s`; **2** failed nodes, `TestJsonModeMatchesTheEnvelopeExactly::test_the_payload_is_not_wrapped_in_an_extra_key` **among them** (the other `…::test_the_json_payload_equals_build_job_digest_independently_computed`) |
| G5(3) a summary that is never live | same worktree, after `checkout --` | 1 | MUT-3-FROM count **1**; `1 failed, 250 passed in 12.06s`; **1** failed node, `TestSummarySection::test_a_job_with_run_events_is_live` **among them** |
| G5(4) the open decisions after the job line | same worktree, after `checkout --` | 1 | MUT-4-FROM count **1**; `1 failed, 250 passed in 12.20s`; **1** failed node, `TestJobStatusView::test_the_open_decision_block_is_printed_first` **among them** |
| G5(5) two registry entries swapped | same worktree, after `checkout --` | 1 | MUT-5-FROM count **1**; `1 failed, 250 passed in 12.07s`; **1** failed node, `TestSections::test_full_prints_the_registered_sections_in_the_d4_order` **among them** |
| G6 the suite, SPEC S | primary checkout at C4, serially | 0 | `suite_spec.py`: argv `python3 -B -m pytest -q -p no:randomly -p no:cacheprovider --tb=short -rfEs`, `PYTHONPATH`, `REMEDY_PROJECT`, `REMEDY_DATA_DIR` removed, `PYTHONDONTWRITEBYTECODE=1`; last line `18188 passed, 23 skipped, 1 warning in 1344.90s (0:22:24)`; distinct bad nodes **0**, so no re-run; `git status --porcelain` `''` afterwards |
| G7 the tree | after C5 and the push | not yet run | reported in the completion message only |

Open findings: **98** by distinct id. The open High ids are **R-0803, R-0804 and R-0807**.

Operator questions open: 0

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r10.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN10 | `.agent/plan.md` | **equal** at C1 (G2) |
| RECORD10, DEC9 | `.agent/live_review.md`, `.agent/decisions.md` | each **equal** to its `a00c1624` blob followed by the slice at C1 (G2) |
| fold tables 1, 2, 3 | `.agent/authored/f261-r10-fold-{1,2,3}.jsonl` and their paths | carrier digests **equal**; the C2, C3 and C4 trees equal the reviewer's dry run (G3) |
| MUT-1-FROM to MUT-5-TO | the G5 worktree only | used as the mutation bytes; never written to the checkout |

NO SLICE AND NO TABLE WAS EDITED. Every slice was extracted programmatically as the bytes strictly between its `BEGIN`
and `END` lines and verified against its BEGIN-marker sha256 before use; each table was verified against its digest
before it was applied and copied.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN10, RECORD10, DEC9 | done | one commit, the first substantive commit |
| C2 fold table 1, `job digest` | done | one commit |
| C3 fold table 2, `job summary` | done | one commit |
| C4 fold table 3, `job status` | done | one commit |
| C5 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 | done | exit codes and readings above |
| G7 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **G1's carrier clause was read after C4, not after C1.** Constraint 8 places G1 after C1, but the carriers are first
   committed at C2 to C4; their committed digests were read by `gate_g3g4.py` after C4, and each source carrier's
   digest was also verified before its table was applied and copied.
2. **Tables were applied directly on disk.** `.remedy-wt/f261r10w/apply_table.py` checks the carrier digest, then
   applies every row strictly in file order against the tree the previous rows left, with `encoding="utf-8",
   newline=""`, the exact-count check and the must-not-exist check, stopping on the first mismatch; it copies the
   carrier after the last row. Every row was an `edit`; no count differed, so no STOP arose.
3. **G4's ruff ran over the working tree at C4**, so the `.py` paths of C2 and C3 were checked in their C4 content.
4. **G5 ran through a runner**, `.remedy-wt/f261r10w/wt_runner.py`, invoked as `python3 -B`: it drops its own directory
   from `sys.path`, changes into the worktree, puts it first on `sys.path` and in `PYTHONPATH`, removes
   `REMEDY_PROJECT` and `REMEDY_DATA_DIR`, sets `PYTHONDONTWRITEBYTECODE=1`, asserts that `apps.cli.commands.job`
   loaded from inside the worktree, and calls `pytest.main` with `-q -p no:randomly -p no:cacheprovider -rf --tb=no`
   over the seven test files G5 names.
5. **Commit subjects** were worded by this worker, since the block names each commit's content but not its subject.
6. **The open set** was computed as the distinct `^- R-\d+ — ` ids minus the distinct `^Done: R-\d+ — ` ids.
7. **The suite ran in the foreground**, inside one tool call with a 60-minute limit, from the primary checkout; it
   finished in 22 minutes and nothing else ran meanwhile.
8. **File reading before edits.** The tables and slices were applied programmatically, so instead of reading each
   target file in full I read the unstaged diff of each of C1 to C4 before committing; the byte-equality, tree-id
   gates and ruff prove each result.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 10.
3. The fold of `job report` and the deletion of `do job-report`.
