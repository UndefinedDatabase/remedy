# Handback — F261 round 1

## Session

`SESSION 1 of feature F261 · round 1 · rounds so far 1`

Session 1 claimed F261 after pull request 250 merged as `7cdde89b`. Context self-assessment: this worker's context is
comfortable, and nothing in the round was cut short.

## Range

Review of `7cdde89b`..`HEAD`: C0a, C0b, C1, C2, C3 and C4, plus this handback commit C5. `.agent/STOP` was ABSENT at all
four readings constraint 2 orders (before C0a, before C2, before C4, before C5): `.remedy-wt/f261r1w/stop.py` printed
`STOP exists: False` and exited 0 each time.

The Open PR Gate read `gh pr list --state open` as `[]` before the branch was cut.

## Commits

### 997b3b9f F261 R1 C0a: save the round 1 step block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f261-r1.md` | +447 / -0 | the block, copied with `shutil.copyfile`; sha256 `2ec68048…98016728` equal to the delegated digest |

### 19e14e71 F261 R1 C0b: mirror the round 1 step block into last_block

| Path | +/- | Reason |
|---|---|---|
| `.agent/last_block.md` | +420 / -178 | the same bytes, the mirror |

### c092f505 F261 R1 C1: re-point the plan at F261 round 1

This is the FIRST SUBSTANTIVE COMMIT.

| Path | +/- | Reason |
|---|---|---|
| `.agent/plan.md` | +26 / -20 | slice PLAN1, a full replacement: 2048 bytes, 39 lines |

### e2dc892a F261 R1 C2: re-head the record, book F275 round 110, resolve R-0889, register R-0890, rule DECISION F261 D1

| Path | +/- | Reason |
|---|---|---|
| `.agent/candidates.md` | +6 / -1 | pair PC, a rewrite: PC-FROM replaced by CAND1 |
| `.agent/decisions.md` | +18 / -0 | slice DEC1 appended: DECISION F261 D1 |
| `.agent/live_review.md` | +29 / -44 | head swap to HEAD1 at the one `^## Findings$` line, 955133 carried bytes unchanged, then RECORD1 appended |
| `docs/roadmap/features/T2_F261.md` | +8 / -0 | pair PD: PD-FROM replaced by AMEND1 |
| `docs/roadmap/features/T2_F273.md` | +2 / -0 | pair PA: PA-FROM replaced by ACC1 |

### 75c96592 F261 R1 C3: claim F261 in the roadmap ledger and re-point the context

| Path | +/- | Reason |
|---|---|---|
| `.agent/context.md` | +26 / -34 | slice CTX1, a full replacement |
| `docs/roadmap/STATUS.md` | +1 / -1 | pair PS, a rewrite: PS-FROM replaced by STATUS1 |

### 1a8de8cd F261 R1 C4: rename do job-evidence to job evidence, with the rename guard

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | +5 / -5 | S1: the entry becomes `job.evidence`, group `job`, subcommand `evidence`; two `related=` references follow |
| `apps/cli/commands/do_cmd.py` | +7 / -7 | S2: handler `_cmd_job_evidence`, table key and index source `job.evidence`, three `do job-evidence` texts, the docstring phrase |
| `docs/system/vocabulary.md` | +1 / -1 | S6 |
| `packages/orchestration/job_evidence.py` | +2 / -2 | S3 |
| `packages/orchestration/pingpong_job.py` | +1 / -1 | S4 |
| `scripts/make_review_zip.sh` | +2 / -2 | S3: the export call and the index hint |
| `tests/cli/test_do_job_flow_review_base.py` | +2 / -2 | S3 |
| `tests/orchestration/test_evidence_index.py` | +4 / -4 | S5 |
| `tests/orchestration/test_job_evidence.py` | +6 / -6 | S5 |
| `tests/orchestration/test_review_zip_hygiene.py` | +1 / -1 | S5 |
| `tests/orchestration/test_stream_export_e2e.py` | +1 / -1 | S3 |
| `tests/orchestration/test_token_ledger.py` | +3 / -3 | S3 |
| `tests/test_command_catalog.py` | +23 / -0 | S7: slice TEST1 appended, `TestRenamedCommands` |

### C5 — this commit (self-reference, R-0149 pattern)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | NO NUMBERS | this handback; its own numstat is reported in the completion message only |

## External actions

