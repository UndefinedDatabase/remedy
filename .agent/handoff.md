# Handoff — F273 Findings paydown v1 · Round 2

## Session

SESSION 1 of feature F273 · round 2 · rounds so far 2

Context self-assessment: the worker read the block, AGENTS.md, DECISION F273 D2, the handback template and the self-drive protocol's questions-file rule; every figure below comes from a command run in this round, and the worker's context held all of it without loss.

## Range

Review of f32363e9..HEAD — branch `feature/f273-findings-paydown-v1`.

## Summary

Round 2 books round 1's verdict, repairs round 1's five reds and builds the rest of T001.
- C1 books Gate F273 R1 (VERDICT PASS) and the resolutions of R-0804 and R-0810 into the ledger, appends one prose slip, lands DECISION F273 D2, rewrites the plan and saves the five payload copies.
- C2 repairs round 1's five reds: four `tests/orchestration/test_config.py` tests delete `REMEDY_DATA_DIR` first, and the walk test's docstring no longer names the deleted adapter class.
- C3 builds R-0812: `run_job` writes `task_run_started`, one `task_round_completed` per round, and `task_run_completed` or `task_run_failed`; the teacher's table narrates every kind the unified path writes.
- C4 builds R-0807's code and tests: one ledger row per provider call, keyed `"<job_id>:<task_id>:<seq>"`, superseding the task run's old D16 row.
- C5 adds R-0807's dated note to the D16 section of `docs/roadmap/features/T2_F103.md`.
- C6 is this handoff.

Landed: R-0812 — `d2c65597`
Landed: R-0807 — `b090e6f9` (code and tests) and `7a6b4c9a` (docs); resolution also needs a real run's row count to equal its call count, read from the closure sequence's self-use run (DECISION F273 D2 (1))

## Commits