| Command | Outcome |
|---|---|
| `gh pr list --state open --json number,headRefName,baseRefName,isDraft` | `[]`, before the branch was cut |
| `git checkout -b feature/f261-cli-vocabulary-v2` | cut at `7cdde89b` |
| `git worktree add --detach .remedy-wt/f261r1w/wt 1a8de8cd…` | created for G6; restored after each mutation with `git -C .remedy-wt/f261r1w/wt checkout -- <file>`, then removed with `git worktree remove .remedy-wt/f261r1w/wt` |
| `git push -u origin feature/f261-cli-vocabulary-v2` | the one push, after this commit; its result is in the completion message (G8) |
| pull request create / merge / force-push / branch delete / `remedy` | NOT RUN |

## Verification

The scripts and raw outputs are under `.remedy-wt/f261r1w/`, not committed.

| Gate | At | REAL exit | Decisive reading |
|---|---|---|---|
| G1 transport | after C1 `c092f505` | `g1g2.py` 0 | sha256 of `.agent/authored/f261-r1.md` at C0a `2ec68048843a2743c30d9409b317f62079618343b38b9b077795b7627778a02c`, **equal** to the delegated digest; `.agent/last_block.md` at C0b **byte-identical**. Slices FOUND **14** (ACC1, AMEND1, CAND1, CTX1, DEC1, HEAD1, PA-FROM, PC-FROM, PD-FROM, PLAN1, PS-FROM, RECORD1, STATUS1, TEST1), mismatching **none** |
| G2 the plan | C1 | `g1g2.py` 0 | `plan.md` **equals** PLAN1; **39** lines; `^## Goal$` **1**; `^## Next Steps$` **1** |
| G3 the record | C2 `e2dc892a` | `g3.py` 0 | (a) `^## Findings$` 1 at base and C2; `live_review.md` **equals** HEAD1 + base from that line + RECORD1; carried-region sha256 `b5b29dc41e4568f994be5719acbd1ebfe020ab683b1b87690f50f0e1b266a565` at base and at C2. (b) `decisions.md` **equals** base + DEC1. (c) PC, PA, PD each **equal** base with FROM's one occurrence replaced by TO; PC at C2 FROM **0** TO **1**. (d) `Gate:` lines **109** → **110**, `Gate: F275 R110 — ` **1**; distinct `- R-` ids **92** → **93**; distinct `Done:` ids **2** → **3**; open by distinct id **90** → **90**, C2 minus base `['R-0890']`, base minus C2 `['R-0889']`. (e) lines beginning `- ` in `candidates.md` **0** |
| G4 the claim | C3 `75c96592` | `g4.py` 0 | PS FROM **0**, TO **1**; `^- \[~\] ` **1**; `^- \[x\] F\d{3} — ` **77** at base and **77** at C3; `context.md` **equals** CTX1 |
| G5 the rename | C4 `1a8de8cd` | `g5.py` 0; ruff 0 | numstat names exactly the **13** paths. Trees: `apps` `34a974f0…`, `packages` `7143da9d…`, `scripts` `79be9d31…`, `tests` `222e7bf7…`, `docs/system` `6cdd3424…`, each **match**. `git grep` prints exactly **1** line: `tests/test_command_catalog.py:274:        ("do.job-evidence", "job.evidence"),`. `python3 -m ruff check` over the 11 `.py` paths: `All checks passed!` |
| G6(a) control | worktree at C4 | 0 | module loaded from the worktree; `121 passed in 25.62s` |
| G6(b) handler key `job.evidense` | same worktree | 1 | FROM count **1**; `5 failed, 116 passed in 25.48s`; failed: `tests/test_command_catalog.py::TestRenamedCommands::test_every_new_id_parses_from_its_words_and_has_a_handler`, `tests/orchestration/test_job_evidence.py::TestCLIJsonRedaction::test_cli_handler_json_output`, `…::TestCLIJsonRedaction::test_cli_handler_text_output`, `…::TestDogfoodCommandShape::test_handler_exists`, `…::TestDogfoodCommandShape::test_documented_shape_runs` |
| G6(c) catalog id `do.job-evidence` | same worktree, after `checkout --` | 1 | FROM count **1**; `5 failed, 116 passed in 19.72s`; failed: `tests/test_command_catalog.py::TestCatalogIntegrity::test_command_id_format`, `…::TestCatalogIntegrity::test_every_related_reference_resolves_to_a_live_command`, `…::TestRenamedCommands::test_no_old_id_is_left_in_the_catalog`, `…::TestRenamedCommands::test_every_new_id_parses_from_its_words_and_has_a_handler`, `tests/orchestration/test_job_evidence.py::TestDogfoodCommandShape::test_command_catalog_has_job_evidence` |
| G7 suites | primary checkout at C4, serially | each 0 | `tests/test_command_catalog.py` 28 passed · `tests/cli/test_advertised_commands.py` 5 passed · `tests/cli/test_command_catalog.py` 22 passed · `tests/cli/test_job_commands.py` 34 passed · `tests/cli/test_cli_ux.py` 57 passed · `tests/orchestration/test_job_evidence.py` 93 passed · `tests/orchestration/test_evidence_index.py` 33 passed · `tests/orchestration/test_review_zip_hygiene.py` 44 passed · `tests/orchestration/test_token_ledger.py` 120 passed · `tests/orchestration/test_stream_export_e2e.py` 7 passed · `tests/cli/test_do_job_flow_review_base.py` 4 passed · `tests/test_do_job_flow.py` 178 passed · `tests/docs/` 306 passed · `tests/orchestration/test_roadmap_index.py` 30 passed · `tests/ui_server/` 505 passed · `tests/orchestration/test_test_runner.py` 51 passed · `tests/regression/test_resource_safety.py` 21 passed · `tests/orchestration/test_integrity_gate.py` 16 passed · canary `tests/cli/test_golden_path.py` 42 passed |
| G8 the tree | after C5 and the push | not yet run | reported in the completion message only |