### a30377c1 F273 R2 C1: book round 1's verdict and the R-0804 and R-0810 resolutions, land DECISION F273 D2 and save the round 2 payloads
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/authored/f273-r2-block.md` | +103 / -0 | Byte copy of the block |
| `.agent/authored/f273-r2-decisions.md` | +48 / -0 | Byte copy of decisions.md |
| `.agent/authored/f273-r2-ledger.md` | +6 / -0 | Byte copy of ledger.md |
| `.agent/authored/f273-r2-plan.md` | +28 / -0 | Byte copy of plan.md |
| `.agent/authored/f273-r2-slips.md` | +1 / -0 | Byte copy of slips.md |
| `.agent/decisions.md` | +48 / -0 | `f32363e9` bytes + decisions.md (DECISION F273 D2) |
| `.agent/live_review.md` | +6 / -0 | `f32363e9` bytes + ledger.md (Gate F273 R1, R-0804 and R-0810 resolutions) |
| `.agent/plan.md` | +10 / -11 | := plan.md |
| `.agent/prose_slips.md` | +1 / -0 | `f32363e9` bytes + slips.md |

251 insertions, 11 deletions (`git show --numstat`).

### cbbf10bd F273 R2 C2: round 1's reds — four config tests delete REMEDY_DATA_DIR first and the walk docstring no longer names the deleted adapter
| Path | +/- | Reason |
|------|-----|--------|
| `tests/orchestration/test_config.py` | +10 / -4 | `monkeypatch.delenv("REMEDY_DATA_DIR")` in four tests — `git apply .remedy-wt/f273-proto-r1fix.diff` |
| `tests/ui_server/test_handler_table_walk.py` | +2 / -2 | Docstring no longer names the deleted adapter class — same diff |

12 insertions, 6 deletions.

### d2c65597 F273 R2 C3: R-0812 — the unified job path writes task and round events and the teacher narrates every kind it writes
| Path | +/- | Reason |
|------|-----|--------|
| `apps/ui/src/api/humanizeCatalog.ts` | +1 / -0 | `task_round_completed` catalog entry — `git apply .remedy-wt/f273-proto-r0812.diff` |
| `packages/orchestration/pingpong_job.py` | +62 / -0 | Task-lifecycle writes in `run_job`, fail-soft helpers — same diff |
| `packages/orchestration/teacher_narration.py` | +16 / -4 | Four new kinds; fields read from `metadata` when absent at top level — same diff |
| `tests/cli/test_do_sequence_cli.py` | +13 / -0 | `do` job without a budget narrates its task events — same diff |
| `tests/cli/test_teacher_cmd.py` | +77 / -0 | `TestTeacherNarratesTheUnifiedJobPath` — same diff |
| `tests/orchestration/test_teacher_narration.py` | +15 / -0 | Pinned set widened; metadata fallback and precedence — same diff |

184 insertions, 4 deletions.

### b090e6f9 F273 R2 C4: R-0807 — one ledger row per provider call, keyed by the attempt's seq, superseding the task run's old row
| Path | +/- | Reason |
|------|-----|--------|
| `apps/cli/commands/stats_ledger_cmd.py` | +2 / -1 | Backfill's `recorded` counts task runs — `git apply --exclude=docs/roadmap/features/T2_F103.md .remedy-wt/f273-proto-r0807.diff` |
| `packages/orchestration/pingpong_evidence.py` | +7 / -6 | Live hook records per-call rows — same diff |
| `packages/orchestration/pingpong_loop.py` | +43 / -3 | Attempt `round`; `seq`, `round`, `usage`, `total_cost_usd` per attempt in evidence — same diff |
| `packages/orchestration/token_ledger.py` | +203 / -19 | `call_id_for_provider_call`, `call_records_from_evidence`, `record_task_run_calls` (supersede rule), per-call segments, backfill and verify — same diff |
| `tests/cli/test_do_sequence_cli.py` | +2 / -0 | Cost roles read builder and reviewer — same diff |
| `tests/orchestration/test_token_ledger.py` | +139 / -28 | Per-call rows; `TestOneRowPerProviderCall` — same diff |

396 insertions, 57 deletions.

### 7a6b4c9a F273 R2 C5: R-0807 — the D16 section of T2_F103.md notes that its per-call switch was made
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/features/T2_F103.md` | +9 / -0 | Dated D16 amendment — `git apply --include=docs/roadmap/features/T2_F103.md .remedy-wt/f273-proto-r0807.diff` |

9 insertions, 0 deletions.

### C6 (this commit) F273 R2 C6: handoff
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/handoff.md` | rewritten | This handback |

Every commit is under 500 inserted lines. The largest is C4, with 396.

## External actions

- `git worktree add --detach .remedy-wt/f273-r2-g5 7a6b4c9a` for G5, then `git worktree remove .remedy-wt/f273-r2-g5` (exit 0). `git worktree list` afterwards: the primary checkout at `7a6b4c9a` on `feature/f273-findings-paydown-v1` and the reviewer's `.remedy-wt/f273-r2-dry` at `f32363e9`, nothing else.
- After C6: `git push`. No pull request is opened.

## Verification

Exit codes were read through `.remedy-wt/f273-r2/run.py <cwd> <N> cmd...` (runs with an explicit `cwd`, prints the last N lines and `EXIT <returncode>`); every gate ran with `cwd=/home/decodeux/Repos/remedy` except G5, which ran in its own worktree.

- **Transport**, before any write: `.remedy-wt/f273-r2/verify.py` printed MATCH for all five payloads (block.md `ab6c5ef1fef1e078c96398d11692f66375294afd5d362a781816e698dce0472a`) and all three diffs, `ALL True`, EXIT 0.
- **G1** (at C5 `7a6b4c9a`, clean tree): `.remedy-wt/f273-r2/verify.py` re-printed MATCH for all eight digests, `ALL True`, EXIT 0; `.remedy-wt/f273-r2/g1.py`, EXIT 0:
  ```
  plan True
  .agent/live_review.md True
  .agent/prose_slips.md True
  .agent/decisions.md True
  authored/plan.md True
  authored/ledger.md True
  authored/slips.md True
  authored/decisions.md True
  authored/block.md True
  True
  ```
- **G2**: `git rev-parse 7a6b4c9a:tests 7a6b4c9a:packages 7a6b4c9a:apps 7a6b4c9a:docs`, exit 0:
  ```
  44f3310aababca7cab8ff948f05a00bb7fa099b7
  5753db4d19ac2331a1157a7362790d4fbcfd97db
  669c3a23f24a5dca64f2fc47dbd708c9084a1239
  b459d7c5dd6453012cc686a768b55d7cd0a8fadd
  ```
  All four equal the reviewer's dry-run subtrees.
- **G3** (primary checkout, serial, the block's 25 targets): `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_config.py ... tests/cli/test_job_show.py`:
  ```
  1544 passed in 237.91s (0:03:57)
  EXIT 0
  ```
  0 failed. No `R-0803:` line: the tail shows none, and `tests/conftest.py::pytest_sessionfinish` sets the exit status to TESTS_FAILED whenever it writes that line, so exit 0 proves it was not written.
- **G4** (primary checkout): `python3 -m ruff check --output-format concise` over the 12 Python files C2 to C4 touch, EXIT 1:
  ```
  tests/cli/test_teacher_cmd.py:622:9: I001 [*] Import block is un-sorted or un-formatted
  Found 1 error.
  [*] 1 fixable with the `--fix` option.
  ```
  Exactly the one expected finding. Line 622 at C5 is byte-identical to line 545 at `f32363e9` (`from packages.memory.local_gateway import store_memory, _jsonl_path, _load_entries, _rewrite_entries`); C3 inserted the 77 lines between them.
- **G5** (`python3 .remedy-wt/f273-r2/g5.py`, one worktree at `7a6b4c9a`, `python3 -B -m pytest -q -p no:cacheprovider` from its root, `__pycache__` purged before every run, each mutation reverted by its saved bytes and `git status --porcelain` read empty after every revert):
  ```
  import path: /home/decodeux/Repos/remedy/.remedy-wt/f273-r2-g5/packages/orchestration/token_ledger.py
  resolves inside worktree: True
  CONTROL (unmutated) test_token_ledger.py test_do_sequence_cli.py test_teacher_cmd.py: 196 passed in 62.59s — EXIT 0
  (a) token_ledger.py occurrences 1 -> test_token_ledger.py + test_do_sequence_cli.py: 9 failed, 157 passed — EXIT 1
      TestLiveMirrorOnTheProductionPath::test_a_fake_provider_job_yields_one_row_per_provider_call
      TestLiveMirrorOnTheProductionPath::test_the_live_row_says_exactly_what_the_evidence_files_say
      TestLiveMirrorOnTheProductionPath::test_the_live_row_is_the_row_backfill_would_have_written
      TestLiveMirrorOnTheProductionPath::test_re_exporting_the_same_job_adds_no_second_row
      TestCostTruthOnTheJobRunPath::test_unmeasured_cost_stays_honestly_unmeasured
      TestCostTruthOnTheJobRunPath::test_the_measured_row_carries_the_provider_reported_basis
      TestOneRowPerProviderCall::test_a_two_task_two_round_job_has_one_row_per_call_and_both_roles
      TestOneRowPerProviderCall::test_backfill_supersedes_a_task_runs_old_row_instead_of_double_counting
      tests/cli/test_do_sequence_cli.py::test_the_json_cost_has_a_row_per_role_with_the_ledgers_own_numbers
  (b) pingpong_loop.py occurrences 1 -> test_token_ledger.py: 2 failed, 121 passed — EXIT 1
      TestCostTruthOnTheJobRunPath::test_a_measured_run_leaves_a_row_stats_cost_finds
      TestCostTruthOnTheJobRunPath::test_the_measured_row_carries_the_provider_reported_basis
  (c) teacher_narration.py occurrences 1 (the two-line entry) -> test_teacher_cmd.py: 2 failed, 28 passed — EXIT 1
      TestTeacherNarratesTheUnifiedJobPath::test_every_emitted_kind_is_in_the_narration_table
      TestTeacherNarratesTheUnifiedJobPath::test_every_task_and_every_round_gets_a_sentence
  (d) pingpong_job.py occurrences 1 -> test_teacher_cmd.py + test_do_sequence_cli.py: 2 failed, 71 passed — EXIT 1
      tests/cli/test_teacher_cmd.py::TestTeacherNarratesTheUnifiedJobPath::test_every_task_and_every_round_gets_a_sentence
      tests/cli/test_do_sequence_cli.py::test_the_teacher_narrates_the_job_do_ran_without_a_budget
  ```
  Every named file went red under its mutation; no mutation stayed green. The worktree was then removed (see External actions).
- **G6** runs after the push and is reported in the round report, because this commit precedes it.
- Full suite: not run (amend0917-throughput).

## Authored-text proofs

- Every edited `.agent/` file was built by `python3 .remedy-wt/f273-r2/c1.py` from `git show f32363e9:<path>` bytes and the payload bytes; none was hand-edited. G1 re-proves every file and every `.agent/authored/f273-r2-*` copy against its payload.
- The code arrived only by `git apply` of the three reviewer-verified diffs, in the block's order; G2's subtree ids equal the reviewer's dry-run subtrees.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 bookkeeping | done | `a30377c1` |
| C2 round 1's reds | done | `cbbf10bd` |
| C3 R-0812 | done | `d2c65597` |
| C4 R-0807 code and tests | done | `b090e6f9` |
| C5 R-0807 docs | done | `7a6b4c9a` |
| C6 handoff + push | done | This commit, then the push |
| G1, G2, G3, G5 | done | EXIT 0 / exact match as above |
| G4 | done | The one expected pre-existing I001, EXIT 1 as the block predicts |
| G6 | done | After the push; in the round report |

## Open findings

On the committed `.agent/live_review.md` (C1 onwards; C2 to C5 do not touch it), by `.remedy-wt/f273-r1/openset.py`: 128 open BY DISTINCT ID (ids with a `^- R-\d+ — ` line minus ids with a `^Done: R-\d+ — ` line) and 127 by the canonical line formula `scripts/rotate_live_review.py::count_open_findings`. Highest id R-0981. The two drops from round 1's 130 and 129 are R-0804 and R-0810, whose resolutions C1 booked.

## Deviations & assumptions

- **Commit sequence:** as ordered: C1, C2, C3, C4, C5, C6, then the push. No extra commit.
- **Scratch runner:** the block names `.remedy-wt/f273-r1/run.py`, which takes no `cwd`; the worker wrote `.remedy-wt/f273-r2/run.py`, the same with an explicit `cwd` as the first argument, because the worker's shell cwd was the reviewer's `.remedy-wt/f273-r2-dry` worktree. Nothing was run in that worktree; every git command used `git -C` on the primary checkout.
- **G3 `R-0803:` evidence:** the runner kept the last 15 lines of output, so the absence of the line is shown by the tail and by exit 0 (the guard forces a nonzero exit whenever it writes the line), not by a full-output count.
- **G5 purge:** every purge found 0 `__pycache__` directories, because `python3 -B` writes none; the purge still ran before every run.
- **Scratch:** gitignored, under `.remedy-wt/f273-r2/`: `verify.py`, `c1.py`, `g1.py`, `g5.py`, `lines.py`, `run.py`, `msg1.txt` to `msg6.txt`.

## Next

1. Phase 1 rule 1 (`.agent/STOP`), then the review of round 2.

Operator questions open: 5