Open findings: **90** by distinct id. The open High ids are **R-0803, R-0804, R-0806 and R-0807**. R-0889 is resolved and
R-0890 (Low, owner F273) is registered.

## Authored-text proofs

| Text | Target | Result |
|---|---|---|
| the block | `.agent/authored/f261-r1.md`, `.agent/last_block.md` | sha256 **equal** to the delegated digest at C0a; mirror byte-identical at C0b (G1) |
| PLAN1 | `.agent/plan.md` | **equal** at C1 (G2) |
| HEAD1, RECORD1 | `.agent/live_review.md` | **equal** to HEAD1 + carried base region + RECORD1 at C2 (G3a) |
| DEC1 | `.agent/decisions.md` | base + DEC1 at C2 (G3b) |
| PC-FROM/CAND1, PA-FROM/ACC1, PD-FROM/AMEND1 | `.agent/candidates.md`, `T2_F273.md`, `T2_F261.md` | base with the one FROM replaced by TO at C2 (G3c) |
| PS-FROM/STATUS1, CTX1 | `docs/roadmap/STATUS.md`, `.agent/context.md` | FROM 0 / TO 1; CTX1 **equal** at C3 (G4) |
| TEST1 | `tests/test_command_catalog.py` | appended to the base blob; the C4 `tests` tree equals the reviewer's dry run (G5) |

NO SLICE WAS EDITED. Every slice was extracted programmatically from the COMMITTED `.agent/authored/f261-r1.md` and
verified against its BEGIN-marker sha256 before use.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C0a / C0b | done | two commits, as the Bundle orders |
| C1 PLAN1 | done | first substantive commit |
| C2 HEAD1, RECORD1, DEC1, PC, PA, PD | done | one commit |
| C3 PS, CTX1 | done | one commit |
| C4 SPEC S1–S7 | done | one commit |
| C5 handoff | done | this commit |
| G1 · G2 · G3 · G4 · G5 · G6 · G7 | done | exit codes and readings above |
| G8 | skipped | runs after this commit and its push; results in the completion message |

## Deviations & assumptions

1. **G8's `git worktree list` WILL NOT PRINT ONE ROW.** Three worktrees existed before this round began, all detached at
   `7cdde89b`: `.remedy-wt/f261dry/probe`, `.remedy-wt/f261dry/wt` and `.remedy-wt/f261rv/wt`. They are not this
   round's; constraint 4 limits me under `.remedy-wt/` to the block file and my own directory, so I did not remove
   them. My own worktree `.remedy-wt/f261r1w/wt` was removed after G6.
2. **G6 RAN THROUGH A RUNNER**, `.remedy-wt/f261r1w/runner.py`, invoked as `python3 -B`: it changes into the worktree,
   puts it first on `sys.path` and in `PYTHONPATH`, sets `PYTHONDONTWRITEBYTECODE`, asserts that
   `apps.cli.command_catalog` loaded from inside the worktree, and calls `pytest.main` with `-rf --tb=no` and the two
   paths.
3. **STOP READINGS** used a small Python script, because the Bash guard rejects `$?`; exit 0 means absent.
4. **G7** ran through `.remedy-wt/f261r1w/g7.py`, which runs each exact `python3 -B -m pytest -q -p no:randomly <path>`
   argv serially as its own subprocess and reads that subprocess's return code.

## Next

1. Phase 1 rule 1: the next session reads `.agent/STOP` first.
2. The reviewer's verdict on round 1.
3. T001's rename of `do job-promote` to `job apply`.

Operator questions open: 1
